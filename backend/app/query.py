from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from app.utils import COLUMN_MAPPING, get_related_data_api, auth_required, api_response
from app.database import get_db_connection
import traceback
import decimal
from app.utils import get_fields

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
query_model = query_ns.model(
    'QueryRequest', {
        'table': fields.String(required=True, description='查询的目标表', enum=['Student', 'Teacher', 'Project'], example='Student'),
        'filters': fields.Raw(required=False, description='字段过滤条件（动态键值对）', example={
            'name': '张三',
            'gender': '男'
        }),
        'research_field': fields.List(fields.Integer, required=False, description='研究领域ID列表', example=[1, 3])
    })


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


@query_ns.route('/research_fields')
class FieldData(Resource):

    @query_ns.response(200, '研究领域数据获取成功')
    @query_ns.response(500, '获取研究领域数据失败')
    def get(self):
        """获取所有研究领域数据"""
        try:
            research_fields = get_fields()
            return api_response(True, '研究领域数据获取成功', {'research_fields': research_fields})
        except Exception as e:
            return api_response(False, f'获取研究领域数据失败: {str(e)}', status=500)


@query_ns.route('/')
class QueryResource(Resource):

    @query_ns.doc('query_data')
    @query_ns.expect(query_model)
    @query_ns.response(200, '成功响应', success_model)
    @query_ns.response(400, '参数错误', error_model)
    @query_ns.response(403, '权限不足')
    @query_ns.response(500, '服务器错误', error_model)
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """支持字段字典模糊查询 + 多研究领域筛选 + 权限控制 + 视图优化"""
        data = request.get_json()
        if not data:
            return api_response(False, '请求体必须为JSON', status=400)

        table = data.get('table')
        filters = data.get('filters', {})
        research_field_ids = data.get('research_field', [])
        user = request.user
        username = user['username']  # 学号/工号
        role = user['role']

        if not table:
            return api_response(False, '缺少table参数', status=400)

        view_table = f"view_{table.lower()}"

        # 清洗filters
        keyword_dict = {}
        if isinstance(filters, dict):
            keyword_dict = {k: v.strip() for k, v in filters.items() if isinstance(v, str) and v.strip()}
            keyword_dict.update({k: v for k, v in filters.items() if not isinstance(v, str)})

        # 转换研究领域
        if not isinstance(research_field_ids, list):
            research_field_ids = []
        try:
            research_field_ids = [int(i) for i in research_field_ids]
        except Exception:
            research_field_ids = []

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 字段合法性校验
            cursor.execute(f"SHOW COLUMNS FROM {view_table}")
            valid_fields = [f['Field'] for f in cursor.fetchall()]

            wheres = []
            sql_params = []

            # 模糊匹配字段
            for field, keyword in keyword_dict.items():
                if field in valid_fields:
                    wheres.append(f"{field} LIKE %s")
                    sql_params.append(f"%{keyword}%")

            # 研究领域模糊匹配
            if 'research_field' in valid_fields and research_field_ids:
                pattern = '|'.join(map(str, research_field_ids))
                wheres.append("research_field REGEXP %s")
                sql_params.append(pattern)

            # 权限控制（仅对 Project 表）
            if table.lower() == 'project':
                if role == 'Student':
                    # 匹配姓名(学号)
                    wheres.append("(leader LIKE %s OR member LIKE %s)")
                    like_pattern = f"%({username})%"
                    sql_params += [like_pattern, like_pattern]
                elif role == 'Teacher':
                    wheres.append("teacher LIKE %s")
                    sql_params.append(f"%({username})%")

            # 构造 SQL
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
