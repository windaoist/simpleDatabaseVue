from app.database import get_db_connection
from functools import wraps
from flask import request
import jwt
import os

# 表头映射字典
COLUMN_MAPPING = {
    'id': '序号',
    'research_field': '研究领域',
    'project_id': '项目编号',
    'project_name': '项目名称',
    'project_content': '项目内容',
    'leader': '负责人',
    'member': '成员',
    'teacher': '指导教师',
    'project_application_status': '申报状态',
    'project_approval_status': '审批状态',
    'project_acceptance_status': '验收状态',
    'student_id': '学生学号',
    'name': '姓名',
    'gender': '性别',
    'grade': '年级',
    'major': '专业',
    'class': '班级',
    'phone': '联系电话',
    'email': '电子邮箱',
    'teacher_id': '教职工号',
    'title': '职称',
    'college': '所属学院',
    'department': '所属专业',
    'office_location': '办公地点',
    'introduction': '个人简介'
}


def api_response(success, message, data=None, status=200):
    """统一API响应格式"""
    return {'success': success, 'message': message, 'data': data}, status

# # 获取ID
# def get_field_id(research_field):
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (research_field, ))
#     result = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if result:
#         return result['id']
#     return None


# 获取研究领域列表
def get_fields():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, research_field FROM ResearchFields")
    fields = cursor.fetchall()
    cursor.close()
    connection.close()

    return fields


def get_related_data_api(cursor, table, field_ids):
    """
    使用视图查询研究领域匹配数据（排除自身）
    """
    related_data = {
        'related_students': [],
        'related_teachers': [],
        'related_projects': []
    }

    view_map = {
        'Student': 'view_student',
        'Teacher': 'view_teacher',
        'Project': 'view_project'
    }

    for related_table in ['Student', 'Teacher', 'Project']:
        if related_table == table:
            continue  # 跳过主表

        view_name = view_map[related_table]

        try:
            # 使用 REGEXP 匹配研究领域
            pattern = '|'.join([str(fid) for fid in field_ids])
            sql = f"SELECT * FROM {view_name} WHERE research_field REGEXP %s"
            cursor.execute(sql, (pattern,))
            rows = cursor.fetchall()

            for idx, row in enumerate(rows, 1):
                row = dict(row)
                row['序号'] = idx
                related_data[f'related_{related_table.lower()}s'].append(row)

        except Exception as e:
            print(f"[相关数据查询失败] {related_table}: {e}")
            continue

    return related_data


SECRET_KEY = os.environ.get("JWT_SECRET", "my_jwt_secret")


def auth_required(roles=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return {'success': False, 'message': '未提供有效的身份令牌'}, 401

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_role = payload.get('role')
                if roles and user_role not in roles:
                    return {'success': False, 'message': '权限不足'}, 403

                # 可选：注入用户信息供后续使用
                request.user = payload
                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return {'success': False, 'message': '令牌已过期'}, 401
            except jwt.InvalidTokenError:
                return {'success': False, 'message': '无效令牌'}, 401

        return wrapper

    return decorator
