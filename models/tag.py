from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    #Since store_id is a foreign key each Tag will have one store connects with it ONE TO MANY relation...
    # store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),nullable=True)


    # Define relationship with StoreModel
    #It is MANY TO ONE relation. It only point to one tag model at time so no need of lazy="dynamic".Since at a time it point one tag model.
    store = db.relationship("StoreModel", back_populates="tags")

    # Define relationship with ItemTagModle.
    items=db.relationship("ItemModel",back_populates="tag",secondary="items_tags")