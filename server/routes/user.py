from fastapi import APIRouter, Depends
from models.user import UserIn, UserResponse
from controllers.user import register_user, login_user, toggle_follow, get_user_by_id
from lib.verification import verifyUser

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserIn):
    return register_user(user_in.username, user_in.email, user_in.password)

@router.post("/login")
def login(user_in: UserIn):
    return login_user(user_in.email, user_in.password)

@router.post("/toggle_follow")
def toggle_follow_route(followed_id: str, user: dict = Depends(verifyUser)):
    follower_id = user["_id"] 
    return toggle_follow(follower_id, followed_id)

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: str, user: dict = Depends(verifyUser)):
    return get_user_by_id(user_id)
