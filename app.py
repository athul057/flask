from flask import Flask,jsonify
from flask_smorest import Api
import os
import models
from db import db

from flask_migrate import Migrate

from blocklist import BLOCKlIST

from flask_jwt_extended import JWTManager

from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint
from resources.users import blp as UserBLuePrint



# migrate = Migrate()
def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)
    migrate=Migrate(app,db)
    # migrate.init_app(app, db)


    # If we using Flask-Migrate we can avoid using this.We don't want the sqlalchemy to create the tabls for us .Now flask-migrate will take care this.
    with app.app_context():
        db.create_all()

    app.config["JWT_SECRET_KEY"]="athul"
    jwt=JWTManager(app)


    # If this function returns true the we will get error since our current jwt token is in block list
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKlIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "description":"The token has been revoked",
                    "error":"token has revoked"
                }
            ),401
        )

    #To create additional information......Like admin privilage etc.
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity==1:
            return {"is_admin":True}
        else:
            return {"id_admin":False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "message":"Signature verification failed","error":"invalid token"
                }
            ),401
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description":"Request Doesn't contain access token",
                    "error":"authorization_reuqired"
                }
            ),401
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message":"Singature verification failed",
                    "error":"Invalid token"
                }
            ),401
        )
    api = Api(app)
    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBLuePrint)

    return app
