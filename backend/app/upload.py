from flask import Blueprint, request
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from app.utils import COLUMN_MAPPING, get_industry_id
from app.database import get_db_connection
import pandas as pd

# 创建蓝图和API实例
upload_bp = Blueprint('upload', __name__)
api = Api(upload_bp, version='1.0',
          title='Upload API', description='文件上传相关API')

# 创建命名空间
ns = Namespace('upload', description='文件上传操作')
api.add_namespace(ns)

# 定义响应模型
upload_response = ns.model('UploadResponse', {
    'code': fields.Integer(description='状态码'),
    'message': fields.String(description='消息内容'),
    'duplicates': fields.List(fields.String, description='重复数据列表', default=[])
})

# 文件上传解析器
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True, help='Excel文件')

# 文件上传逻辑


@ns.route('/')
class UploadResource(Resource):
    @ns.expect(upload_parser)
    @ns.marshal_with(upload_response)
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']

        if not file.filename.endswith('.xlsx'):
            return {'code': 400, 'message': '文件格式不正确，请上传 Excel 文件 (.xlsx)'}

        try:
            if '专家库' in file.filename:
                result = import_expert_data(file)
            elif '项目库' in file.filename:
                result = import_project_data(file)
            elif '基金库' in file.filename:
                result = import_fund_data(file)
            else:
                return {'code': 400, 'message': '未知文件类型'}

            return {
                'code': 200,
                'message': result['message'],
                'duplicates': result.get('duplicates', [])
            }
        except Exception as e:
            return {'code': 500, 'message': f'上传过程中发生错误: {str(e)}'}


# 导入专家数据
def import_expert_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = ['序号', '专家', '具体产业', '产业类别', '基金名称', '机构名称']
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE Expert")

    duplicates = set()
    inserted_count = 0

    for index, row in df.iterrows():
        try:
            specific_industry_id = get_industry_id(
                row['specific_industry']) if row['specific_industry'] else None
            params = (row['expert_name'], specific_industry_id)

            cursor.execute(
                "SELECT * FROM Expert WHERE expert_name=%s AND specific_industry=%s", params)
            if cursor.fetchone():
                duplicates.add(
                    f"专家: {row['expert_name']}, 具体产业: {row['specific_industry']}")
                continue

            cursor.execute(
                "INSERT INTO Expert (expert_name, specific_industry, industry_category, fund_name, agency_name) VALUES (%s, %s, %s, %s, %s)",
                (row['expert_name'], specific_industry_id, row['industry_category'],
                 row['fund_name'], row['agency_name'])
            )
            inserted_count += 1
        except Exception:
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f'成功导入 {inserted_count} 条专家数据'
    if duplicates:
        message += f', 跳过 {len(duplicates)} 条重复数据'

    return {
        'message': message,
        'duplicates': list(duplicates)
    }


# 导入项目数据
def import_project_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = [
        '序号', '项目名称', '所属产业链', '项目状态', '项目内容', '投资方', '投资额', '融资额', '股权融资',
        '债权融资', '项目进展及资本对接情况', '落地区域', '联系人', '联系方式'
    ]
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE Project")

    duplicates = set()
    inserted_count = 0

    for index, row in df.iterrows():
        try:
            industry_chain_id = get_industry_id(
                row['industry_chain']) if row['industry_chain'] else None
            params = (row['project_name'], industry_chain_id)

            cursor.execute(
                "SELECT * FROM Project WHERE project_name=%s AND industry_chain=%s", params)
            if cursor.fetchone():
                duplicates.add(
                    f"项目名称: {row['project_name']}, 所属产业链: {row['industry_chain']}")
                continue

            cursor.execute(
                "INSERT INTO Project (project_name, industry_chain, project_status, project_content, investor, investment_amount, financing_amount, equity_financing, debt_financing, project_progress, location, contact_person, contact_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (row['project_name'], industry_chain_id, row['project_status'], row['project_content'],
                 row['investor'], row['investment_amount'], row['financing_amount'], row['equity_financing'],
                 row['debt_financing'], row['project_progress'], row['location'], row['contact_person'],
                 row['contact_phone'])
            )
            inserted_count += 1
        except Exception:
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f'成功导入 {inserted_count} 条项目数据'
    if duplicates:
        message += f', 跳过 {len(duplicates)} 条重复数据'

    return {
        'message': message,
        'duplicates': list(duplicates)
    }


# 导入基金数据
def import_fund_data(file):
    df = pd.read_excel(file, header=0, engine='openpyxl')
    df.columns = ['序号', '基金名称', '投资领域', '管理机构', '联系人', '电话', '募资规模', '投资总金额']
    df = df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    df = df.fillna('')

    # 处理数字字段
    df['fundraising_amount'] = pd.to_numeric(
        df['fundraising_amount'], errors='coerce').fillna(0)
    df['total_investment'] = pd.to_numeric(
        df['total_investment'], errors='coerce').fillna(0)

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE Fund")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    duplicates = set()
    inserted_count = 0

    for index, row in df.iterrows():
        try:
            investment_areas = row['investment_area'].split(
                '、') if row['investment_area'] else []

            for area in investment_areas:
                area = area.strip()
                if not area:
                    continue

                investment_area_id = get_industry_id(area)
                params = (row['fund_name'], investment_area_id)

                cursor.execute(
                    "SELECT * FROM Fund WHERE fund_name=%s AND investment_area=%s", params)
                if cursor.fetchone():
                    duplicates.add(f"基金名称: {row['fund_name']}, 投资领域: {area}")
                    continue

                cursor.execute(
                    "INSERT INTO Fund (fund_name, investment_area, management_agency, contact_person, phone, fundraising_amount, total_investment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (row['fund_name'], investment_area_id, row['management_agency'],
                     row['contact_person'], row['phone'], row['fundraising_amount'],
                     row['total_investment'])
                )
                inserted_count += 1
        except Exception:
            continue

    connection.commit()
    cursor.close()
    connection.close()

    message = f'成功导入 {inserted_count} 条基金数据'
    if duplicates:
        message += f', 跳过 {len(duplicates)} 条重复数据'

    return {
        'message': message,
        'duplicates': list(duplicates)
    }
