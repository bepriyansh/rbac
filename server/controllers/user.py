from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
from lib.mongodb import users_collection, follow_relation_collection
from models.user import UserResponse
from lib.response import successResponse, failedResponse

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def register_user(username: str, email: str, password: str) -> dict:
    try:
        hashed_password = hash_password(password)
        user = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.now(),
        }
        result = users_collection.insert_one(user) 
        user["_id"] = str(result.inserted_id) 
        user["password"] = None  

        token = jwt.encode({"sub": user["_id"], "exp": datetime.now()}, SECRET_KEY, algorithm=ALGORITHM)

        user_response = UserResponse(**user)
        return successResponse(201, {"access_token": token, "token_type": "bearer", "user": user_response.model_dump()})
    except Exception as e:
        return failedResponse(500, {"message": f"Error registering user: {str(e)}"})

def login_user(email: str, password: str) -> Optional[dict]:
    try:
        user = users_collection.find_one({"email": email})
        if user and verify_password(password, user["password"]):
            token = jwt.encode({"sub": str(user["_id"]), "exp": datetime.now(timezone.utc)}, SECRET_KEY, algorithm=ALGORITHM)
            user["_id"] = str(user["_id"]) 
            user["password"] = None  
            user_response = UserResponse(**user)
            return successResponse(200, {"access_token": token, "token_type": "bearer", "user": user_response.model_dump()})
        return failedResponse(404, {"message": "Invalid credentials."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error logging in user: {str(e)}"})

def toggle_follow(follower_id: str, followed_id: str) -> dict:
    try:
        existing_relation = follow_relation_collection.find_one({"follower_id": follower_id, "followed_id": followed_id})
        if existing_relation:
            follow_relation_collection.delete_one({"follower_id": follower_id, "followed_id": followed_id})
            return successResponse(200, {"message": "Unfollowed successfully."})
        else:
            follow_relation_collection.insert_one({"follower_id": follower_id, "followed_id": followed_id, "created_at": datetime.now()})
            return successResponse(200, {"message": "Followed successfully."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error toggling follow: {str(e)}"})

def get_user_by_id(user_id: str) -> dict:
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user["password"] = None
            return successResponse(200, user)
        return failedResponse(404, {"message": "User not found."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching user: {str(e)}"})
