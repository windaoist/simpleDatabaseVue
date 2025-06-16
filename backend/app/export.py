import os
import uuid
import pandas as pd
from flask import Blueprint, current_app, request, send_from_directory, url_for
from flask_restx import Resource, fields, Namespace
from openpyxl import Workbook
from datetime import datetime
from app.utils import auth_required

# Blueprint 和 Namespace 保持一致
export_bp = Blueprint('export_bp', __name__)
ns = Namespace('export', description='数据导出接口')

# 定义模型
export_input = ns.model('ExportInput', {'data': fields.List(fields.Raw, required=True, description='待导出的数据')})

export_response = ns.model('ExportResponse', {'success': fields.Boolean, 'message': fields.String, 'download_url': fields.String})


@ns.route('/')
class ExportExcel(Resource):

    @ns.expect(export_input)
    @ns.response(200, '导出成功', export_response)
    @ns.response(400, '无效请求')
    @ns.response(500, '导出失败')
    @ns.doc(description='将前端查询结果导出为 Excel 文件（自动命名）')
    @auth_required(roles=['Admin', 'teacher', 'student'])
    def post(self):
        try:
            payload = request.get_json()
            rows = payload.get('data', [])

            if not rows:
                return {'success': False, 'message': '数据为空，无法导出'}, 400

            df = pd.DataFrame(rows)

            # 自动生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            suffix = uuid.uuid4().hex[:8]
            filename = f"Export_{timestamp}_{suffix}.xlsx"

            temp_dir = os.path.join(current_app.root_path, 'temp_exports')
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, filename)

            wb = Workbook()
            ws = wb.active
            ws.title = 'ExportedData'

            ws.append(['序号'] + list(df.columns))
            for idx, row in enumerate(df.itertuples(index=False), start=1):
                ws.append([idx] + list(row))

            wb.save(file_path)

            download_url = url_for('export_download_file', filename=filename, _external=True)
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
