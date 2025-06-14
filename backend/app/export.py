import os
import uuid
import pandas as pd
from flask import current_app, request, send_from_directory, url_for
from flask_restx import Resource, fields, Namespace
from openpyxl import Workbook
from datetime import datetime
from app.utils import auth_required

ns = Namespace('data', path='/', description='数据操作接口')

export_bp = ns.model('ExportInput', {'data': fields.List(fields.Raw, required=True, description='待导出的数据')})

export_response = ns.model('ExportResponse', {'success': fields.Boolean, 'message': fields.String, 'download_url': fields.String})


@ns.route('/export')
class ExportExcel(Resource):

    @ns.expect(export_bp)
    @ns.response(200, '导出成功', export_response)
    @ns.response(400, '无效请求')
    @ns.response(500, '导出失败')
    @ns.doc(description='将前端查询结果导出为Excel文件（文件名自动生成）')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        try:
            payload = request.get_json()
            rows = payload.get('data', [])

            if not rows:
                return {'success': False, 'message': '数据为空，无法导出'}, 400

            df = pd.DataFrame(rows)

            # 自动生成文件名：Export_20250614_223000_abcd1234.xlsx
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_suffix = uuid.uuid4().hex[:8]
            filename = f"Export_{timestamp}_{random_suffix}.xlsx"

            # 创建目录
            temp_dir = os.path.join(current_app.root_path, 'temp_exports')
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, filename)

            # 写入 Excel 文件
            wb = Workbook()
            ws = wb.active
            ws.title = 'ExportedData'

            # 表头
            headers = list(df.columns)
            ws.append(['序号'] + headers)

            # 数据行
            for idx, row in enumerate(df.itertuples(index=False), start=1):
                ws.append([idx] + list(row))

            wb.save(file_path)

            # 返回下载链接
            download_url = url_for('data_download_file', filename=filename, _external=True)
            return {'success': True, 'message': '导出成功', 'download_url': download_url}

        except Exception as e:
            return {'success': False, 'message': f'导出失败: {str(e)}'}, 500


@ns.route('/download/<string:filename>')
@ns.param('filename', '要下载的文件名')
class DownloadFile(Resource):

    def get(self, filename):
        """下载已导出的 Excel 文件"""
        temp_dir = os.path.join(current_app.root_path, 'temp_exports')
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(file_path):
            return {'message': '文件不存在或已过期'}, 404

        return send_from_directory(temp_dir, filename, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
