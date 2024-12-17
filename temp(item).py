import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route('/item')
class Item(MethodView):
    def post(self):
        """Create a new item."""
        item_data = request.get_json()

        # Validate input
        if "name" not in item_data or "price" not in item_data or "store_id" not in item_data:
            abort(400, message="Bad request: 'name', 'price', and 'store_id' are required.")

        # Check if the store exists
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")

        # Check for duplicate item name within the store
        for item in items.values():
            if item["name"] == item_data["name"] and item["store_id"] == item_data["store_id"]:
                abort(400, message="An item with the same name already exists in this store.")

        # Create and store the new item
        item_id = uuid.uuid4().hex
        new_item = {"id": item_id, **item_data}
        items[item_id] = new_item
        return {"item": new_item}, 201

    def get(self):
        """Retrieve all items."""
        return {"items": list(items.values())}, 200


@blp.route('/item/<string:item_id>')
class ItemDetail(MethodView):
    def get(self, item_id):
        """Retrieve a specific item by ID."""
        item = items.get(item_id)
        if item is None:
            abort(404, message="Item not found.")
        return {"item": item}, 200

    def delete(self, item_id):
        """Delete a specific item by ID."""
        if item_id not in items:
            abort(404, message="Item not found.")
        del items[item_id]
        return {"message": "Item has been deleted."}, 200

    def put(self, item_id):
        """Update a specific item by ID."""
        item_data = request.get_json()

        # Validate input
        if "name" not in item_data or "price" not in item_data:
            abort(400, message="Bad request: 'name' and 'price' are required.")

        # Check if the item exists
        item = items.get(item_id)
        if not item:
            abort(404, message="Item not found.")

        # Update the item
        item.update(item_data)
        return {"item": item, "message": "Update successful."}, 200
