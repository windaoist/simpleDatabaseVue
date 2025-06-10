from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from app.database import get_db_connection
import jwt
import datetime
import os

auth_bp = Blueprint('auth_bp', __name__)
ns = Namespace('auth', description='用户登录接口')

SECRET_KEY = os.environ.get("JWT_SECRET", "my_jwt_secret")


def api_response(success, message, data=None, status=200):
    return {'success': success, 'message': message, 'data': data}, status


def generate_token(username, role):
    payload = {'username': username, 'role': role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


login_model = ns.model(
    'LoginRequest', {
        'username': fields.String(required=True, description='用户名'),
        'password': fields.String(required=True, description='密码'),
        'role': fields.String(required=True, enum=['Admin', 'Teacher', 'Student'], description='用户角色')
    })


@ns.route('/login')
class Login(Resource):

    @ns.expect(login_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return api_response(False, '缺少参数', status=400)

        try:
            # Admin 登录
            if role == 'Admin':
                if username == 'Admin' and password == 'Admin':
                    token = generate_token(username, role)
                    return api_response(True, '登录成功', {'token': token, 'username': username, 'role': role})
                else:
                    return api_response(False, '管理员账号或密码错误', status=401)

            connection = get_db_connection()
            cursor = connection.cursor()

            # 教职工（专家表）
            if role == 'Teacher':
                cursor.execute("SELECT * FROM Expert WHERE expert_name = %s", (username, ))
                user = cursor.fetchone()
                if not user:
                    return api_response(False, '教职工账号不存在', status=404)
                if password != username:
                    return api_response(False, '密码错误', status=401)

            # 学生（基金表）
            elif role == 'Student':
                cursor.execute("SELECT * FROM Fund WHERE fund_name = %s", (username, ))
                user = cursor.fetchone()
                if not user:
                    return api_response(False, '学生账号不存在', status=404)
                if password != username:
                    return api_response(False, '密码错误', status=401)

            else:
                return api_response(False, '无效的用户角色', status=400)

            token = generate_token(username, role)
            return api_response(True, '登录成功', {'token': token, 'username': username, 'role': role})

        except Exception as e:
            return api_response(False, f'服务器错误: {str(e)}', status=500)
        finally:
            if role != 'Admin':
                cursor.close()
                connection.close()
