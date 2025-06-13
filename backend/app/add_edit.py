from flask import Blueprint, request
from flask_restx import Resource, fields, Namespace, reqparse
from app.utils import auth_required, api_response
from app.database import get_db_connection

# 创建蓝图和 API 实例
add_edit_bp = Blueprint('add_edit', __name__)

# 创建命名空间
ns = Namespace('data', path='/', description='数据操作接口')

# 教职工模型
teacher_model = ns.model(
    'Teacher', {
        'teacher_id': fields.String(required=True, description='教职工号'),
        'name': fields.String(required=True, description='姓名'),
        'gender': fields.String(description='性别，男或女'),
        'title': fields.String(description='职称'),
        'college': fields.String(description='所属学院'),
        'department': fields.String(description='所属专业'),
        'research_field': fields.String(description='研究领域，多个用顿号分隔'),
        'phone': fields.String(description='联系电话'),
        'email': fields.String(description='电子邮箱'),
        'office_location': fields.String(description='办公地点'),
        'introduction': fields.String(description='个人简介')
    })

# 学生模型
student_model = ns.model(
    'Student', {
        'student_id': fields.String(required=True, description='学生学号'),
        'name': fields.String(required=True, description='姓名'),
        'gender': fields.String(description='性别，男或女'),
        'grade': fields.String(description='年级'),
        'major': fields.String(description='专业'),
        'class': fields.String(description='班级'),
        'research_field': fields.String(description='研究领域，多个用顿号分隔'),
        'phone': fields.String(description='联系电话'),
        'email': fields.String(description='电子邮箱')
    })

# 科研项目模型
project_model = ns.model(
    'Project', {
        'project_id': fields.String(required=True, description='项目编号'),
        'name': fields.String(required=True, description='项目名称'),
        'research_field': fields.String(required=True, description='研究领域，多个用顿号分隔'),
        '负责人学号': fields.String(description='负责人学号，仅1个'),
        '成员学号': fields.String(description='成员学号，最多4个，用顿号分隔'),
        '指导教师工号': fields.String(description='指导教师工号，最多2个，用顿号分隔'),
        'project_content': fields.String(description='项目内容')
    })

# 删除操作解析器
delete_parser = reqparse.RequestParser()
delete_parser.add_argument('table', type=str, required=True, help='表名', location='json')
delete_parser.add_argument('key', type=str, required=True, help='主键值', location='json')

# 编辑操作解析器
edit_parser = reqparse.RequestParser()
edit_parser.add_argument('table', type=str, required=True, help='表名', location='json')
edit_parser.add_argument('old_key', type=str, required=True, help='原主键ID', location='json')


@ns.route('/validate_id')
class ValidateID(Resource):

    @ns.doc(params={'type': 'student/teacher', 'id': '输入的学号或工号'})
    def get(self):
        """校验输入的学号/工号是否存在，并返回姓名"""
        id_type = request.args.get('type')
        person_id = request.args.get('id')

        if id_type not in ['student', 'teacher']:
            return api_response(False, '类型必须为student或teacher', status=400)

        table = 'Student' if id_type == 'student' else 'Teacher'
        id_field = 'student_id' if id_type == 'student' else 'teacher_id'
        name_field = 'name'

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT {name_field} FROM {table} WHERE {id_field} = %s", (person_id, ))
            row = cursor.fetchone()
            if row:
                return api_response(True, f"{id_type} 存在", {'valid': True, f'{id_type}_name': row[name_field]})
            else:
                return api_response(True, f"{id_type} 不存在", {'valid': False})
        finally:
            cursor.close()
            connection.close()


@ns.route('/add')
class AddData(Resource):

    @ns.expect(
        ns.model('AddRequest', {
            'table': fields.String(required=True, enum=['Student', 'Teacher', 'Project'], description='表名'),
            'data': fields.Raw(required=True, description='数据内容')
        }))
    @ns.response(200, '添加成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(403, '权限不足')
    @ns.response(409, '数据已存在')
    @ns.response(500, '数据库错误')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """添加新数据"""
        user = request.user
        user_id = user['username']
        role = user['role']

        data = request.get_json()
        if not data:
            return api_response(False, '请求数据格式错误', status=400)

        table = data.get('table')
        if not table:
            return api_response(False, '缺少表名参数', status=400)

        record_data = data.get('data', {})
        connection = get_db_connection()
        cursor = connection.cursor()
        response_data = {'table': table}

        try:
            if table == 'student':
                if role != 'Admin':
                    return api_response(False, '仅管理员可添加学生信息', status=403)

                required_fields = ['student_id', 'name']
                if not all(record_data.get(field) and str(record_data.get(field)).strip() for field in required_fields):
                    return api_response(False, '存在必要字段为空', status=400)

                # 检查重复项
                cursor.execute("SELECT 1 FROM Student WHERE student_id = %s", (record_data['student_id'], ))
                if cursor.fetchone():
                    return api_response(False, '该学生已存在', {'type': 'duplicate'}, 409)

                # 插入学生表
                cursor.execute("INSERT INTO Student (student_id, name, gender, grade, major, class, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (record_data['student_id'], record_data['name'], record_data.get('gender', ''), record_data.get('grade', ''),
                                record_data.get('major', ''), record_data.get('class', ''), record_data.get('phone', ''), record_data.get('email', '')))

                # 插入研究领域关联表
                field_names = record_data.get('research_field', '')
                if field_names:
                    fields = [f.strip() for f in field_names.split('、') if f.strip()]
                    for fname in fields:
                        cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (fname, ))
                        row = cursor.fetchone()
                        if row:
                            cursor.execute("INSERT IGNORE INTO StudentResearchField (student_id, research_field) VALUES (%s, %s)",
                                           (record_data['student_id'], row['id']))

                response_data['record'] = {'student_id': record_data['student_id']}

            elif table == 'teacher':
                if role != 'Admin':
                    return api_response(False, '仅管理员可添加教师信息', status=403)

                required_fields = ['teacher_id', 'name']
                if not all(record_data.get(field) and str(record_data.get(field)).strip() for field in required_fields):
                    return api_response(False, '存在必要字段为空', status=400)

                # 检查重复项
                cursor.execute("SELECT 1 FROM Teacher WHERE teacher_id = %s", (record_data['teacher_id'], ))
                if cursor.fetchone():
                    return api_response(False, '该教师已存在', {'type': 'duplicate'}, 409)

                # 插入教师表
                cursor.execute(
                    "INSERT INTO Teacher (teacher_id, name, gender, title, college, department, phone, email, office_location, introduction) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (record_data['teacher_id'], record_data['name'], record_data.get('gender', ''), record_data.get('title', ''), record_data.get(
                        'college', ''), record_data.get('department', ''), record_data.get('phone', ''), record_data.get(
                            'email', ''), record_data.get('office_location', ''), record_data.get('introduction', '')))

                # 插入研究领域
                field_names = record_data.get('research_field', '')
                if field_names:
                    fields = [f.strip() for f in field_names.split('、') if f.strip()]
                    for fname in fields:
                        cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (fname, ))
                        row = cursor.fetchone()
                        if row:
                            cursor.execute("INSERT IGNORE INTO TeacherResearchField (teacher_id, research_field) VALUES (%s, %s)",
                                           (record_data['teacher_id'], row['id']))

                response_data['record'] = {'teacher_id': record_data['teacher_id']}

            elif table == 'project':
                if role != 'Student':
                    return api_response(False, '仅学生可添加科研项目信息', status=403)

                # 判断学生是否已是某项目负责人
                cursor.execute("SELECT COUNT(*) FROM StudentProject WHERE student_id=%s AND role='负责人'", (user_id, ))
                count = cursor.fetchone()
                if count[0] >= 1:
                    return api_response(False, '您已作为负责人参与一个项目，不能再次创建', status=409)

                required_fields = ['project_id', 'name']
                if not all(record_data.get(field) and str(record_data.get(field)).strip() for field in required_fields):
                    return api_response(False, '存在必要字段为空', status=400)

                project_id = record_data['project_id']
                cursor.execute("SELECT 1 FROM Project WHERE project_id=%s", (project_id, ))
                if cursor.fetchone():
                    return api_response(False, '项目已存在', {'type': 'duplicate'}, 409)

                # 当前用户就是负责人，不能传 leader 字段
                student_leader_id = user_id

                # 获取成员与教师 ID
                member_ids = [s.strip() for s in record_data.get('member_ids', '').split('、') if s.strip()]
                teacher_ids = [t.strip() for t in record_data.get('teacher_ids', '').split('、') if t.strip()]

                # 负责人不能出现在成员中
                if student_leader_id in member_ids:
                    return api_response(False, '负责人不能同时是成员', status=400)

                # 成员数量限制
                if len(member_ids) > 4:
                    return api_response(False, '成员不能超过4人', status=400)

                # 教师数量限制
                if len(teacher_ids) > 2:
                    return api_response(False, '指导教师不能超过2人', status=400)

                # 校验成员学生是否存在
                for sid in member_ids:
                    cursor.execute("SELECT name FROM Student WHERE student_id=%s", (sid, ))
                    student_row = cursor.fetchone()
                    if not student_row:
                        return api_response(False, f"学生学号不存在：{sid}", status=400)

                # 校验教师是否存在
                for tid in teacher_ids:
                    cursor.execute("SELECT name FROM Teacher WHERE teacher_id=%s", (tid, ))
                    teacher_row = cursor.fetchone()
                    if not teacher_row:
                        return api_response(False, f"教师工号不存在：{tid}", status=400)

                # 插入主表
                cursor.execute(
                    "INSERT INTO Project (project_id, name, project_content, project_application_status, project_approval_status, project_acceptance_status) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (project_id, record_data['name'], record_data['project_content'], record_data.get(
                        'project_application_status', ''), record_data.get('project_approval_status', ''), record_data.get('project_acceptance_status', '')))

                # 插入研究领域
                field_str = record_data.get('research_field', '')
                research_fields = [int(fid) for fid in field_str.split('、') if fid.isdigit()]
                for fid in research_fields:
                    cursor.execute("INSERT IGNORE INTO ProjectResearchField (project_id, research_field) VALUES (%s, %s)", (project_id, fid))

                # 插入负责人（当前用户）
                cursor.execute("SELECT name FROM Student WHERE student_id=%s", (student_leader_id, ))
                student_row = cursor.fetchone()
                if student_row:
                    leader_display = f"{student_row['name']}（{student_leader_id}）"
                    cursor.execute("INSERT INTO StudentProject (student_id, project_id, role, display) VALUES (%s, %s, '负责人', %s)",
                                   (student_leader_id, project_id, leader_display))

                # 插入成员
                for sid in member_ids:
                    cursor.execute("SELECT name FROM Student WHERE student_id=%s", (sid, ))
                    name_row = cursor.fetchone()
                    if name_row:
                        display = f"{name_row['name']}（{sid}）"
                        cursor.execute("INSERT INTO StudentProject (student_id, project_id, role, display) VALUES (%s, %s, '成员', %s)",
                                       (sid, project_id, display))

                # 插入教师
                for tid in teacher_ids:
                    cursor.execute("SELECT name FROM Teacher WHERE teacher_id=%s", (tid, ))
                    name_row = cursor.fetchone()
                    if name_row:
                        display = f"{name_row['name']}（{tid}）"
                        cursor.execute("INSERT INTO TeacherProject (teacher_id, project_id, display) VALUES (%s, %s, %s)", (tid, project_id, display))

                response_data['record'] = {'project_id': project_id}

            else:
                return api_response(False, '不支持的表名', status=400)

            connection.commit()
            return api_response(True, '添加成功', response_data)

        except Exception as e:
            connection.rollback()
            return api_response(False, f'数据库错误: {str(e)}', status=500)
        finally:
            cursor.close()
            connection.close()


@ns.route('/edit')
class EditData(Resource):

    @ns.expect(
        ns.model(
            'EditRequest', {
                'table': fields.String(required=True, enum=['Student', 'Teacher', 'Project'], description='表名'),
                'old_key': fields.String(required=True, description='原主键'),
                'data': fields.Raw(required=True, description='新数据内容')
            }))
    @ns.response(200, '更新成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(403, '权限不足')
    @ns.response(409, '数据已存在')
    @ns.response(500, '数据库错误')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """编辑现有数据"""
        user = request.user
        user_id = user['username']
        role = user['role']

        data = request.get_json()
        if not data:
            return api_response(False, '请求数据格式错误', status=400)

        table = data.get('table')
        old_key = data.get('old_key')
        record_data = data.get('data', {})

        if not table or not old_key:
            return api_response(False, '缺少必要参数', status=400)

        connection = get_db_connection()
        cursor = connection.cursor()
        response_data = {'table': table}

        try:
            if table == 'student':
                if role != 'Admin':
                    return api_response(False, '仅管理员可编辑学生信息', status=403)

                new_key = record_data.get('student_id')
                if new_key != old_key:
                    cursor.execute("SELECT 1 FROM Student WHERE student_id=%s", (new_key, ))
                    if cursor.fetchone():
                        return api_response(False, '学生学号已存在', {'type': 'duplicate'}, 409)

                cursor.execute("UPDATE Student SET student_id=%s, name=%s, gender=%s, grade=%s, major=%s, class=%s, phone=%s, email=%s "
                               "WHERE student_id=%s",
                               (new_key, record_data.get('name', ''), record_data.get('gender', ''), record_data.get('grade', ''), record_data.get(
                                   'major', ''), record_data.get('class', ''), record_data.get('phone', ''), record_data.get('email', ''), old_key))

                cursor.execute("DELETE FROM StudentResearchField WHERE student_id=%s", (new_key, ))
                # 兼容格式处理：研究领域为ID列表或用顿号分隔的字符串
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                    research_fields = [row['id'] for row in cursor.fetchall()]
                for rf_id in research_fields:
                    cursor.execute("INSERT INTO StudentResearchField (student_id, research_field) VALUES (%s, %s)", (new_key, rf_id))
                response_data['record'] = {'student_id': new_key}

            elif table == 'teacher':
                if role != 'Admin':
                    return api_response(False, '仅管理员可编辑教师信息', status=403)

                new_key = record_data.get('teacher_id')
                if new_key != old_key:
                    cursor.execute("SELECT 1 FROM Teacher WHERE teacher_id=%s", (new_key, ))
                    if cursor.fetchone():
                        return api_response(False, '教职工号已存在', {'type': 'duplicate'}, 409)

                cursor.execute(
                    "UPDATE Teacher SET teacher_id=%s, name=%s, gender=%s, title=%s, college=%s, department=%s, phone=%s, email=%s, office_location=%s, introduction=%s "
                    "WHERE teacher_id=%s", (new_key, record_data.get('name', ''), record_data.get('gender', ''), record_data.get(
                        'title', ''), record_data.get('college', ''), record_data.get('department', ''), record_data.get(
                            'phone', ''), record_data.get('email', ''), record_data.get('office_location', ''), record_data.get('introduction', ''), old_key))

                cursor.execute("DELETE FROM TeacherResearchField WHERE teacher_id=%s", (new_key, ))
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                    research_fields = [row['id'] for row in cursor.fetchall()]
                for rf_id in research_fields:
                    cursor.execute("INSERT INTO TeacherResearchField (teacher_id, research_field) VALUES (%s, %s)", (new_key, rf_id))
                response_data['record'] = {'teacher_id': new_key}

            elif table == 'project':
                new_key = record_data.get('project_id')
                if new_key != old_key:
                    cursor.execute("SELECT 1 FROM Project WHERE project_id=%s", (new_key, ))
                    if cursor.fetchone():
                        return api_response(False, '项目编号已存在', {'type': 'duplicate'}, 409)

                # 校验是否存在
                cursor.execute("SELECT project_approval_status, project_acceptance_status FROM Project WHERE project_id=%s", (old_key, ))
                row = cursor.fetchone()
                if not row:
                    return api_response(False, '项目不存在', status=400)

                # 权限限制：审批通过或验收通过仅 Admin 可编辑
                if (row['project_approval_status'] == '审批通过' or row['project_acceptance_status'] == '验收通过') and role != 'Admin':
                    return api_response(False, '项目已审批或验收，仅管理员可编辑', status=403)

                # 权限限制：学生需为负责人，教师需为指导老师
                if role == 'Student':
                    cursor.execute("SELECT 1 FROM StudentProject WHERE project_id=%s AND student_id=%s AND role='负责人'", (old_key, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '您无权编辑该项目（不是负责人）', status=403)
                elif role == 'Teacher':
                    cursor.execute("SELECT 1 FROM TeacherProject WHERE project_id=%s AND teacher_id=%s", (old_key, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '您无权编辑该项目（不是指导教师）', status=403)

                # 校验负责人和指导老师不能为空
                leader_id = record_data.get('负责人学号', '').strip()
                teacher_ids = [tid.strip() for tid in record_data.get('指导教师工号', '').split('、') if tid.strip()]
                if not leader_id or not teacher_ids:
                    return api_response(False, '负责人和指导老师不能为空', status=400)

                # 更新主表
                cursor.execute("UPDATE Project SET project_id=%s, name=%s, project_content=%s WHERE project_id=%s",
                               (new_key, record_data.get('name', ''), record_data.get('project_content', ''), old_key))

                # 更新研究领域
                cursor.execute("DELETE FROM ProjectResearchField WHERE project_id=%s", (new_key, ))
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                    research_fields = [row['id'] for row in cursor.fetchall()]
                for rf_id in research_fields:
                    cursor.execute("INSERT INTO ProjectResearchField (project_id, research_field) VALUES (%s, %s)", (new_key, rf_id))

                # 更新参与人员关系
                cursor.execute("DELETE FROM StudentProject WHERE project_id=%s", (new_key, ))
                cursor.execute("DELETE FROM TeacherProject WHERE project_id=%s", (new_key, ))

                # 插入负责人
                cursor.execute("INSERT INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '负责人')", (leader_id, new_key))

                # 插入成员
                member_ids = [mid.strip() for mid in record_data.get('成员学号', '').split('、') if mid.strip()]
                for mid in member_ids:
                    cursor.execute("INSERT INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '成员')", (mid, new_key))

                # 插入指导教师
                for tid in teacher_ids:
                    cursor.execute("INSERT INTO TeacherProject (teacher_id, project_id) VALUES (%s, %s)", (tid, new_key))

                response_data['record'] = {'project_id': new_key}

            else:
                return api_response(False, '不支持的表名', status=400)

            connection.commit()
            return api_response(True, '更新成功', response_data)

        except Exception as e:
            connection.rollback()
            return api_response(False, f'服务器错误：{str(e)}', status=500)
        finally:
            cursor.close()
            connection.close()


@ns.route('/delete')
class DeleteData(Resource):

    @ns.expect(delete_parser)
    @ns.response(200, '删除成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(403, '权限不足')
    @ns.response(500, '删除失败')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """删除数据（含权限校验、状态判断、级联删除）"""
        user = request.user
        user_id = user['username']
        role = user['role']

        args = delete_parser.parse_args()
        table = args['table'].lower()
        key = args['key']

        if not all([table, key]):
            return api_response(False, '缺少必要参数', status=400)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            if table == 'project':
                # 查询审批状态
                cursor.execute("SELECT project_approval_status, project_acceptance_status FROM Project WHERE project_id=%s", (key, ))
                row = cursor.fetchone()
                if not row:
                    return api_response(False, '项目不存在', status=400)

                approval_status = row['project_approval_status']
                acceptance_status = row['project_acceptance_status']

                # 已审批/验收项目仅 Admin 可删
                if (approval_status == '审批通过' or acceptance_status == '验收通过') and role != 'Admin':
                    return api_response(False, '项目已审批或验收，仅管理员可删除', status=403)

                # 权限校验
                if role == 'Student':
                    cursor.execute("SELECT 1 FROM StudentProject WHERE project_id=%s AND student_id=%s AND role='负责人'", (key, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '无权删除该项目（不是负责人）', status=403)
                elif role == 'Teacher':
                    cursor.execute("SELECT 1 FROM TeacherProject WHERE project_id=%s AND teacher_id=%s", (key, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '无权删除该项目（不是指导老师）', status=403)

                # 删除项目关联信息（顺序：先删关联，再删主表）
                cursor.execute("DELETE FROM ProjectResearchField WHERE project_id=%s", (key, ))
                cursor.execute("DELETE FROM StudentProject WHERE project_id=%s", (key, ))
                cursor.execute("DELETE FROM TeacherProject WHERE project_id=%s", (key, ))
                cursor.execute("DELETE FROM Project WHERE project_id=%s", (key, ))

            elif table == 'student':
                if role != 'Admin':
                    return api_response(False, '仅管理员可删除学生信息', status=403)

                # 先删除关联信息
                cursor.execute("DELETE FROM StudentProject WHERE student_id=%s", (key, ))
                cursor.execute("DELETE FROM StudentResearchField WHERE student_id=%s", (key, ))
                cursor.execute("DELETE FROM Student WHERE student_id=%s", (key, ))

            elif table == 'teacher':
                if role != 'Admin':
                    return api_response(False, '仅管理员可删除教师信息', status=403)

                # 先删除关联信息
                cursor.execute("DELETE FROM TeacherProject WHERE teacher_id=%s", (key, ))
                cursor.execute("DELETE FROM TeacherResearchField WHERE teacher_id=%s", (key, ))
                cursor.execute("DELETE FROM Teacher WHERE teacher_id=%s", (key, ))

            else:
                return api_response(False, '不支持的表名', status=400)

            connection.commit()
            return api_response(True, '删除成功', {'table': table, 'deleted_key': key})

        except Exception as e:
            connection.rollback()
            return api_response(False, f'删除失败：{str(e)}', status=500)
        finally:
            cursor.close()
            connection.close()
