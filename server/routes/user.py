from fastapi import APIRouter, Depends
from models.user import UserIn, UserResponse
from controllers.user import register_user, login_user, toggle_follow, get_user_by_id
from lib.verification import verifyUser
from lib.response import failedResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserIn):
    try:
        return register_user(user_in.username, user_in.email, user_in.password)
    except Exception as e:
        return failedResponse(500, {"message": f"Error registering user: {str(e)}"})

@router.post("/login")
def login(user_in: UserIn):
    try:
        result = login_user(user_in.email, user_in.password)
        if result:
            return result
        return failedResponse(404, {"message": "Invalid credentials."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error logging in user: {str(e)}"})

@router.post("/toggle_follow")
def toggle_follow_route(followed_id: str, user: dict = Depends(verifyUser)):
    try:
        follower_id = user["_id"] 
        return toggle_follow(follower_id, followed_id)
    except Exception as e:
        return failedResponse(500, {"message": f"Error toggling follow: {str(e)}"})

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: str, user: dict = Depends(verifyUser)):
    try:
        return get_user_by_id(user_id)
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching user: {str(e)}"})
