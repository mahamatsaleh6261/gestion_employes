from flask import Flask

from app.routes import employee_bp, main_bp
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    init_app(app)
    register_blueprints(app)

    from app.models import Employee, User

    return app


def init_app(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask):
    app.register_blueprint(main_bp)
    app.register_blueprint(employee_bp)
