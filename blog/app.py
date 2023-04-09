from flask import Flask
from blog import commands
from blog.extensions import db, login_manager
from blog.models import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "!$kh8$cz-z9q4@_430j_23-kw=y9*!#3v76vc!mp9c1*f)j+4z"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"


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
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_init_user)