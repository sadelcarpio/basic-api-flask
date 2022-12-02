from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # lazy means that items are not fetched with the record unless you tell it to
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
