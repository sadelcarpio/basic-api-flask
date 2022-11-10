import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        item = items.get(item_id)
        if item is not None:
            return item
        abort(404, message="Item not found.")

    def delete(self, item_id):
        item = items.get(item_id)
        if item is not None:
            del items[item_id]
            return {"message": "Item deleted."}
        abort(404, message="Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
        try:
            item = items[item_id]
            print(item)
            print(item_data)
            item |= item_data  # item now contains the union of item and item_data dictionaries
            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if "name" not in item_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(400, message="Item already exists.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
