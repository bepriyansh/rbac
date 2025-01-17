from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize MongoDB Client
DATABASE_URL = os.getenv("DATABASE_URL")
client = MongoClient(DATABASE_URL)
db = client['rabc']

# Export collections
users_collection = db['users']
posts_collection = db['posts']
comments_collection = db['comments']
follow_relation_collection = db['follow_relation']
