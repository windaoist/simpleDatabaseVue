from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_apscheduler import APScheduler
from app.backup import auto_backup_database
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    authorizations = {'Bearer Auth': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization', 'description': '输入JWT Bearer令牌'}}
    api = Api(app, version='1.0', title='project API', description='本项目的API文档', authorizations=authorizations, security='Bearer Auth', doc='/swagger/')

    CORS(app, expose_headers=["Content-Disposition"])

    # 注册蓝图
    from app.main import main_bp
    from app.query import query_bp, query_ns
    from app.upload import upload_bp, ns as upload_ns
    from app.add_edit import add_edit_bp, ns as add_edit_ns
    from app.export import export_bp, ns as export_ns
    from app.auth import auth_bp, ns as auth_ns
    from app.backup import backup_bp, backup_ns

    app.register_blueprint(main_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(add_edit_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(backup_bp)

    # api.init_app(app)  # 延迟绑定
    api.add_namespace(query_ns, path='/query')
    api.add_namespace(upload_ns, path='/upload')
    api.add_namespace(add_edit_ns, path='/add-edit')
    api.add_namespace(export_ns, path='/export')
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(backup_ns, path='/backup')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    @scheduler.task('interval', id='daily_auto_backup', hours=24)
    def auto_task():
        with app.app_context():
            auto_backup_database(app.root_path)

    return app
