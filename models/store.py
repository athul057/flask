from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Define relationship with ItemModel
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic",cascade="all,delete")

    # Define relationship with TagModel
    #Here back_populates should point to the TagModel's 'store' item.
    #One store will connect with many tags.ONE TO MANY relation.
    #For that reason we are using lazy="dynamic"
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
