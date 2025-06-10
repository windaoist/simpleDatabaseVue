from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.utils import COLUMN_MAPPING
from .utils import get_related_data_api
from app.database import get_db_connection
import traceback
import pdb
import decimal

query_bp = Blueprint('query_bp', __name__)
# 创建命名空间
query_ns = Namespace('query', description='数据查询接口')

# 定义Swagger响应模型
success_model = query_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据')
})

error_model = query_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='操作是否成功', default=False),
    'message': fields.String(description='错误信息')
})

query_parser = reqparse.RequestParser()
query_parser.add_argument('keyword1', type=str,
                          help='主关键词（名称模糊匹配）', location='args')
query_parser.add_argument('keyword2', type=str,
                          help='产业名称筛选', location='args')
query_parser.add_argument('table', type=str, required=True,
                          choices=('Expert', 'Project', 'Fund'),
                          help='查询表名（必须是 Expert, Project 或 Fund）', location='args')


def convert_decimal(obj):
    """递归将对象中的Decimal转为float"""
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj


@query_ns.route('/')
class QueryResource(Resource):
    @query_ns.doc('query_data')
    @query_ns.expect(query_parser)
    @query_ns.response(200, '成功响应', success_model)
    @query_ns.response(400, '参数错误', error_model)
    @query_ns.response(500, '服务器错误', error_model)
    def get(self):
        """执行数据查询"""
        params = request.args
        keyword1 = params.get('keyword1', '').strip()
        keyword2_name = params.get('keyword2', '').strip()
        table = params.get('table')
        # 参数验证
        if not table or table not in ['Expert', 'Project', 'Fund']:
            return {'success': False, 'message': '无效的表名参数，必须是 Expert, Project, 或 Fund 之一'}, 400

        # 映射表配置
        table_config = {
            'Expert': {'name_field': 'expert_name', 'industry_field': 'specific_industry'},
            'Project': {'name_field': 'project_name', 'industry_field': 'industry_chain'},
            'Fund': {'name_field': 'fund_name', 'industry_field': 'investment_area'}
        }
        config = table_config[table]

        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # 获取产业映射数据
            cursor.execute("SELECT id, industry_name FROM KeyIndustries")
            industries = cursor.fetchall()
            id_to_name = {row['id']: row['industry_name']
                          for row in industries}
            name_to_id = {row['industry_name']: row['id']
                          for row in industries}

            # 处理产业筛选条件
            keyword2_id = name_to_id.get(
                keyword2_name) if keyword2_name else None
            if keyword2_name and not keyword2_id:
                # 未找到匹配的产业ID
                return {
                    'success': True,
                    'message': f"未找到产业名称 '{keyword2_name}' 的匹配ID",
                    'data': {
                        'results': [],
                        'related_data': get_related_data_api(cursor, id_to_name, table, None)
                    }
                }

            # 构建查询
            query = f"SELECT * FROM {table} WHERE {config['name_field']} LIKE %s"
            params = [f'%{keyword1}%']

            if keyword2_id:
                query += f" AND {config['industry_field']} = %s"
                params.append(keyword2_id)

            cursor.execute(query, params)
            raw_results = cursor.fetchall()

            # 处理结果集
            processed_results = []
            for idx, row in enumerate(raw_results, 1):
                processed_row = {'序号': idx}

                # 产业ID转名称
                industry_id = row.get(config['industry_field'])
                if industry_id:
                    row = dict(row)
                    row[config['industry_field']] = id_to_name.get(
                        industry_id, f"未知产业ID: {industry_id}")

                # 合并数据并映射列名
                processed_row.update({
                    COLUMN_MAPPING.get(col, col): val
                    for col, val in row.items()
                })
                processed_results.append(processed_row)

            # 获取关联数据
            related_data = get_related_data_api(
                cursor, id_to_name, table, keyword2_id)

            # Decimal 转换
            processed_results = convert_decimal(processed_results)
            related_data = convert_decimal(related_data)

            # 构造响应
            response_data = {
                'query_params': {
                    'keyword1': keyword1,
                    'keyword2_name': keyword2_name,
                    'keyword2_id': keyword2_id,
                    'table': table
                },
                'results': processed_results,
                'related_data': related_data
            }

            message = "查询成功"
            if not processed_results and not any(related_data.values()):
                message = "未查询到匹配数据"
            # pdb.set_trace()
            return {'success': True, 'message': message, 'data': response_data}

        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'message': f'服务器错误: {str(e)}'}, 500
        finally:
            if connection:
                connection.close()
