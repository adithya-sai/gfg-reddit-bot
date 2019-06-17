from pymongo import MongoClient

client = MongoClient()

db = client.gfg_db

fixtures_col = db.fixtures_collection
users_col = db.users_collection
