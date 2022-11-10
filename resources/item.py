import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
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

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)  # The order of decorators matter
    def put(self, item_id, item_data):
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
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):  # it's not necessary to get_json from request
        # Still need to validate if item already exists
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(400, message="Item already exists.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
