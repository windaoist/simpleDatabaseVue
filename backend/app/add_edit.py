from flask import Blueprint, request
from flask_restx import Resource, fields, Namespace, reqparse
from app.utils import get_industry_id, get_industries
from app.database import get_db_connection

# 创建蓝图和 API 实例
add_edit_bp = Blueprint('add_edit', __name__)
# api = Api(
#     add_edit_bp,
#     title='数据管理 API',
#     version='1.0',
#     description='用于添加、编辑和删除专家、项目和基金数据的API',
#     doc='/swagger/'  # Swagger UI 访问路径
# )

# 创建命名空间
ns = Namespace('data', path='/', description='数据操作接口')

# 请求模型定义
expert_model = ns.model('Expert', {
    'expert_name': fields.String(required=True, description='专家姓名'),
    'industry_category': fields.String(required=True, description='行业类别'),
    'specific_industry': fields.String(required=True, description='具体行业'),
    'fund_name': fields.String(required=True, description='基金名称'),
    'agency_name': fields.String(required=True, description='机构名称')
})

project_model = ns.model('Project', {
    'project_name': fields.String(required=True, description='项目名称'),
    'project_status': fields.String(required=True, description='项目状态'),
    'industry_chain': fields.String(required=True, description='产业链'),
    'project_content': fields.String(required=True, description='项目内容'),
    'investor': fields.String(description='投资者'),
    'investment_amount': fields.Float(description='投资金额'),
    'financing_amount': fields.Float(description='融资总额'),
    'equity_financing': fields.Float(description='股权融资'),
    'debt_financing': fields.Float(description='债权融资'),
    'project_progress': fields.String(description='项目进展'),
    'location': fields.String(description='所在地'),
    'contact_person': fields.String(description='联系人'),
    'contact_phone': fields.String(description='联系电话')
})

fund_model = ns.model('Fund', {
    'fund_name': fields.String(required=True, description='基金名称'),
    'management_agency': fields.String(required=True, description='管理机构'),
    'investment_area': fields.String(required=True, description='投资领域'),
    'contact_person': fields.String(required=True, description='联系人'),
    'phone': fields.String(required=True, description='联系电话'),
    'fundraising_amount': fields.Float(description='募资总额'),
    'total_investment': fields.Float(description='总投资额')
})

# 删除操作解析器
delete_parser = reqparse.RequestParser()
delete_parser.add_argument(
    'table', type=str, required=True, help='表名', location='json')
delete_parser.add_argument(
    'key1', type=str, required=True, help='主键1', location='json')
delete_parser.add_argument(
    'key2', type=str, required=True, help='主键2', location='json')

# 编辑操作解析器
edit_parser = reqparse.RequestParser()
edit_parser.add_argument(
    'table', type=str, required=True, help='表名', location='json')
edit_parser.add_argument('old_key1', type=str,
                         required=True, help='原主键1', location='json')
edit_parser.add_argument('old_key2', type=str,
                         required=True, help='原主键2', location='json')


def api_response(success, message, data=None, status=200):
    """统一API响应格式"""
    return {
        'success': success,
        'message': message,
        'data': data
    }, status


@ns.route('/add')
class AddData(Resource):
    @ns.expect(ns.model('AddRequest', {
        'table': fields.String(required=True, enum=['Expert', 'Project', 'Fund'], description='表名'),
        'data': fields.Raw(required=True, description='数据内容')
    }))
    @ns.response(200, '添加成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(409, '数据已存在')
    @ns.response(500, '数据库错误')
    def post(self):
        """添加新数据"""
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
            if table == 'Expert':
                required_fields = ['expert_name', 'industry_category',
                                   'specific_industry', 'fund_name', 'agency_name']
                if not all(field in record_data for field in required_fields):
                    return api_response(False, '缺少必要字段', status=400)

                # 检查重复项
                cursor.execute(
                    "SELECT * FROM Expert WHERE expert_name=%s AND specific_industry=%s",
                    (record_data['expert_name'],
                     record_data['specific_industry'])
                )
                if cursor.fetchone():
                    return api_response(False, '专家已存在', {'type': 'duplicate'}, 409)

                # 插入新专家
                cursor.execute(
                    "INSERT INTO Expert (expert_name, industry_category, specific_industry, fund_name, agency_name) VALUES (%s, %s, %s, %s, %s)",
                    (record_data['expert_name'], record_data['industry_category'],
                     record_data['specific_industry'], record_data['fund_name'], record_data['agency_name'])
                )
                response_data['record'] = {
                    'expert_name': record_data['expert_name']}

            elif table == 'Project':
                # 项目数据验证和插入逻辑
                required_fields = ['project_name', 'project_status',
                                   'industry_chain', 'project_content']
                if not all(field in record_data for field in required_fields):
                    return api_response(False, '缺少必要字段', status=400)

                # 检查重复项
                cursor.execute(
                    "SELECT * FROM Project WHERE project_name=%s AND industry_chain=%s",
                    (record_data['project_name'],
                     record_data['industry_chain'])
                )
                if cursor.fetchone():
                    return api_response(False, '项目已存在', {'type': 'duplicate'}, 409)

                # 插入新项目
                cursor.execute(
                    "INSERT INTO Project (project_name, industry_chain, project_status, project_content, investor, investment_amount, financing_amount, equity_financing, debt_financing, project_progress, location, contact_person, contact_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (record_data['project_name'], record_data['industry_chain'], record_data['project_status'], record_data['project_content'],
                     record_data.get('investor', ''), record_data.get(
                         'investment_amount', 0), record_data.get('financing_amount', 0),
                     record_data.get('equity_financing', 0), record_data.get(
                         'debt_financing', 0), record_data.get('project_progress', ''),
                     record_data.get('location', ''), record_data.get('contact_person', ''), record_data.get('contact_phone', ''))
                )
                response_data['record'] = {
                    'project_name': record_data['project_name']}

            elif table == 'Fund':
                # 基金数据验证和插入逻辑
                required_fields = ['fund_name', 'management_agency',
                                   'investment_area', 'contact_person', 'phone']
                if not all(field in record_data for field in required_fields):
                    return api_response(False, '缺少必要字段', status=400)

                # 检查重复项
                cursor.execute(
                    "SELECT * FROM Fund WHERE fund_name=%s AND investment_area=%s",
                    (record_data['fund_name'], record_data['investment_area'])
                )
                if cursor.fetchone():
                    return api_response(False, '基金已存在', {'type': 'duplicate'}, 409)

                # 插入新基金
                cursor.execute(
                    "INSERT INTO Fund (fund_name, investment_area, management_agency, contact_person, phone, fundraising_amount, total_investment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (record_data['fund_name'], record_data['investment_area'], record_data['management_agency'], record_data['contact_person'],
                     record_data['phone'], record_data.get('fundraising_amount', 0), record_data.get('total_investment', 0))
                )
                response_data['record'] = {
                    'fund_name': record_data['fund_name']}

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


@ns.route('/industries')
class IndustryData(Resource):
    @ns.response(200, '行业数据获取成功')
    @ns.response(500, '获取行业数据失败')
    def get(self):
        """获取所有行业数据"""
        try:
            industries = get_industries()
            return api_response(True, '行业数据获取成功', {'industries': industries})
        except Exception as e:
            return api_response(False, f'获取行业数据失败: {str(e)}', status=500)


@ns.route('/edit')
class EditData(Resource):
    @ns.expect(ns.model('EditRequest', {
        'table': fields.String(required=True, enum=['Expert', 'Project', 'Fund'], description='表名'),
        'old_key1': fields.String(required=True, description='原主键1'),
        'old_key2': fields.String(required=True, description='原主键2'),
        'data': fields.Raw(required=True, description='新数据内容')
    }))
    @ns.response(200, '更新成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(409, '数据已存在')
    @ns.response(500, '数据库错误')
    def post(self):
        """编辑现有数据"""
        data = request.get_json()
        if not data:
            return api_response(False, '请求数据格式错误', status=400)

        table = data.get('table')
        old_key1 = data.get('old_key1')
        old_key2 = data.get('old_key2')
        record_data = data.get('data', {})

        if not table or not old_key1 or not old_key2:
            return api_response(False, '缺少必要参数', status=400)

        connection = get_db_connection()
        cursor = connection.cursor()
        response_data = {'table': table}

        try:
            if table == 'Expert':
                # 专家数据更新逻辑
                new_key1 = record_data.get('expert_name')
                new_key2 = record_data.get('specific_industry')

                # 检查重复项（排除自身）
                if new_key1 != old_key1 or new_key2 != old_key2:
                    cursor.execute(
                        "SELECT * FROM Expert WHERE expert_name=%s AND specific_industry=%s",
                        (new_key1, new_key2)
                    )
                    if cursor.fetchone():
                        return api_response(False, '专家已存在', {'type': 'duplicate'}, 409)

                # 更新专家数据
                cursor.execute(
                    "UPDATE Expert SET expert_name=%s, specific_industry=%s, industry_category=%s, fund_name=%s, agency_name=%s WHERE expert_name=%s AND specific_industry=%s",
                    (new_key1, new_key2, record_data['industry_category'],
                     record_data['fund_name'], record_data['agency_name'], old_key1, old_key2)
                )
                response_data['record'] = {'expert_name': new_key1}

            elif table == 'Project':
                # 项目数据更新逻辑
                new_key1 = record_data.get('project_name')
                new_key2 = record_data.get('industry_chain')

                # 检查重复项（排除自身）
                if new_key1 != old_key1 or new_key2 != old_key2:
                    cursor.execute(
                        "SELECT * FROM Project WHERE project_name=%s AND industry_chain=%s",
                        (new_key1, new_key2)
                    )
                    if cursor.fetchone():
                        return api_response(False, '项目已存在', {'type': 'duplicate'}, 409)

                # 更新项目数据
                cursor.execute(
                    "UPDATE Project SET project_name=%s, industry_chain=%s, project_status=%s, project_content=%s, investor=%s, investment_amount=%s, financing_amount=%s, equity_financing=%s, debt_financing=%s, project_progress=%s, location=%s, contact_person=%s, contact_phone=%s WHERE project_name=%s AND industry_chain=%s",
                    (new_key1, new_key2, record_data['project_status'], record_data['project_content'], record_data.get('investor', ''),
                     record_data.get('investment_amount', 0), record_data.get(
                         'financing_amount', 0), record_data.get('equity_financing', 0),
                     record_data.get('debt_financing', 0), record_data.get(
                         'project_progress', ''), record_data.get('location', ''),
                     record_data.get('contact_person', ''), record_data.get('contact_phone', ''), old_key1, old_key2)
                )
                response_data['record'] = {'project_name': new_key1}

            elif table == 'Fund':
                # 基金数据更新逻辑
                new_key1 = record_data.get('fund_name')
                new_key2 = record_data.get('investment_area')

                # 检查重复项（排除自身）
                if new_key1 != old_key1 or new_key2 != old_key2:
                    cursor.execute(
                        "SELECT * FROM Fund WHERE fund_name=%s AND investment_area=%s",
                        (new_key1, new_key2)
                    )
                    if cursor.fetchone():
                        return api_response(False, '基金已存在', {'type': 'duplicate'}, 409)

                # 更新基金数据
                cursor.execute(
                    "UPDATE Fund SET fund_name=%s, investment_area=%s, management_agency=%s, contact_person=%s, phone=%s, fundraising_amount=%s, total_investment=%s WHERE fund_name=%s AND investment_area=%s",
                    (new_key1, new_key2, record_data['management_agency'], record_data['contact_person'], record_data['phone'],
                     record_data.get('fundraising_amount', 0), record_data.get('total_investment', 0), old_key1, old_key2)
                )
                response_data['record'] = {'fund_name': new_key1}

            else:
                return api_response(False, '不支持的表名', status=400)

            connection.commit()
            return api_response(True, '更新成功', response_data)

        except Exception as e:
            connection.rollback()
            return api_response(False, f'数据库错误: {str(e)}', status=500)
        finally:
            cursor.close()
            connection.close()


@ns.route('/delete')
class DeleteData(Resource):
    @ns.expect(delete_parser)
    @ns.response(200, '删除成功')
    @ns.response(400, '请求数据格式错误')
    @ns.response(500, '删除失败')
    def post(self):
        """删除数据"""
        args = delete_parser.parse_args()
        table = args['table']
        key1 = args['key1']
        key2 = args['key2']

        if not all([table, key1, key2]):
            return api_response(False, '缺少必要参数', status=400)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            if table == 'Expert':
                cursor.execute(
                    "DELETE FROM Expert WHERE expert_name=%s AND specific_industry=%s",
                    (key1, get_industry_id(key2)))
            elif table == 'Project':
                cursor.execute(
                    "DELETE FROM Project WHERE project_name=%s AND industry_chain=%s",
                    (key1, get_industry_id(key2)))
            elif table == 'Fund':
                cursor.execute(
                    "DELETE FROM Fund WHERE fund_name=%s AND investment_area=%s",
                    (key1, get_industry_id(key2)))
            else:
                return api_response(False, '不支持的表名', status=400)

            connection.commit()
            return api_response(True, '删除成功', {'table': table, 'deleted_key': [key1, key2]})

        except Exception as e:
            connection.rollback()
            return api_response(False, f'删除失败: {str(e)}', status=500)
        finally:
            cursor.close()
            connection.close()


# 将命名空间添加到API
# api.add_namespace(ns)
