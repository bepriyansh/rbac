import os
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get MongoDB URI from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to MongoDB
client = MongoClient(DATABASE_URL)
db = client['testdb']  # Database name
users_collection = db['users']  # Collection name

# Pydantic model to define user data
class User(BaseModel):
    name: str
    email: str
    age: int

# Utility function to convert ObjectId to string
def user_dict(user) -> dict:
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

# Route to create a user
@app.post("/create_user")
async def create_user(user: User):
    user_data = user.dict()
    result = users_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return JSONResponse(content=user_data)

# Route to fetch the created user
@app.get("/user/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return JSONResponse(content=user_dict(user))
    return JSONResponse(status_code=404, content={"message": "User not found"})

