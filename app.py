import os

from flask import Flask
from flask_smorest import Api

from db import db
from resources.item import blp as item_blueprint
from resources.store import blp as store_blueprint
from resources.tag import blp as tag_blueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # Use swagger documentation (smorest)
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_CONFIGURATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(item_blueprint)
    api.register_blueprint(store_blueprint)
    api.register_blueprint(tag_blueprint)

    return app
