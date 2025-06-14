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

# 状态模型
mark_status_model = ns.model(
    'MarkStatusRequest', {
        'project_id': fields.String(required=True, description='项目编号'),
        'action': fields.String(required=True, enum=['application', 'approval', 'acceptance'], description='操作类型')
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

                # 添加用户记录（默认密码为学号）
                cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, 'Student')",
                               (record_data['student_id'], record_data['student_id']))

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

                # 添加用户记录（默认密码为工号）
                cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, 'Teacher')",
                               (record_data['teacher_id'], record_data['teacher_id']))

                response_data['record'] = {'teacher_id': record_data['teacher_id']}

            elif table == 'project':
                if role != 'Student':
                    return api_response(False, '仅学生可添加科研项目信息', status=403)

                # 判断学生是否已是某项目负责人
                cursor.execute("SELECT COUNT(*) FROM StudentProject WHERE student_id=%s AND role='负责人'", (user_id, ))
                count = cursor.fetchone()
                if count['COUNT(*)'] >= 1:
                    return api_response(False, '您已作为负责人参与一个项目，不能再次创建', status=409)

                required_fields = ['project_id', 'project_name']
                if not all(record_data.get(field) and str(record_data.get(field)).strip() for field in required_fields):
                    return api_response(False, '存在必要字段为空', status=400)

                project_id = record_data['project_id']
                cursor.execute("SELECT 1 FROM Project WHERE project_id=%s", (project_id, ))
                if cursor.fetchone():
                    return api_response(False, '项目已存在', {'type': 'duplicate'}, 409)

                # 当前用户就是负责人，不能传 leader 字段
                student_leader_id = user_id

                # 获取成员与教师 ID
                member_ids = [s.strip() for s in record_data.get('member', '').split('、') if s.strip()]
                teacher_ids = [t.strip() for t in record_data.get('teacher', '').split('、') if t.strip()]

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
                cursor.execute("INSERT INTO Project (project_id, project_name, project_content) "
                               "VALUES (%s, %s, %s)", (project_id, record_data['project_name'], record_data['project_content']))

                # 插入研究领域
                field_str = record_data.get('research_field', '')
                research_fields = [int(fid) for fid in field_str.split('、') if fid.isdigit()]
                for fid in research_fields:
                    cursor.execute("INSERT IGNORE INTO ProjectResearchField (project_id, research_field) VALUES (%s, %s)", (project_id, fid))

                # 插入负责人（当前用户）
                cursor.execute("SELECT name FROM Student WHERE student_id=%s", (student_leader_id, ))
                student_row = cursor.fetchone()
                if student_row:
                    cursor.execute("INSERT INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '负责人')", (student_leader_id, project_id))

                # 插入成员
                for sid in member_ids:
                    cursor.execute("SELECT name FROM Student WHERE student_id=%s", (sid, ))
                    name_row = cursor.fetchone()
                    if name_row:
                        cursor.execute("INSERT INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '成员')", (sid, project_id))

                # 插入教师
                for tid in teacher_ids:
                    cursor.execute("SELECT name FROM Teacher WHERE teacher_id=%s", (tid, ))
                    name_row = cursor.fetchone()
                    if name_row:
                        cursor.execute("INSERT INTO TeacherProject (teacher_id, project_id) VALUES (%s, %s)", (tid, project_id))

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
        ns.model('EditRequest', {
            'table': fields.String(required=True, enum=['Student', 'Teacher', 'Project'], description='表名'),
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
        record_data = data.get('data', {})

        if not table:
            return api_response(False, '缺少必要参数', status=400)

        connection = get_db_connection()
        cursor = connection.cursor()
        response_data = {'table': table}

        try:
            if table == 'student':
                target_id = record_data.get('student_id')  # 正在被修改的学生ID
                if not target_id:
                    return api_response(False, '缺少学生学号', status=400)

                if role == 'Admin':
                    pass  # 管理员可修改任何学生信息
                elif role == 'Student':
                    if target_id != user_id:
                        return api_response(False, '您无权修改其他学生的信息', status=403)
                else:
                    return api_response(False, '无权限修改学生信息', status=403)

                student_id = record_data.get('student_id')
                if not student_id:
                    return api_response(False, '学生学号不能为空', status=400)

                # 检查学生是否存在
                cursor.execute("SELECT 1 FROM Student WHERE student_id=%s", (student_id, ))
                if not cursor.fetchone():
                    return api_response(False, '该学生不存在，无法修改', status=404)

                # 更新主表字段
                cursor.execute(
                    """
                    UPDATE Student SET
                        name=%s, gender=%s, grade=%s,
                        major=%s, class=%s, phone=%s, email=%s
                    WHERE student_id=%s
                """, (record_data.get('name', ''), record_data.get('gender', ''), record_data.get('grade', ''), record_data.get(
                        'major', ''), record_data.get('class', ''), record_data.get('phone', ''), record_data.get('email', ''), student_id))

                # 获取旧研究领域
                cursor.execute("SELECT research_field FROM StudentResearchField WHERE student_id=%s", (student_id, ))
                old_fields = set(row['research_field'] for row in cursor.fetchall())

                # 解析新研究领域
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    if research_fields:
                        cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                        research_fields = [row['id'] for row in cursor.fetchall()]
                new_fields = set(research_fields)

                # 仅当研究领域有变动时才更新
                if new_fields != old_fields:
                    cursor.execute("DELETE FROM StudentResearchField WHERE student_id=%s", (student_id, ))
                    for rf_id in new_fields:
                        cursor.execute("INSERT INTO StudentResearchField (student_id, research_field) VALUES (%s, %s)", (student_id, rf_id))

                response_data['record'] = {'student_id': student_id}

            elif table == 'teacher':
                target_id = record_data.get('teacher_id')  # 正在被修改的教职工ID
                if not target_id:
                    return api_response(False, '缺少教职工号', status=400)

                if role == 'Admin':
                    pass  # 管理员可修改任何教职工信息
                elif role == 'Teacher':
                    if target_id != user_id:
                        return api_response(False, '您无权修改其他教职工的信息', status=403)
                else:
                    return api_response(False, '无权限修改教职工信息', status=403)

                teacher_id = record_data.get('teacher_id')
                if not teacher_id:
                    return api_response(False, '教职工号不能为空', status=400)

                # 校验主键是否存在
                cursor.execute("SELECT 1 FROM Teacher WHERE teacher_id=%s", (teacher_id, ))
                if not cursor.fetchone():
                    return api_response(False, '该教职工不存在，无法修改', status=404)

                # 更新主表字段
                cursor.execute(
                    """
                    UPDATE Teacher SET
                        name=%s, gender=%s, title=%s,
                        college=%s, department=%s, phone=%s, email=%s,
                        office_location=%s, introduction=%s
                    WHERE teacher_id=%s
                """, (record_data.get('name', ''), record_data.get('gender', ''), record_data.get('title', ''), record_data.get(
                        'college', ''), record_data.get('department', ''), record_data.get('phone', ''), record_data.get(
                            'email', ''), record_data.get('office_location', ''), record_data.get('introduction', ''), teacher_id))

                # 获取旧研究领域
                cursor.execute("SELECT research_field FROM TeacherResearchField WHERE teacher_id=%s", (teacher_id, ))
                old_fields = set(row['research_field'] for row in cursor.fetchall())

                # 解析新研究领域
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    if research_fields:
                        cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                        research_fields = [row['id'] for row in cursor.fetchall()]
                new_fields = set(research_fields)

                # 如果研究领域有变化，则更新
                if new_fields != old_fields:
                    cursor.execute("DELETE FROM TeacherResearchField WHERE teacher_id=%s", (teacher_id, ))
                    for rf_id in new_fields:
                        cursor.execute("INSERT INTO TeacherResearchField (teacher_id, research_field) VALUES (%s, %s)", (teacher_id, rf_id))

                response_data['record'] = {'teacher_id': teacher_id}

            elif table == 'project':
                # 获取项目主键
                project_id = record_data.get('project_id')
                if not project_id:
                    return api_response(False, '项目编号不能为空', status=400)

                # 查询三项状态字段
                cursor.execute(
                    """
                    SELECT project_application_status, project_approval_status, project_acceptance_status
                    FROM Project
                    WHERE project_id = %s
                    """, (project_id, ))
                row = cursor.fetchone()
                if not row:
                    return api_response(False, '项目不存在', status=404)

                app_status = row['project_application_status']
                aprv_status = row['project_approval_status']
                accp_status = row['project_acceptance_status']

                # 状态约束判断
                if accp_status == '验收通过':
                    return api_response(False, '项目已验收通过，禁止编辑', status=403)

                if app_status == '未申报':
                    if role != 'Student':
                        return api_response(False, '仅负责人可编辑未申报项目', status=403)
                    cursor.execute("SELECT 1 FROM StudentProject WHERE project_id=%s AND student_id=%s AND role='负责人'", (project_id, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '您无权编辑该项目（不是负责人）', status=403)

                elif app_status == '申报通过' and aprv_status == '未审批':
                    if role != 'Teacher':
                        return api_response(False, '仅指导教师可编辑该项目', status=403)
                    cursor.execute("SELECT 1 FROM TeacherProject WHERE project_id=%s AND teacher_id=%s", (project_id, user_id))
                    if not cursor.fetchone():
                        return api_response(False, '您无权编辑该项目（不是指导教师）', status=403)

                elif aprv_status == '审批通过' and accp_status == '未验收':
                    if role != 'Admin':
                        return api_response(False, '仅管理员可编辑该项目', status=403)

                else:
                    if role != 'Admin':
                        return api_response(False, '当前状态禁止编辑', status=403)

                # 更新主表字段（project_id 不再允许修改）
                cursor.execute(
                    """
                    UPDATE Project SET
                        project_name=%s,
                        project_content=%s
                    WHERE project_id=%s
                    """, (record_data.get('project_name', ''), record_data.get('project_content', ''), project_id))

                # 获取旧研究领域
                cursor.execute("SELECT research_field FROM ProjectResearchField WHERE project_id=%s", (project_id, ))
                old_fields = set(row['research_field'] for row in cursor.fetchall())

                # 新研究领域解析
                research_fields = record_data.get('research_field', [])
                if isinstance(research_fields, str):
                    research_fields = [rf.strip() for rf in research_fields.split('、') if rf.strip()]
                    if research_fields:
                        cursor.execute("SELECT id FROM ResearchFields WHERE research_field IN %s", (tuple(research_fields), ))
                        research_fields = [row['id'] for row in cursor.fetchall()]
                new_fields = set(research_fields)

                # 研究领域发生变更，才更新
                if new_fields != old_fields:
                    cursor.execute("DELETE FROM ProjectResearchField WHERE project_id=%s", (project_id, ))
                    for rf_id in new_fields:
                        cursor.execute("INSERT INTO ProjectResearchField (project_id, research_field) VALUES (%s, %s)", (project_id, rf_id))

                response_data['record'] = {'project_id': project_id}

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

                # 同时删除 Users 表中对应记录
                cursor.execute("DELETE FROM Users WHERE username=%s AND role='Student'", (key, ))

            elif table == 'teacher':
                if role != 'Admin':
                    return api_response(False, '仅管理员可删除教师信息', status=403)

                # 先删除关联信息
                cursor.execute("DELETE FROM TeacherProject WHERE teacher_id=%s", (key, ))
                cursor.execute("DELETE FROM TeacherResearchField WHERE teacher_id=%s", (key, ))
                cursor.execute("DELETE FROM Teacher WHERE teacher_id=%s", (key, ))

                # 同时删除 Users 表中对应记录
                cursor.execute("DELETE FROM Users WHERE username=%s AND role='Teacher'", (key, ))

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


@ns.route('/mark-status')
class ProjectMarkStatus(Resource):

    @ns.expect(ns.model('MarkStatusRequest', {'project_id': fields.String(required=True, description='项目编号')}))
    @ns.response(200, '状态更新成功')
    @ns.response(400, '请求参数错误')
    @ns.response(403, '权限不足或条件不符')
    @ns.response(404, '项目或用户不存在')
    @ns.response(500, '数据库错误')
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        """点击一次自动判断当前用户权限与项目状态，完成状态推进"""
        user = request.user
        username = user['username']
        role = user['role']

        data = request.get_json()
        project_id = data.get('project_id')
        if not project_id:
            return api_response(False, '缺少项目编号', status=400)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 查询项目当前三项状态
            cursor.execute(
                """
                SELECT project_application_status, project_approval_status, project_acceptance_status
                FROM Project WHERE project_id = %s
            """, (project_id, ))
            project = cursor.fetchone()
            if not project:
                return api_response(False, '项目不存在', status=404)

            app_status = project['project_application_status']
            aprv_status = project['project_approval_status']
            accp_status = project['project_acceptance_status']

            # 获取用户姓名
            if role == 'Student':
                cursor.execute("SELECT name FROM Student WHERE student_id = %s", (username, ))
                row = cursor.fetchone()
                if not row:
                    return api_response(False, '学生用户不存在', status=404)
                full_role = f"学生{row['name']}"

                # 学生只能进行“申报”操作
                if app_status == '未申报':
                    cursor.execute(
                        """
                        SELECT 1 FROM StudentProject WHERE student_id = %s AND project_id = %s AND role = '负责人'
                    """, (username, project_id))
                    if not cursor.fetchone():
                        return api_response(False, '无权申报该项目（非负责人）', status=403)

                    cursor.execute("SET @current_user = %s", (username, ))
                    cursor.execute("SET @current_role = %s", (full_role, ))
                    cursor.execute("UPDATE Project SET project_application_status = 'TRIGGER_PENDING' WHERE project_id = %s", (project_id, ))
                    conn.commit()
                    return api_response(True, '申报通过')

                else:
                    return api_response(False, '学生仅能在未申报状态执行操作', status=403)

            elif role == 'Teacher':
                cursor.execute("SELECT name FROM Teacher WHERE teacher_id = %s", (username, ))
                row = cursor.fetchone()
                if not row:
                    return api_response(False, '教职工用户不存在', status=404)
                full_role = f"教职工{row['name']}"

                # 教师只能进行“审批”操作
                if '申报通过' in app_status and aprv_status == '未审批':
                    cursor.execute("""
                        SELECT 1 FROM TeacherProject WHERE teacher_id = %s AND project_id = %s
                    """, (username, project_id))
                    if not cursor.fetchone():
                        return api_response(False, '无权审批该项目（非指导教师）', status=403)

                    cursor.execute("SET @current_user = %s", (username, ))
                    cursor.execute("SET @current_role = %s", (full_role, ))
                    cursor.execute("UPDATE Project SET project_approval_status = 'TRIGGER_PENDING' WHERE project_id = %s", (project_id, ))
                    conn.commit()
                    return api_response(True, '审批通过')

                else:
                    return api_response(False, '教职工仅能在申报通过且未审批状态执行操作', status=403)

            elif role == 'Admin':
                # 管理员只能执行验收
                if '审批通过' in aprv_status and accp_status == '未验收':
                    full_role = f"管理员{username}"
                    cursor.execute("SET @current_user = %s", (username, ))
                    cursor.execute("SET @current_role = %s", (full_role, ))
                    cursor.execute("UPDATE Project SET project_acceptance_status = 'TRIGGER_PENDING' WHERE project_id = %s", (project_id, ))
                    conn.commit()
                    return api_response(True, '验收通过')
                else:
                    return api_response(False, '管理员仅能在审批通过且未验收状态操作', status=403)

            else:
                return api_response(False, '无权限角色', status=403)

        except Exception as e:
            conn.rollback()
            return api_response(False, f'更新失败：{str(e)}', status=500)
        finally:
            cursor.close()
            conn.close()
