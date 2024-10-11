from pymongo import MongoClient
from urllib.parse import quote_plus

'''use for cloud MongoDB connections'''
#username = "username"
#password = "password"
#escaped_username = quote_plus(username)
#escaped_password = quote_plus(password)
#mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.6yvxr.mongodb.net/"
#client = MongoClient(mongo_uri)

'''for local MongoDB connection'''
mongoURI = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURI)

db = client["MyDB"]
items_collection = db["items"]
clock_in_records_collection = db["clock_in_records"]


def create(data, collection):
    data = dict(data)
    response = collection.insert_one(data)
    return response

