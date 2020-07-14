from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


def save_product_list(products):
    mongo.db.products.insert_many(products)


def clear_product_list():
    mongo.db.products.drop()


def get_products_list():
    return mongo.db.products.find()

