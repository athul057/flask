from flask.views import MethodView
from flask_smorest import Blueprint,abort

from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from blocklist import BLOCKlIST

from passlib.hash import pbkdf2_sha256

from db import db

from models import UserModel
from schemas import UserSchema


blp =Blueprint("users",__name__,"Operation on user creation.")

@blp.route("/register")
class UserRegister(MethodView):

 @blp.arguments(UserSchema)
 def post(self,user_data):
  if UserModel.query.filter(UserModel.username==user_data["username"]).first():
   abort(409,message="A user with the give user name already exists.")

  user=UserModel(
   username=user_data["username"],
   password=pbkdf2_sha256.hash(user_data["password"])
  )
  db.session.add(user)
  db.session.commit()

  return {"message":"User created"},201
 

@blp.route("/user/<int:user_id>")
class UserLogin(MethodView):

 def delete(self,user_id):
  user=UserModel.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return {"message":"user delted"},200



@blp.route("/login")
class Login(MethodView):
  @blp.arguments(UserSchema)
  def post(self,user_data):
   

   user=UserModel.query.filter(UserModel.username==user_data["username"]).first()
   if user and pbkdf2_sha256.verify(user_data["password"],user.password):
    access_token = create_access_token(identity=str(user.id),fresh=True)

    # access_token=create_access_token(identity=user.id)
    
    return {"message":access_token},201
   
   abort(404,message="Please check your credentials.")


@blp.route("/logout")
class Logout(MethodView):
 @jwt_required()
 def post(self):
  # jti=get_jwt().get("jti")
  jti=get_jwt()["jti"]
  BLOCKlIST.add(jti)
  return {"message":"Successfully Logged out"},201

 
