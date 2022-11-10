import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = stores.get(store_id)
        if store is not None:
            return store
        abort(404, message="Store not found.")

    def delete(self, store_id):
        store = stores.get(store_id)
        if store is not None:
            del stores[store_id]
            return {"message": "Store deleted."}
        abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        if "name" not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
