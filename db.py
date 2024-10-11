from pymongo import MongoClient
from urllib.parse import quote_plus

username = "tanmaya"
password = "Tanmaya@mongo"

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.6yvxr.mongodb.net/"
client = MongoClient(mongo_uri)

db = client["MyDB"]
items_collection = db["items"]
clock_in_records_collection = db["clock_in_records"]


def create(data, collection):
    data = dict(data)
    response = collection.insert_one(data)
    return response

