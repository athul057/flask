from db import db

class ItemTags(db.Model):
 __tablename__="items_tags"


 id=db.Column(db.Integer,primary_key=True)
 item=db.Column(db.Integer,db.ForeignKey("items.id"))
 tag=db.Column(db.Integer,db.ForeignKey("tags.id"))
