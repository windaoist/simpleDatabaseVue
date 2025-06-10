# from app.database import get_db_connection
from functools import wraps
from flask import request
from app.database import get_db_connection
import jwt
import os

# 表头映射字典
COLUMN_MAPPING = {
    'id': '序号',
    'research_field': '研究领域',
    'project_id': '项目编号',
    'project_name': '项目名称',
    'project_content': '项目内容',
    'leader_names': '负责人',
    'member_names': '成员',
    'teacher_names': '指导老师',
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
    使用 SQL 查询相关表的研究领域匹配数据
    """
    related_data = {'related_students': [],
                    'related_teachers': [], 'related_projects': []}

    fields = {'Student': 'research_field',
              'Teacher': 'research_field', 'Project': 'research_field'}

    for related_table, col in fields.items():
        if related_table == table:
            continue  # 跳过主表

        placeholders = ', '.join(['%s'] * len(field_ids))
        sql = f"SELECT * FROM {related_table} WHERE {col} IN ({placeholders})"

        try:
            cursor.execute(sql, field_ids)
            rows = cursor.fetchall()
            for idx, row in enumerate(rows, 1):
                row = dict(row)
                row['序号'] = idx
                related_data[f'related_{related_table.lower()}s'].append(row)
        except Exception as e:
            print(f"关联查询 {related_table} 出错: {e}")
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
