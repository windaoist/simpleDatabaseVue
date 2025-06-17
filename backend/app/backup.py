import os
import subprocess
from datetime import datetime
from flask import Blueprint, request, send_file
from flask_restx import Namespace, Resource, reqparse, fields
import ipdb
from app.utils import auth_required, api_response
from app.database import sql_info

# Blueprint + Namespace 注册
backup_bp = Blueprint('backup_bp', __name__)
backup_ns = Namespace('backup', description='数据库备份与恢复接口')

# 通用响应模型
success_model = backup_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='操作是否成功', example=True),
    'message': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据内容，如备份文件列表或空')
})

error_model = backup_ns.model('ErrorResponse', {'success': fields.Boolean(
    example=False), 'message': fields.String(description='错误信息')})

# 上传文件解析器
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type='FileStorage', required=True, help='上传 .sql 数据库备份文件')

# 查询参数解析器（restore/download/delete）
restore_query_model = backup_ns.parser()
restore_query_model.add_argument('source', type=str, required=True, choices=[
                                 'auto', 'manual'], help='备份来源')
restore_query_model.add_argument(
    'filename', type=str, required=True, help='.sql 文件名')


@backup_ns.route('/list')
class BackupFileList(Resource):

    @backup_ns.doc(description="获取所有备份文件列表（按自动/手动分类）")
    @backup_ns.response(200, '成功', success_model)
    @backup_ns.response(500, '服务器错误', error_model)
    @auth_required(roles=['Admin'])
    def get(self):
        try:
            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            auto_dir = os.path.join(project_root, 'backup', 'auto')
            manual_dir = os.path.join(project_root, 'backup', 'manual')

            auto_files = sorted(f for f in os.listdir(auto_dir) if f.endswith(
                '.sql')) if os.path.exists(auto_dir) else []
            manual_files = sorted(f for f in os.listdir(manual_dir) if f.endswith(
                '.sql')) if os.path.exists(manual_dir) else []

            return api_response(True, '获取成功', data={'auto': auto_files, 'manual': manual_files})
        except Exception as e:
            return api_response(False, f'获取失败: {str(e)}', status=500)


@backup_ns.route('/restore_file')
class RestoreFromFile(Resource):

    @backup_ns.expect(restore_query_model)
    @backup_ns.doc(description="根据已存在的备份文件恢复数据库")
    @backup_ns.response(200, '恢复成功', success_model)
    @backup_ns.response(400, '参数错误', error_model)
    @backup_ns.response(404, '文件不存在', error_model)
    @backup_ns.response(500, '恢复失败', error_model)
    @auth_required(roles=['Admin'])
    def post(self):
        source = request.args.get('source')
        filename = request.args.get('filename')

        if source not in ['auto', 'manual'] or not filename.endswith('.sql'):
            return api_response(False, '参数错误，请提供正确的 source 和 .sql 文件名', status=400)

        try:
            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            file_path = os.path.join(project_root, 'backup', source, filename)

            if not os.path.exists(file_path):
                return api_response(False, '文件不存在', status=404)

            db_host = sql_info['host']
            db_user = sql_info['user']
            db_password = sql_info['password']
            db_name = sql_info['db']

            with open(file_path, 'rb') as sql_file:
                proc = subprocess.Popen(['mysql', f'-h{db_host}', f'-u{db_user}', f'-p{db_password}', db_name],
                                        stdin=sql_file,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                _, stderr = proc.communicate()

                if proc.returncode != 0:
                    return api_response(False, f"恢复失败（mysql错误）: {stderr.decode('utf-8')}", status=500)

            return api_response(True, '数据库恢复成功')

        except Exception as e:
            return api_response(False, f'恢复失败: {str(e)}', status=500)


@backup_ns.route('/download_file')
class DownloadBackupFile(Resource):

    @backup_ns.expect(restore_query_model)
    @backup_ns.doc(description="下载指定备份文件")
    @backup_ns.response(200, '下载成功')
    @backup_ns.response(400, '参数错误', error_model)
    @backup_ns.response(404, '文件不存在', error_model)
    @backup_ns.response(500, '下载失败', error_model)
    @auth_required(roles=['Admin'])
    def get(self):
        source = request.args.get('source')
        filename = request.args.get('filename')

        if source not in ['auto', 'manual'] or not filename.endswith('.sql'):
            return api_response(False, '参数错误', status=400)

        try:
            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            file_path = os.path.join(project_root, 'backup', source, filename)

            if not os.path.exists(file_path):
                return api_response(False, '文件不存在', status=404)

            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return api_response(False, f'下载失败: {str(e)}', status=500)


@backup_ns.route('/delete_file')
class DeleteBackupFile(Resource):

    @backup_ns.expect(restore_query_model)
    @backup_ns.doc(description="删除指定备份文件")
    @backup_ns.response(200, '删除成功', success_model)
    @backup_ns.response(400, '参数错误', error_model)
    @backup_ns.response(404, '文件不存在', error_model)
    @backup_ns.response(500, '删除失败', error_model)
    @auth_required(roles=['Admin'])
    def delete(self):
        source = request.args.get('source')
        filename = request.args.get('filename')

        if source not in ['auto', 'manual'] or not filename.endswith('.sql'):
            return api_response(False, '参数错误', status=400)

        try:
            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            file_path = os.path.join(project_root, 'backup', source, filename)

            if not os.path.exists(file_path):
                return api_response(False, '文件不存在', status=404)

            os.remove(file_path)
            return api_response(True, '文件删除成功')
        except Exception as e:
            return api_response(False, f'删除失败: {str(e)}', status=500)


@backup_ns.route('/backup')
class ManualBackup(Resource):

    @backup_ns.doc(description="手动触发数据库备份并立即下载 SQL 文件")
    @backup_ns.response(200, '备份成功')
    @backup_ns.response(500, '备份失败', error_model)
    @auth_required(roles=['Admin'])
    def get(self):
        try:
            db_host = sql_info['host']
            db_user = sql_info['user']
            db_password = sql_info['password']
            db_name = sql_info['db']

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"manual_backup_{timestamp}.sql"

            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            backup_dir = os.path.join(project_root, 'backup', 'manual')
            os.makedirs(backup_dir, exist_ok=True)
            file_path = os.path.join(backup_dir, filename)

            cmd = [
                r"C:\Program Files\MySQL\MySQL Server 9.2\bin\mysqldump.exe",
                f"-h{db_host}",
                f"-u{db_user}",
                f"-p{db_password}",
                db_name,
            ]

            with open(file_path, "w", encoding="utf-8") as f:
                subprocess.run(
                    cmd, stdout=f, stderr=subprocess.PIPE, check=True)

            return send_file(file_path, as_attachment=True)
        except subprocess.CalledProcessError as e:
            return api_response(False, f"备份失败（mysqldump错误）: {str(e)}", status=500)
        except Exception as e:
            return api_response(False, f"备份失败: {str(e)}", status=500)


@backup_ns.route('/restore')
class RestoreFromUpload(Resource):

    @backup_ns.expect(upload_parser)
    @backup_ns.doc(description="上传 SQL 文件进行数据库恢复")
    @backup_ns.response(200, '恢复成功', success_model)
    @backup_ns.response(400, '上传无效', error_model)
    @backup_ns.response(500, '恢复失败', error_model)
    @auth_required(roles=['Admin'])
    def post(self):
        file = request.files.get('file')
        if not file or not file.filename.endswith('.sql'):
            return api_response(False, '请上传 .sql 格式的数据库备份文件', status=400)

        try:
            db_host = sql_info['host']
            db_user = sql_info['user']
            db_password = sql_info['password']
            db_name = sql_info['db']

            project_root = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..'))
            upload_dir = os.path.join(project_root, 'backup', 'upload')
            os.makedirs(upload_dir, exist_ok=True)

            filepath = os.path.join(upload_dir, file.filename)
            file.save(filepath)

            with open(filepath, 'rb') as sql_file:
                proc = subprocess.Popen(['mysql', f'-h{db_host}', f'-u{db_user}', f'-p{db_password}', db_name],
                                        stdin=sql_file,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()

            with open(filepath, 'rb') as sql_file:
                proc = subprocess.Popen(['mysql', f'-h{db_host}', f'-u{db_user}', f'-p{db_password}', db_name],
                                        stdin=sql_file,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                _, stderr = proc.communicate()
                if proc.returncode != 0:
                    return api_response(False, f"恢复失败（mysql错误）: {stderr.decode('utf-8')}", status=500)

            return api_response(True, '数据库恢复成功')
        except Exception as e:
            return api_response(False, f"恢复失败: {str(e)}", status=500)


def auto_backup_database(root_path=None):
    db_host = sql_info['host']
    db_user = sql_info['user']
    db_password = sql_info['password']
    db_name = sql_info['db']

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"auto_backup_{timestamp}.sql"

        project_root = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..'))
        backup_dir = os.path.join(project_root, 'backup', 'auto')
        os.makedirs(backup_dir, exist_ok=True)
        file_path = os.path.join(backup_dir, filename)

        # 删除旧文件，保留10个
        backups = sorted([f for f in os.listdir(
            backup_dir) if f.endswith('.sql')])
        while len(backups) >= 10:
            os.remove(os.path.join(backup_dir, backups.pop(0)))

        # 控制最多保留10个备份
        existing_backups = sorted([f for f in os.listdir(
            backup_dir) if f.startswith('auto_backup_') and f.endswith('.sql')])
        while len(existing_backups) >= 10:
            oldest = existing_backups.pop(0)
            os.remove(os.path.join(backup_dir, oldest))

        cmd = [
            r"C:\Program Files\MySQL\MySQL Server 9.2\bin\mysqldump.exe",
            f"-h{db_host}",
            f"-u{db_user}",
            f"-p{db_password}",
            db_name,
        ]

        with open(file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)

        print(f"[Auto Backup] 成功备份数据库至: {file_path}")
    except Exception as e:
        print(f"[Auto Backup] 自动备份失败: {e}")
