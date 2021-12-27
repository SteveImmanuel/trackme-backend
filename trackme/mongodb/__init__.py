from dotenv import load_dotenv

load_dotenv()

import os
from pymongo import MongoClient
import trackme.mongodb.collections as db_collections

# initialize connection
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}')

# initialize database
db = client.trackme
for collection_model in db_collections.models:
    collection = db.get_collection(collection_model.collection_name)
    for index in collection_model.indexes:
        collection.create_index(index)