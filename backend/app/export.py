from flask import Blueprint, request, jsonify, send_from_directory, current_app, url_for
from flask_restx import Namespace, Resource, fields, reqparse
from openpyxl import Workbook
import os
import uuid
import pandas as pd
from app.utils import auth_required

# 创建蓝图和命名空间
export_bp = Blueprint('export', __name__)
ns = Namespace('export', description='数据导出操作')

# 导出请求模型
export_input = ns.model('ExportInput', {
    'data': fields.List(fields.Raw, required=True, description='当前查询结果数据（列表字典形式）'),
    'filename': fields.String(required=False, description='导出文件名，可选')
})

# 响应模型
export_response = ns.model('ExportResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='操作消息'),
    'download_url': fields.String(description='文件下载地址')
})


@ns.route('/excel')
class ExportExcel(Resource):

    @ns.expect(export_input)
    @ns.response(200, '导出成功', export_response)
    @ns.response(400, '无效请求')
    @ns.response(404, '未找到数据')
    @ns.doc(description='导出数据到Excel文件')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """
        接收前端查询结果并导出为 Excel 文件
        """
        try:
            payload = request.get_json()
            rows = payload.get('data', [])
            filename = payload.get('filename', '导出结果')

            if not rows:
                return {'success': False, 'message': '数据为空，无法导出'}, 400

            df = pd.DataFrame(rows)

            # 创建 Excel 文件
            wb = Workbook()
            ws = wb.active
            ws.title = filename

            # 写入表头（序号 + 所有字段）
            ws.append(['序号'] + list(df.columns))

            # 写入数据行
            for idx, row in enumerate(df.itertuples(index=False), start=1):
                ws.append([idx] + list(row))

            # 生成唯一文件名
            temp_dir = os.path.join(current_app.root_path, 'temp_exports')
            os.makedirs(temp_dir, exist_ok=True)
            unique_filename = f"{filename}_{uuid.uuid4().hex}.xlsx"
            file_path = os.path.join(temp_dir, unique_filename)
            wb.save(file_path)

            # 返回下载地址
            download_url = url_for('export_download_file', filename=unique_filename, _external=True)
            return {'success': True, 'message': '导出成功', 'download_url': download_url}

        except Exception as e:
            return {'success': False, 'message': f'导出失败: {str(e)}'}, 500


@ns.route('/download/<string:filename>')
@ns.param('filename', '要下载的文件名')
class DownloadFile(Resource):

    def get(self, filename):
        """下载Excel文件"""
        temp_dir = os.path.join(current_app.root_path, 'temp_exports')
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(file_path):
            return {'message': '文件不存在或已过期'}, 404

        return send_from_directory(temp_dir, filename, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
