
from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from .auth import auth
        from .user import user
        from .admin import admin

        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(user, url_prefix='/user')
        app.register_blueprint(admin, url_prefix='/admin')

        return app
