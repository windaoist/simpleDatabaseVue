from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from app.database import get_db_connection
import jwt
import datetime
import os
import pdb

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

change_password_model = ns.model(
    'ChangePasswordRequest', {
        'username': fields.String(required=True, description='用户名'),
        'old_password': fields.String(required=True, description='原密码'),
        'new_password': fields.String(required=True, description='新密码')
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
            connection = get_db_connection()
            cursor = connection.cursor()

            # 若不存在，添加 Admin 账号
            if role == 'Admin' and username == 'Admin':
                cursor.execute("SELECT * FROM Users WHERE username = %s AND role = %s", ('Admin', 'Admin'))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)", ('Admin', 'Admin', 'Admin'))
                    connection.commit()

            # 查询用户信息
            cursor.execute("SELECT * FROM Users WHERE username = %s AND role = %s", (username, role))
            user = cursor.fetchone()

            if not user:
                return api_response(False, '账号不存在或角色不匹配', status=404)

            if user['password'] != password:
                return api_response(False, '密码错误', status=401)

            token = generate_token(username, role)
            return api_response(True, '登录成功', {'token': token, 'username': username, 'role': role})

        except Exception as e:
            return api_response(False, f'服务器错误: {str(e)}', status=500)

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


@ns.route('/change-password')
class ChangePassword(Resource):

    @ns.expect(change_password_model)
    def post(self):
        """修改密码接口"""
        data = request.json
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not all([username, old_password, new_password]):
            return api_response(False, '缺少参数', status=400)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM Users WHERE username = %s", (username, ))
            row = cursor.fetchone()
            if not row:
                return api_response(False, '用户不存在', status=404)

            if row['password'] != old_password:
                return api_response(False, '原密码错误', status=401)

            cursor.execute("UPDATE Users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            return api_response(True, '密码修改成功')

        except Exception as e:
            conn.rollback()
            return api_response(False, f'修改失败: {str(e)}', status=500)
        finally:
            cursor.close()
            conn.close()
