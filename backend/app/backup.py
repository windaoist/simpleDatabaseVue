import os
import subprocess
from datetime import datetime
from flask import Blueprint, request, current_app, send_file
from werkzeug.utils import secure_filename
from flask_restx import Namespace, Resource
from app.utils import auth_required, api_response

# 定义 Blueprint 与 Namespace
backup_bp = Blueprint('backup_bp', __name__)
backup_ns = Namespace('backup', description='数据库备份与恢复接口')


@backup_ns.route('/backup')
class DatabaseBackup(Resource):

    @auth_required(roles=['Admin'])
    def get(self):
        """导出数据库 SQL 文件（仅限管理员）"""
        try:
            db_host = '127.0.0.1'
            db_user = 'root'
            db_password = 'root'
            db_name = 'myDatabase'

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"backup_{timestamp}.sql"
            backup_dir = os.path.join(current_app.root_path, 'db_backups')
            os.makedirs(backup_dir, exist_ok=True)
            file_path = os.path.join(backup_dir, filename)

            cmd = f"mysqldump -h{db_host} -u{db_user} -p{db_password} {db_name} > \"{file_path}\""
            subprocess.run(cmd, shell=True, check=True)

            return send_file(file_path, as_attachment=True)

        except subprocess.CalledProcessError as e:
            return api_response(False, f"备份失败（mysqldump错误）: {str(e)}", status=500)
        except Exception as e:
            return api_response(False, f"备份失败: {str(e)}", status=500)


@backup_ns.route('/restore')
class DatabaseRestore(Resource):

    @auth_required(roles=['Admin'])
    def post(self):
        """上传 SQL 文件并恢复数据库（仅限管理员）"""
        file = request.files.get('file')
        if not file or not file.filename.endswith('.sql'):
            return api_response(False, '请上传 .sql 格式的数据库备份文件', status=400)

        try:
            db_host = '127.0.0.1'
            db_user = 'root'
            db_password = 'root'
            db_name = 'myDatabase'

            backup_dir = os.path.join(current_app.root_path, 'db_backups')
            os.makedirs(backup_dir, exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(backup_dir, filename)
            file.save(file_path)

            cmd = f"mysql -h{db_host} -u{db_user} -p{db_password} {db_name} < \"{file_path}\""
            subprocess.run(cmd, shell=True, check=True)

            return api_response(True, '数据库恢复成功')

        except subprocess.CalledProcessError as e:
            return api_response(False, f"恢复失败（mysql错误）: {str(e)}", status=500)
        except Exception as e:
            return api_response(False, f"恢复失败: {str(e)}", status=500)
