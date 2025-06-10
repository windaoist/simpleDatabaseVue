from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.utils import COLUMN_MAPPING, get_related_data_api, auth_required
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
        """支持全字段模糊查询 + 多研究领域筛选 + 身份权限控制"""
        params = request.args
        keyword = params.get('keyword', '').strip()
        table = params.get('table')
        research_field_raw = params.get('research_field', '')
        user = request.user
        username = user['username']
        role = user['role']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 获取表字段名，排除 id 和 auto_increment
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            fields = [f['Field'] for f in cursor.fetchall() if f['Field'].lower() not in ['id']]

            # 构造模糊查询条件（全字段）
            like_conditions = [f"{table}.{col} LIKE %s" for col in fields]
            sql = f"SELECT DISTINCT {table}.* FROM {table}"  # DISTINCT 避免因 JOIN 多行重复
            joins = []
            wheres = ["(" + " OR ".join(like_conditions) + ")"]
            sql_params = [f"%{keyword}%"] * len(like_conditions)

            # 多研究领域筛选逻辑
            research_field_ids = [int(i) for i in research_field_raw.split('、') if i.strip().isdigit()]
            if research_field_ids:
                rel_table = {
                    'Student': 'StudentResearchField',
                    'Teacher': 'TeacherResearchField',
                    'Project': 'ProjectResearchField'
                }[table]
                id_col = {
                    'Student': 'student_id',
                    'Teacher': 'teacher_id',
                    'Project': 'project_id'
                }[table]
                joins.append(f"JOIN {rel_table} rf ON {table}.{id_col} = rf.{id_col}")
                placeholders = ','.join(['%s'] * len(research_field_ids))
                wheres.append(f"rf.field_id IN ({placeholders})")
                sql_params += research_field_ids

            # 项目权限限制（身份过滤）
            if table == 'Project':
                if role == 'Student':
                    joins.append("JOIN StudentProject sp ON Project.project_id = sp.project_id")
                    wheres.append("sp.student_id = %s")
                    sql_params.append(username)
                elif role == 'Teacher':
                    joins.append("JOIN TeacherProject tp ON Project.project_id = tp.project_id")
                    wheres.append("tp.teacher_id = %s")
                    sql_params.append(username)

            # 拼接最终SQL
            if joins:
                sql += " " + " ".join(joins)
            if wheres:
                sql += " WHERE " + " AND ".join(wheres)

            # 执行主查询
            cursor.execute(sql, sql_params)
            data_rows = cursor.fetchall()

            results = []
            for idx, row in enumerate(data_rows, 1):
                row = dict(row)
                row_display = {'序号': idx}

                # 查询并拼接研究领域（适配多对多结构）
                if table in ['Student', 'Teacher', 'Project']:
                    id_col = {
                        'Student': 'student_id',
                        'Teacher': 'teacher_id',
                        'Project': 'project_id'
                    }[table]
                    record_id = row[id_col]

                    cursor.execute(
                        f"SELECT rf.research_field FROM {table}ResearchField trf JOIN ResearchFields rf ON trf.field_id = rf.id WHERE trf.{id_col} = %s",
                        (record_id,))
                    field_names = [f['research_field'] for f in cursor.fetchall()]
                    row_display['研究领域'] = '、'.join(field_names) if field_names else '无'

                # 添加其他字段
                row_display.update({COLUMN_MAPPING.get(k, k): v for k, v in row.items() if k not in ['research_field']})
                results.append(row_display)

            # 关联查询（只在有研究领域ID的情况下做）
            related_data = get_related_data_api(cursor, table, research_field_ids) if research_field_ids else {}

            return {
                'success': True,
                'message': '查询成功' if results else '无匹配数据',
                'data': {
                    'results': convert_decimal(results),
                    'related_data': convert_decimal(related_data),
                    'query_params': {
                        'keyword': keyword,
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
