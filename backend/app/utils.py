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
    查询与当前研究领域完全匹配的相关学生、教师、项目（排除自身表）
    """
    related_data = {'相关学生': [], '相关教职工': [], '相关科研项目': []}

    relation_map = {
        'Student': ('StudentResearchField', 'student_id', 'view_student', '相关学生'),
        'Teacher': ('TeacherResearchField', 'teacher_id', 'view_teacher', '相关教职工'),
        'Project': ('ProjectResearchField', 'project_id', 'view_project', '相关科研项目'),
    }

    for related_table, (middle_table, id_field, view_name, target_key) in relation_map.items():
        if related_table == table:
            continue  # 跳过当前主表

        try:
            # 精确匹配研究领域：完全包含全部 field_ids 的记录
            cursor.execute(
                f"""
                SELECT {id_field}
                FROM {middle_table}
                WHERE research_field IN ({','.join(['%s'] * len(field_ids))})
                GROUP BY {id_field}
                HAVING COUNT(DISTINCT research_field) = %s
                """, field_ids + [len(field_ids)])
            matched_ids = [str(row[id_field]) for row in cursor.fetchall()]
            if not matched_ids:
                continue

            placeholders = ','.join(['%s'] * len(matched_ids))
            sql = f"SELECT * FROM {view_name} WHERE {id_field} IN ({placeholders})"
            cursor.execute(sql, matched_ids)
            rows = cursor.fetchall()

            for idx, row in enumerate(rows, 1):
                row = dict(row)
                row['序号'] = idx
                row = {COLUMN_MAPPING.get(k, k): v for k, v in row.items()}  # 字段名转中文
                related_data[target_key].append(row)

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


def change_password(username, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM Users WHERE username=%s", (username, ))
        row = cursor.fetchone()
        if not row:
            return {'success': False, 'message': '用户不存在'}

        if row['password'] != old_password:
            return {'success': False, 'message': '原密码错误'}

        cursor.execute("UPDATE Users SET password=%s WHERE username=%s", (new_password, username))
        conn.commit()
        return {'success': True, 'message': '密码修改成功'}

    except Exception as e:
        conn.rollback()
        return {'success': False, 'message': f'修改失败: {str(e)}'}
    finally:
        cursor.close()
        conn.close()
