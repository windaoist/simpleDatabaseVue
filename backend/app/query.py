from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.utils import COLUMN_MAPPING, get_related_data_api, auth_required, api_response
from app.database import get_db_connection
import traceback
import decimal

query_bp = Blueprint('query_bp', __name__)
query_ns = Namespace('query', description='数据查询接口')

# Swagger响应模型
success_model = query_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据')
})
error_model = query_ns.model('ErrorResponse', {'success': fields.Boolean(default=False), 'message': fields.String(description='错误信息')})

# 请求参数定义
query_parser = reqparse.RequestParser()
query_parser.add_argument('keyword', type=str, help='模糊关键词（匹配所有字段）', location='args')
query_parser.add_argument('research_field', type=str, help='研究领域ID，多个用顿号分隔', location='args')
query_parser.add_argument('table', type=str, required=True, choices=('Student', 'Teacher', 'Project'), help='查询表名', location='args')


# decimal类型转换
def convert_decimal(obj):
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
    @query_ns.response(403, '权限不足')
    @query_ns.response(500, '服务器错误', error_model)
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def get(self):
        """支持字段字典模糊查询 + 多研究领域筛选 + 权限控制 + 视图优化"""
        params = request.args.to_dict()
        table = params.get('table')
        user = request.user
        username = user['username']
        role = user['role']

        if not table:
            return api_response(False, '缺少table参数', status=400)

        view_table = f"view_{table.lower()}"  # 使用视图查询
        keyword_dict = {k: v.strip() for k, v in params.items() if k not in ['table', 'research_field'] and v.strip()}

        # 处理研究领域（必须为列表）
        research_field_list = request.args.getlist('research_field')  # e.g., ?research_field=1&research_field=2
        research_field_ids = [int(i) for i in research_field_list if i.strip().isdigit()]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 获取字段名（用于合法性校验）
            cursor.execute(f"SHOW COLUMNS FROM {view_table}")
            valid_fields = [f['Field'] for f in cursor.fetchall()]
            wheres = []
            sql_params = []

            # 处理模糊查询（每个字段独立 LIKE）
            for field, keyword in keyword_dict.items():
                if field in valid_fields:
                    wheres.append(f"{field} LIKE %s")
                    sql_params.append(f"%{keyword}%")

            # 研究领域查询（IN 结构）
            if 'research_field' in valid_fields and research_field_ids:
                wheres.append("research_field REGEXP %s")
                pattern = '|'.join([str(fid) for fid in research_field_ids])
                sql_params.append(pattern)

            # 身份权限过滤（仅对 Project 表）
            if table == 'Project':
                if role == 'Student':
                    wheres.append("FIND_IN_SET(%s, leader_names) > 0 OR FIND_IN_SET(%s, member_names) > 0")
                    sql_params += [username, username]
                elif role == 'Teacher':
                    wheres.append("FIND_IN_SET(%s, teacher_names) > 0")
                    sql_params.append(username)

            # 拼接SQL
            sql = f"SELECT * FROM {view_table}"
            if wheres:
                sql += " WHERE " + " AND ".join(f"({w})" for w in wheres)

            cursor.execute(sql, sql_params)
            rows = cursor.fetchall()

            results = []
            for idx, row in enumerate(rows, 1):
                row = dict(row)
                row['序号'] = idx
                results.append({COLUMN_MAPPING.get(k, k): v for k, v in row.items()})

            # 查询关联数据（用于推荐或筛选）
            related_data = get_related_data_api(cursor, table, research_field_ids) if research_field_ids else {}

            return {
                'success': True,
                'message': '查询成功' if results else '无匹配数据',
                'data': {
                    'results': convert_decimal(results),
                    'related_data': convert_decimal(related_data),
                    'query_params': {
                        'filters': keyword_dict,
                        'research_field': research_field_ids,
                        'table': table
                    }
                }
            }

        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'message': f'服务器错误: {str(e)}'}, 500
        finally:
            cursor.close()
            conn.close()
