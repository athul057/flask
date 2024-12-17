from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, StoreModel,ItemModel
from schemas import TagSchema,PlainTagSchema

blp = Blueprint("Tags", __name__, description="Operation on tags")

@blp.route("/store/<string:store_id>/tag")
class TaginStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()  # Fetch all tags for the store

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data,store_id=store_id)  # Correctly use store_id

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))  # Use 500 for server errors

        return tag


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)  # Return a single tag
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    

@blp.route("/tag")
class Tag(MethodView):

    @blp.response(200,TagSchema(many=True))
    def get(self):
        return TagModel.query.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    
    def post(self,tag_data):
        tag=TagModel(**tag_data)
        print(tag)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag


    


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(200,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        my_tag=TagModel.query.get_or_404(tag_id)
        item.tag.append(my_tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
                abort(500,message=str(e))

        #Here the 'tag' will automatically serialize by using TagSchema...
        return my_tag
    
    @blp.response(200,TagSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        my_tag=TagModel.query.get_or_404(tag_id)

        item.tag.remove(my_tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message="An error occured during the deletion")

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,description="Deletes a tag if not item tagged with it ")
    @blp.alt_response(400,description="Returns if the tag is assigned with another item It can't be delete,First we have the unassign the tag from the item")
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag deleted"}
        abort(
            400,message="Could not be deleted Make sure the tag is not associated with any other items."
        )
        
