import os
import subprocess
from datetime import datetime
from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename
from flask_restx import Namespace, Resource, reqparse
from app.utils import auth_required, api_response

# Blueprint + Namespace 注册
backup_bp = Blueprint('backup_bp', __name__)
backup_ns = Namespace('backup', description='数据库备份与恢复接口')

# 定义 Swagger 上传模型（手动支持文件上传）
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type='FileStorage', required=True, help='上传 .sql 数据库备份文件')


@backup_ns.route('/backup')
class ManualBackup(Resource):

    @auth_required(roles=['Admin'])
    def get(self):
        """手动触发备份（仅限管理员）"""
        try:
            db_host = '127.0.0.1'
            db_user = 'root'
            db_password = 'root'
            db_name = 'myDatabase'

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"manual_backup_{timestamp}.sql"

            parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            backup_dir = os.path.join(parent_dir, 'db_backups', 'manual')
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
class Restore(Resource):

    @auth_required(roles=['Admin'])
    def post(self):
        """上传 SQL 文件恢复数据库（仅限管理员）"""
        file = request.files.get('file')
        if not file or not file.filename.endswith('.sql'):
            return api_response(False, '请上传 .sql 格式的数据库备份文件', status=400)

        try:
            db_host = '127.0.0.1'
            db_user = 'remoteuser'
            db_password = 'password123'
            db_name = 'myDatabase'

            parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            backup_dir = os.path.join(parent_dir, 'db_backups', 'auto')
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


def auto_backup_database(root_path=None):
    """
    自动备份数据库（保留最近10个），不返回文件，而是仅执行备份
    """
    db_host = '127.0.0.1'
    db_user = 'remoteuser'
    db_password = 'password123'
    db_name = 'myDatabase'

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"auto_backup_{timestamp}.sql"

        if not root_path:
            root_path = os.getcwd()

        backup_dir = os.path.join(root_path, 'db_backups', 'auto')
        os.makedirs(backup_dir, exist_ok=True)
        file_path = os.path.join(backup_dir, filename)

        # 控制最多保留10个备份
        existing_backups = sorted([f for f in os.listdir(
            backup_dir) if f.startswith('auto_backup_') and f.endswith('.sql')])
        while len(existing_backups) >= 10:
            oldest = existing_backups.pop(0)
            os.remove(os.path.join(backup_dir, oldest))

        # 调用 mysqldump 命令
        cmd = f"mysqldump -h{db_host} -u{db_user} -p{db_password} {db_name} > \"{file_path}\""
        subprocess.run(cmd, shell=True, check=True)

        print(f"[Auto Backup] 成功备份数据库至: {file_path}")
    except Exception as e:
        print(f"[Auto Backup] 自动备份失败: {e}")
