import requests

from dataclasses import dataclass
from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from sqlalchemy.exc import IntegrityError

from producer import publish


# import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:password@db/main"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title: str = db.Column(db.String(200))
    image: str = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer)
    product_id: int = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="user_product_unique")


@app.route("/api/products")
def index():
    return jsonify(Product.query.all())


@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id: int):
    req = requests.get("http://172.17.0.1:8000/api/user")
    json = req.json()

    try:
        product_user = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish("product_liked", id)
    except IntegrityError:
        abort(400, "You already liked this product")

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
