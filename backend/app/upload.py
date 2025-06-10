from flask import Blueprint, request
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from app.utils import COLUMN_MAPPING, auth_required
from app.database import get_db_connection
import pandas as pd

# 创建蓝图和API实例
upload_bp = Blueprint('upload', __name__)
api = Api(upload_bp, version='1.0', title='Upload API', description='文件上传相关API')

# 创建命名空间
ns = Namespace('upload', description='文件上传操作')
api.add_namespace(ns)

# 定义响应模型
upload_response = ns.model(
    'UploadResponse', {
        'code': fields.Integer(description='状态码'),
        'message': fields.String(description='消息内容'),
        'duplicates': fields.List(fields.String, description='重复数据列表', default=[])
    })

# 文件上传解析器
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Excel文件')


@ns.route('/')
class UploadResource(Resource):

    @ns.expect(upload_parser)
    @ns.marshal_with(upload_response)
    @auth_required(roles=['Admin'])
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']

        if not file.filename.endswith('.xlsx'):
            return {'code': 400, 'message': '文件格式不正确，请上传 Excel 文件 (.xlsx)'}

        try:
            if '学生库' in file.filename:
                result = import_student_data(file)
            elif '教职工库' in file.filename:
                result = import_teacher_data(file)
            elif '科研项目库' in file.filename:
                result = import_project_data(file)
            else:
                return {'code': 400, 'message': '未知文件类型'}

            return {'code': 200, 'message': result['message'], 'duplicates': result.get('duplicates', [])}
        except Exception as e:
            return {'code': 500, 'message': f'上传过程中发生错误: {str(e)}'}


# 导入学生表
def import_student_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = ['序号', '学生学号', '姓名', '性别', '年级', '专业', '班级', '研究方向', '联系电话', '电子邮箱']
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    connection = get_db_connection()
    cursor = connection.cursor()

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE StudentProject")
    cursor.execute("TRUNCATE TABLE StudentResearchField")
    cursor.execute("TRUNCATE TABLE Student")

    duplicates = set()
    inserted_count = 0

    for _, row in df.iterrows():
        try:
            student_id = row['student_id']

            cursor.execute("SELECT * FROM Student WHERE student_id=%s", (student_id, ))
            if cursor.fetchone():
                duplicates.add(f"重复学生学号: {student_id}")
                continue

            cursor.execute("INSERT INTO Student (student_id, name, gender, grade, major, class, phone, email) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (student_id, row['name'], row['gender'], row['grade'], row['major'], row['class'], row['phone'], row['email']))
            inserted_count += 1

            # 处理研究方向（多对多插入）
            field_names = row['research_field'].split('、') if row['research_field'] else []
            for fname in field_names:
                fname = fname.strip()
                if not fname:
                    continue
                # 查询 ID
                cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (fname, ))
                res = cursor.fetchone()
                if not res:
                    duplicates.add(f"无效研究领域: {fname}（学生 {student_id}）")
                    continue
                field_id = res['id']
                # 插入中间表
                cursor.execute("INSERT IGNORE INTO StudentResearchField (student_id, field_id) VALUES (%s, %s)", (student_id, field_id))

        except Exception as e:
            duplicates.add(f"插入失败: {student_id}，错误: {str(e)}")
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f'成功导入 {inserted_count} 条学生数据'
    if duplicates:
        message += f', 跳过 {len(duplicates)} 条重复或异常数据'

    return {'message': message, 'duplicates': list(duplicates)}


# 导入教职工表
def import_teacher_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = ['序号', '教职工号', '姓名', '性别', '职称', '所属学院', '所属专业', '研究领域', '联系电话', '电子邮箱', '办公地点', '个人简介']
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    connection = get_db_connection()
    cursor = connection.cursor()

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE TeacherProject")
    cursor.execute("TRUNCATE TABLE TeacherResearchField")
    cursor.execute("TRUNCATE TABLE Teacher")

    duplicates = set()
    inserted_count = 0

    for _, row in df.iterrows():
        try:
            teacher_id = row['teacher_id']

            cursor.execute("SELECT * FROM Teacher WHERE teacher_id=%s", (teacher_id, ))
            if cursor.fetchone():
                duplicates.add(f"重复教职工号: {teacher_id}")
                continue

            cursor.execute(
                "INSERT INTO Teacher (teacher_id, name, gender, title, college, department, phone, email, office_location, introduction) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (teacher_id, row['name'], row['gender'], row['title'], row['college'], row['department'],
                                                                        row['phone'], row['email'], row['office_location'], row['introduction']))
            inserted_count += 1

            # 处理研究方向（多对多插入）
            field_names = row['research_field'].split('、') if row['research_field'] else []
            for fname in field_names:
                fname = fname.strip()
                if not fname:
                    continue
                # 查询 ID
                cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (fname, ))
                res = cursor.fetchone()
                if not res:
                    duplicates.add(f"无效研究领域: {fname}（教师 {teacher_id}）")
                    continue
                field_id = res['id']
                # 插入中间表
                cursor.execute("INSERT IGNORE INTO TeacherResearchField (teacher_id, field_id) VALUES (%s, %s)", (teacher_id, field_id))

        except Exception as e:
            duplicates.add(f"插入失败: {teacher_id}，错误: {str(e)}")
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f"成功导入 {inserted_count} 条教职工数据"
    if duplicates:
        message += f"，跳过 {len(duplicates)} 条重复或异常数据"

    return {'message': message, 'duplicates': list(duplicates)}


# 导入科研项目表
def import_project_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = ['序号', '项目编号', '项目名称', '研究领域', '负责人学号', '成员学号', '指导教师工号', '项目内容']
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    connection = get_db_connection()
    cursor = connection.cursor()

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE StudentProject")
    cursor.execute("TRUNCATE TABLE TeacherProject")
    cursor.execute("TRUNCATE TABLE ProjectResearchField")
    cursor.execute("TRUNCATE TABLE Project")

    duplicates = set()
    inserted_count = 0

    for _, row in df.iterrows():
        try:
            project_id = row['project_id']

            cursor.execute("SELECT * FROM Project WHERE project_id=%s", (project_id, ))
            if cursor.fetchone():
                duplicates.add(f"重复项目编号: {project_id}")
                continue

            cursor.execute(
                "INSERT INTO Project (project_id, name, project_content, project_application_status, project_approval_status, project_acceptance_status) "
                "VALUES (%s, %s, %s, %s, %s, %s)", (project_id, row['name'], row['project_content'], row['project_application_status'],
                                                    row['project_approval_status'], row['project_acceptance_status']))
            inserted_count += 1

            # 处理研究方向（多对多插入）
            field_names = row['research_field'].split('、') if row['research_field'] else []
            for fname in field_names:
                fname = fname.strip()
                if not fname:
                    continue
                # 查询 ID
                cursor.execute("SELECT id FROM ResearchFields WHERE research_field = %s", (fname, ))
                res = cursor.fetchone()
                if not res:
                    duplicates.add(f"无效研究领域: {fname}（项目 {project_id}）")
                    continue
                field_id = res['id']
                # 插入中间表
                cursor.execute("INSERT IGNORE INTO ProjectResearchField (project_id, field_id) VALUES (%s, %s)", (project_id, field_id))

            # 插入负责人（学生，最多1个）
            leader_ids = [s.strip() for s in row.get('负责人学号', '').split('、') if s.strip()]
            if leader_ids:
                student_id = leader_ids[0]  # 只取第一个
                cursor.execute("SELECT 1 FROM Student WHERE student_id = %s", (student_id, ))
                if cursor.fetchone():
                    cursor.execute("INSERT IGNORE INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '负责人')", (student_id, project_id))

            # 插入成员（学生，最多4个）
            member_ids = [s.strip() for s in row.get('成员学号', '').split('、') if s.strip()]
            for student_id in member_ids[:4]:  # 最多取前4个
                cursor.execute("SELECT 1 FROM Student WHERE student_id = %s", (student_id, ))
                if cursor.fetchone():
                    cursor.execute("INSERT IGNORE INTO StudentProject (student_id, project_id, role) VALUES (%s, %s, '成员')", (student_id, project_id))

            # 插入指导教师（最多2个）
            teacher_ids = [t.strip() for t in row.get('指导教师工号', '').split('、') if t.strip()]
            for teacher_id in teacher_ids[:2]:  # 最多取前2个
                cursor.execute("SELECT 1 FROM Teacher WHERE teacher_id = %s", (teacher_id, ))
                if cursor.fetchone():
                    cursor.execute("INSERT IGNORE INTO TeacherProject (teacher_id, project_id) VALUES (%s, %s)", (teacher_id, project_id))

        except Exception as e:
            duplicates.add(f"插入失败: {project_id}，错误: {str(e)}")
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f'成功导入 {inserted_count} 条科研项目数据'
    if duplicates:
        message += f', 跳过 {len(duplicates)} 条重复或异常数据'

    return {'message': message, 'duplicates': list(duplicates)}
