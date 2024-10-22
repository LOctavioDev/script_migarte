import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def get_db_connection():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client.db_residency
