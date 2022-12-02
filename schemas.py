from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)  # only for returning data
    name = fields.Str(required=True)  # required both as input and as a response
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):  # Having Plain classes prevents
    # from circular dependency
    store_id = fields.Int(required=True, load_only=True)  # only for input
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  # only for
    # output


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
