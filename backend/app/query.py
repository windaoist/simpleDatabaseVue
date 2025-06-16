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
        """支持字段字典模糊查询 + 多研究领域筛选 + 权限控制"""
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

        # 限制学生只可访问 Project 表
        if role == 'Student' and table.lower() != 'project':
            return api_response(False, '学生无权限访问该表', status=403)

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

            # 模糊字段匹配
            for field, keyword in keyword_dict.items():
                if field in valid_fields:
                    wheres.append(f"{field} LIKE %s")
                    sql_params.append(f"%{keyword}%")

            # 前端传的是研究领域ID列表，必须关联 ProjectResearchField 表来筛选 project_id
            if table.lower() == 'project' and research_field_ids:
                # 查找同时包含所有 research_field_ids 的项目
                cursor.execute(
                    f"""
                    SELECT project_id
                    FROM ProjectResearchField
                    WHERE research_field IN ({','.join(['%s'] * len(research_field_ids))})
                    GROUP BY project_id
                    HAVING COUNT(DISTINCT research_field) = %s
                    """, research_field_ids + [len(research_field_ids)])
                field_project_ids = [str(row['project_id']) for row in cursor.fetchall()]
                if not field_project_ids:
                    return api_response(True, '暂无匹配研究领域的项目', data={'results': [], 'query_params': data})

                placeholders = ','.join(['%s'] * len(field_project_ids))
                wheres.append(f"project_id IN ({placeholders})")
                sql_params += field_project_ids
            elif table.lower() == 'student' and research_field_ids:
                cursor.execute(
                    f"""
                    SELECT student_id
                    FROM StudentResearchField
                    WHERE research_field IN ({','.join(['%s'] * len(research_field_ids))})
                    GROUP BY student_id
                    HAVING COUNT(DISTINCT research_field) = %s
                    """, research_field_ids + [len(research_field_ids)])
                field_student_ids = [str(row['student_id']) for row in cursor.fetchall()]
                if not field_student_ids:
                    return api_response(True, '暂无匹配研究领域的学生', data={'results': [], 'query_params': data})

                placeholders = ','.join(['%s'] * len(field_student_ids))
                wheres.append(f"student_id IN ({placeholders})")
                sql_params += field_student_ids
            elif table.lower() == 'teacher' and research_field_ids:
                cursor.execute(
                    f"""
                    SELECT teacher_id
                    FROM TeacherResearchField
                    WHERE research_field IN ({','.join(['%s'] * len(research_field_ids))})
                    GROUP BY teacher_id
                    HAVING COUNT(DISTINCT research_field) = %s
                    """, research_field_ids + [len(research_field_ids)])
                field_teacher_ids = [str(row['teacher_id']) for row in cursor.fetchall()]
                if not field_teacher_ids:
                    return api_response(True, '暂无匹配研究领域的教师', data={'results': [], 'query_params': data})

                placeholders = ','.join(['%s'] * len(field_teacher_ids))
                wheres.append(f"teacher_id IN ({placeholders})")
                sql_params += field_teacher_ids

            # 权限控制逻辑（仅Project表启用）
            if table.lower() == 'project':
                if role == 'Student':
                    # 查找该学生参与的所有项目编号
                    cursor.execute("SELECT project_id FROM StudentProject WHERE student_id = %s", (username, ))
                    project_ids = [str(row['project_id']) for row in cursor.fetchall()]
                    if not project_ids:
                        return api_response(True, '暂无匹配数据', data={'results': [], 'related_data': {'相关学生': [], '相关教职工': [], '相关科研项目': []}, 'query_params': data})

                    placeholders = ','.join(['%s'] * len(project_ids))
                    wheres.append(f"project_id IN ({placeholders})")
                    sql_params += project_ids

                elif role == 'Teacher':
                    # 查找该教师参与的所有项目编号
                    cursor.execute("SELECT project_id FROM TeacherProject WHERE teacher_id = %s", (username, ))
                    project_ids = [str(row['project_id']) for row in cursor.fetchall()]
                    if not project_ids:
                        return api_response(True, '暂无匹配数据', data={'results': [], 'related_data': {'相关学生': [], '相关教职工': [], '相关科研项目': []}, 'query_params': data})

                    placeholders = ','.join(['%s'] * len(project_ids))
                    wheres.append(f"project_id IN ({placeholders})")
                    sql_params += project_ids

            # 构建最终SQL
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

            related_data = get_related_data_api(cursor, table, research_field_ids) if research_field_ids else {'相关学生': [], '相关教职工': [], '相关科研项目': []}

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


@query_ns.route('/statistics')
class ProjectStatistics(Resource):

    @query_ns.response(200, '统计成功', success_model)
    @query_ns.response(500, '服务器错误', error_model)
    @auth_required(roles=['Admin'])
    def get(self):
        """
        按项目负责人专业统计科研项目各状态的通过数量（使用存储过程）
        """

        def convert_decimal_to_str(obj):
            if isinstance(obj, list):
                return [convert_decimal_to_str(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_decimal_to_str(v) for k, v in obj.items()}
            elif isinstance(obj, decimal.Decimal):
                return str(obj)
            else:
                return obj

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 调用存储过程
            cursor.callproc('GetProjectStatisticsByMajor')

            # MySQL中结果要用 nextset()
            for result in cursor.stored_results():
                data = result.fetchall()

            return api_response(True, '统计成功', {'results': convert_decimal_to_str(data)})

        except Exception as e:
            traceback.print_exc()
            return api_response(False, f'服务器错误: {str(e)}', status=500)

        finally:
            cursor.close()
            conn.close()
