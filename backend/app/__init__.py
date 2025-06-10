from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    api = Api(
        app,
        version='1.0',
        title='Project API',
        description='API documentation for the project',
        doc='/swagger/'
    )
    CORS(app)
    # 注册蓝图
    from app.main import main_bp
    from app.query import query_bp, query_ns
    from app.upload import upload_bp, ns as upload_ns
    from app.add_edit import add_edit_bp, ns as add_edit_ns
    from app.export import export_bp, ns as export_ns

    app.register_blueprint(main_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(add_edit_bp)
    app.register_blueprint(export_bp)

    # api.init_app(app)  # 延迟绑定
    api.add_namespace(query_ns, path='/query')
    api.add_namespace(upload_ns, path='/upload')
    api.add_namespace(add_edit_ns, path='/add-edit')
    api.add_namespace(export_ns, path='/export')
    return app
