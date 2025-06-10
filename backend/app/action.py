from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from app.database import get_db_connection
from app.utils import auth_required

action_bp = Blueprint('action_bp', __name__)
ns = Namespace('action', description='科研项目申报、审批、验收接口')


def api_response(success, message, data=None, status=200):
    return {'success': success, 'message': message, 'data': data}, status


# 请求模型
action_model = ns.model(
    'Action', {
        'project_name': fields.String(required=True, description='项目名称'),
        'industry_chain': fields.String(required=True, description='所属产业链'),
        'action': fields.String(required=True, enum=['申报', '审批', '验收'], description='操作类型')
    })


@ns.route('/submit')
class Action(Resource):

    @ns.expect(action_model)
    @auth_required(roles=['Admin', 'Teacher', 'Student'])
    def post(self):
        data = request.get_json()
        project_name = data.get('project_name')
        industry_chain = data.get('industry_chain')
        action = data.get('action')

        if not all([project_name, industry_chain, action]):
            return api_response(False, '缺少参数', status=400)

        # 获取当前用户角色
        user_role = getattr(request, 'user', {}).get('role', None)

        # 权限细粒度校验
        if action == '申报' and user_role not in ['Admin', 'Teacher', 'Student']:
            return api_response(False, '无权限申报项目', status=403)
        elif action == '审批' and user_role not in ['Admin', 'Teacher']:
            return api_response(False, '无权限审批项目', status=403)
        elif action == '验收' and user_role != 'Admin':
            return api_response(False, '无权限验收项目', status=403)

        field_map = {'申报': 'project_application_status', '审批': 'project_approval_status', '验收': 'project_acceptance_status'}
        field = field_map.get(action)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(f"""
                UPDATE Project SET {field} = %s
                WHERE project_name = %s AND industry_chain = %s
            """, (action, project_name, industry_chain))

            if cursor.rowcount == 0:
                return api_response(False, '未找到对应项目', status=404)

            connection.commit()
            return api_response(True, f'{action}操作成功')

        except Exception as e:
            connection.rollback()
            return api_response(False, f'数据库错误: {str(e)}', status=500)

        finally:
            cursor.close()
            connection.close()
