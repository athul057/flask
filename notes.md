**PYTHON**

In Python, when you retrieve a dictionary item (or a mutable object like a list) using its key (e.g., item = items[item_id]), the item variable is a reference to the actual dictionary stored in items.

When you call item.update(item_data), you're modifying the same object in memory, which means the changes are reflected in items without needing any additional assignment.

Why Does This Work?
Mutable Objects in Python:

Dictionaries are mutable, meaning they can be changed in place.
item = items[item_id] gives item a reference to the dictionary stored in items at the key item_id.
In-Place Update:

The update() method modifies the dictionary in place, so changes to item are directly applied to items[item_id].
Example

```python
items = {
    "item1": {"name": "Book", "price": 10},
    "item2": {"name": "Pen", "price": 2}
}

item_id = "item1"
item_data = {"price": 12, "color": "blue"}

# Update the item
item = items[item_id]
item.update(item_data)

print(items)
```



`pip install -r requirements.txt`

```sql
from db import db

class StoreModel(db.Model):
 __tablename__="stores"
 id=db.Column(db.Integer,primary_key=True)
 name=db.Column(db.String(80),unique=True,nullable=False)
 items=db.relationship("ItemModel",back_populate="stores",lazy="dynamic")
```
 
Here __lazy="dynamic__ means don't prefetch the items  from the databse until we explicitly tells about it.
So sql alchemy won't prefetch the items and it will give us some performance boost....
Here items will prefetch data from Itemmodel class.(It made a relationship with 'items' table in the ItemModel class..)
Here we can make the fetching from database dynamically if we want it .



` app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")`

Here if the database environ ment variable "DATABASE_URL" present the we will use that environment variable for that particular database(ed:postgress).Other wise we will use sqlite database



 serialized
 converting Python objects to JSON




 ```python
 import secrets

 my_secret=secrets.SystemRandom().getrandbits(128)
 ```

 passlib for hashing our password.