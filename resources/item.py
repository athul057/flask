
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db

from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required,get_jwt

from models import ItemModel

from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route('/item')
class Item(MethodView):

    #we can't call this reequest unless we send a jwt along with the request.
    @jwt_required()
    @blp.arguments(ItemSchema)
    # @blp.response(201, ItemSchema)
    
    def post(self,item_data):
        item=ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"error is {e}")
            abort(500,message=str(e))
        # return item
        return {"message":"item created"},201

    @blp.response(200,ItemSchema(many=True))
    @jwt_required()
    def get(self):
        
        """Retrieve all items."""
        return ItemModel.query.all()


@blp.route('/item/<string:item_id>')
class ItemDetail(MethodView):
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        """Retrieve a specific item by ID."""
        item=ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="You don't have the permission")

        """Delete a specific item by ID."""
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item has been deleted."}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data, item_id):
        # Check if the item exists
        item=ItemModel.query.get(item_id)
        if item:
            item.name=item_data["name"]
            item.price=item_data["price"]
        else:
            item=ItemModel(**item_data)
        db.session.add(item)
        db.session.commit()

        return item



