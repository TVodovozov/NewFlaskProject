import os
from flask import Flask
from blog import commands
from blog.extensions import db, login_manager, csrf
from blog.models import User
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
cfg_name = os.environ.get("CONFIG_NAME") or "DevConfig"
app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db, compare_type=True)
csrf.init_app(app)


def create_app() -> Flask:
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from blog.auth.views import auth
    from blog.user.views import user

    app.register_blueprint(user)
    app.register_blueprint(auth)


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)