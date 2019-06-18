from pymongo import MongoClient
from pymodm.connection import connect

connect("mongodb://localhost:27017/gfg_db")