import jwt
from fastapi import HTTPException, Request
from lib.mongodb import users_collection
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def verifyToken(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    return token.split(" ")[1]

def verifyUser(request: Request):
    token = verifyToken(request)
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = users_collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verifyAdmin(request: Request):
    user = verifyUser(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="User does not have admin privileges")
    return user
