import uuid
from flask_smorest import abort
from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists.")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    store = stores.get(store_id)
    if store is not None:
        del stores[store_id]
        return {"message": "Store deleted."}
    abort(404, message="Store not found.")


@app.get("/store/<string:store_id>")  # path parameter
def get_store(store_id):
    store = stores.get(store_id)
    if store is not None:
        return store
    abort(404, message="Store not found.")


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Data validation. This comes by default with FastAPI, but you can use marshmallow or pydantic
    if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are in the JSON payload")

    for item in items.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message="Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
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


@app.get("/item/<string:item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if item is not None:
        return item
    abort(404, message="Item not found.")
