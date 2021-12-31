from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient
from trackme.contants import *
import trackme.database.mongo.collections as db_collections

# initialize connection
client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}')

# initialize database
db = client.trackme
for collection_model in db_collections.models:
    collection = db.get_collection(collection_model.collection_name)
    for index in collection_model.indexes:
        if isinstance(index, tuple):
            collection.create_index(index[0], unique=True)
        else:
            collection.create_index(index)