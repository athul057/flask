from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import StoreModel
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from db import db

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        """Retrieve a specific store by ID."""
        store=StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        """Delete a specific store by ID."""
        item=StoreModel.query.get_or_404(store_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Store has been deleted."}, 200


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        """Retrieve all stores."""
        return StoreModel.query.all()
    

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as i:
            print(f"ingegrity error {i}")
            abort(500,message="A store with that name already exists.")
        except SQLAlchemyError as e:
            print(f"sqlAlchemy error {e}")
            abort(500,message="Some error happened in the database.")
        return store

