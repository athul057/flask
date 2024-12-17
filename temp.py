from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)

@app.get('/store')
def get_store_data():
    return {"stores": list(stores.values())}, 200


@app.post('/store')
def create_store():
    

   # Check if the request body is empty or not valid JSON
    if not request.data:
        return {"message": "Request body cannot be empty"}, 400
    store_data = request.get_json()
    
    # Validate input
    if not store_data.get("name"):
        abort(404,message="Store not found")

    # Check for duplicate store names
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(404,message="Store with this already exits")

    store_id = uuid.uuid4().hex
    new_store = {"id": store_id, "name": store_data["name"]}
    stores[store_id] = new_store
    return {"store": new_store}, 201


@app.post('/item')
def create_item():
    item_data = request.get_json()

    # # Validate input
    # if not item_data.get("name") or not item_data.get("store_id"):
    #     abort(404,message="Store not found")  

    # if "name" not in item_data or "price" not in item_data or "store_id" not in item_data:
    #     abort(404,message="Some Bad request check name and price is available or not")

    if "name" not in item_data or "price" not in item_data or "store_id" not in item_data:
        return {"message":"Some Bad request check name and price is available or not"},404

    # CHECK FOR DUPLICATE VALUE...................


    if item_data["store_id"] not in stores:
        abort(404,message="Store not found")

    item_id = uuid.uuid4().hex
    new_item = {"id": item_id, **item_data}
    items[item_id] = new_item
    return {"item": new_item}, 201


@app.get('/item')
def get_items():
    return {"items": list(items.values())}, 200


@app.get('/store/<string:store_id>')
def get_store(store_id):
    store = stores.get(store_id)
    if store is None:
        abort(404,message="Store not found")
    return {"store": store}, 200


@app.get('/item/<string:item_id>')
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        abort(404,message="Item not found")
    return {"item": item}, 200


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item has deleted"}
    except:
        abort(404,message="Item not found")

@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data=request.get_json()
    if("price"not in item_data or "name" not in item_data):
        abort(404,message="Please check your values")
    try:
        item=items[item_id]
        item.update(item_data)
        return {"message":"update successful"}
    except KeyError:
        abort(404,message="Check your storeId")

if __name__ == '__main__':
    app.run(debug=True)
