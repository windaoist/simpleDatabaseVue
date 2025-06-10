import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app, url_for
from flask_restx import Namespace, Resource, fields, reqparse
from app.database import get_db_connection
from app.utils import COLUMN_MAPPING
from openpyxl import Workbook

# 创建蓝图和API实例
export_bp = Blueprint('export', __name__)
# api = Api(export_bp,
#           version='1.0',
#           title='数据导出API',
#           description='专家库、项目库和基金库数据导出接口')

# 创建命名空间
ns = Namespace('export', description='数据导出操作')

# 定义请求参数模型
export_parser = reqparse.RequestParser()
export_parser.add_argument('keyword1', type=str, required=True,
                           help='主关键词 (专家姓名/项目名称/基金名称)', location='args')
export_parser.add_argument('keyword2', type=str,
                           help='次要关键词 (产业领域/产业链/投资领域)', location='args')
export_parser.add_argument('table', type=str, required=True, choices=['Expert', 'Project', 'Fund'],
                           help='导出目标表: Expert/Project/Fund', location='args')

# 定义响应模型
export_response = ns.model('ExportResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='操作消息'),
    'download_url': fields.String(description='文件下载URL')
})


@ns.route('/excel')
class ExportExcel(Resource):
    @ns.expect(export_parser)
    @ns.response(200, '导出成功', export_response)
    @ns.response(400, '无效请求')
    @ns.response(404, '未找到数据')
    @ns.doc(description='导出数据到Excel文件')
    def get(self):
        """导出查询结果到Excel"""
        args = export_parser.parse_args()
        keyword1 = args['keyword1']
        keyword2 = args['keyword2']
        table = args['table']

        # 确定表和字段映射
        if table == 'Expert':
            column_name1 = 'expert_name'
            column_name2 = 'specific_industry'
            file_name = "专家库"
        elif table == 'Project':
            column_name1 = 'project_name'
            column_name2 = 'industry_chain'
            file_name = "项目库"
        elif table == 'Fund':
            column_name1 = 'fund_name'
            column_name2 = 'investment_area'
            file_name = "基金库"
        else:
            return {'success': False, 'message': '无效的表名'}, 400

        # 数据库查询
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = f"SELECT * FROM {table} WHERE {column_name1} LIKE %s"
        params = [f'%{keyword1}%']
        if keyword2:
            sql += f" AND {column_name2} = %s"
            params.append(keyword2)

        cursor.execute(sql, params)
        results = cursor.fetchall()

        if not results:
            return {'success': False, 'message': '未查询到匹配数据'}, 404

        # 获取产业映射
        cursor.execute("SELECT id, industry_name FROM KeyIndustries")
        industry_mapping = {row['id']: row['industry_name']
                            for row in cursor.fetchall()}

        # 处理产业字段
        for result in results:
            if 'industry_chain' in result:
                result['industry_chain'] = industry_mapping.get(
                    result['industry_chain'], '未知产业')
            if 'investment_area' in result:
                result['investment_area'] = industry_mapping.get(
                    result['investment_area'], '未知产业')
            if 'specific_industry' in result:
                result['specific_industry'] = industry_mapping.get(
                    result['specific_industry'], '未知产业')

        # 创建Excel文件
        wb = Workbook()
        ws = wb.active
        ws.title = table
        columns = ['序号'] + \
            [COLUMN_MAPPING.get(col, col) for col in results[0].keys()]
        ws.append(columns)

        for idx, row in enumerate(results, start=1):
            row_values = [idx] + list(row.values())
            ws.append(row_values)

        # 保存临时文件
        temp_dir = os.path.join(current_app.root_path, 'temp_exports')
        os.makedirs(temp_dir, exist_ok=True)
        unique_filename = f"{file_name}_{uuid.uuid4().hex}.xlsx"
        file_path = os.path.join(temp_dir, unique_filename)
        wb.save(file_path)

        cursor.close()
        connection.close()

        # 生成下载URL
        download_url = url_for('export_download_file',
                               filename=unique_filename, _external=True)
        return {
            'success': True,
            'message': '导出成功',
            'download_url': download_url
        }


@ns.route('/download/<string:filename>')
@ns.param('filename', '要下载的文件名')
class DownloadFile(Resource):
    @ns.response(200, '文件下载')
    @ns.response(404, '文件未找到')
    @ns.doc(description='下载导出的Excel文件')
    def get(self, filename):
        """下载Excel文件"""
        temp_dir = os.path.join(current_app.root_path, 'temp_exports')
        if not os.path.exists(os.path.join(temp_dir, filename)):
            return {'message': '文件不存在或已过期'}, 404

        return send_from_directory(
            temp_dir,
            filename,
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
