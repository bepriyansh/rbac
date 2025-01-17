from datetime import datetime
from bson import ObjectId
from typing import Optional
from lib.mongodb import users_collection, follow_relation_collection
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User Registration Pydantic Model
class UserIn(BaseModel):
    username: str
    email: str
    password: str

# User Response Pydantic Model
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Utility function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Register a new user
def register_user(username: str, email: str, password: str) -> dict:
    hashed_password = hash_password(password)
    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(),
    }
    result = users_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    user["password"] = None  # Remove the password field from the response
    return user

# Login user (authenticate user and generate JWT token)
def login_user(email: str, password: str) -> Optional[dict]:
    user = users_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        # Generate JWT token on successful login
        token = jwt.encode({"sub": str(user["_id"]), "exp": datetime.utcnow()}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    return None

# Toggle follow/unfollow functionality
def toggle_follow(follower_id: str, followed_id: str) -> bool:
    # Check if the user is already following
    existing_relation = follow_relation_collection.find_one({"follower_id": follower_id, "followed_id": followed_id})
    
    if existing_relation:
        # Unfollow the user
        follow_relation_collection.delete_one({"follower_id": follower_id, "followed_id": followed_id})
        return False
    else:
        # Follow the user
        follow_relation_collection.insert_one({"follower_id": follower_id, "followed_id": followed_id, "created_at": datetime.now()})
        return True

# Get user by ID (For displaying profile or other user-related details)
def get_user_by_id(user_id: str) -> dict:
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        user["password"] = None  # Remove password for security
    return user
