from fastapi import APIRouter, Depends
from models.post import PostIn, PostResponse
from controllers.posts import create_post, get_post_by_id, get_public_posts, get_posts_from_following_people, update_post, delete_post, toggle_like
from lib.verification import verifyUser
from lib.response import failedResponse

router = APIRouter()

@router.post("/create", response_model=PostResponse)
def create(post_in: PostIn, user: dict = Depends(verifyUser)):
    try:
        return create_post(user["_id"], post_in.content)
    except Exception as e:
        return failedResponse(500, {"message": f"Error creating post: {str(e)}"})

@router.get("/post/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    try:
        return get_post_by_id(post_id)
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching post: {str(e)}"})

@router.get("/public_posts")
def get_public(page: int = 1, page_size: int = 10):
    try:
        return get_public_posts(page, page_size)
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching public posts: {str(e)}"})

@router.get("/following_posts")
def get_following_posts(page: int = 1, page_size: int = 10, user: dict = Depends(verifyUser)):
    try:
        return get_posts_from_following_people(user["_id"], page, page_size)
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching posts from following people: {str(e)}"})

@router.put("/post/{post_id}")
def update_post_route(post_id: str, post_in: PostIn, user: dict = Depends(verifyUser)):
    try:
        return update_post(post_id, user, post_in.content)
    except Exception as e:
        return failedResponse(500, {"message": f"Error updating post: {str(e)}"})

@router.delete("/post/{post_id}")
def delete_post_route(post_id: str, user: dict = Depends(verifyUser)):
    try:
        return delete_post(post_id, user)
    except Exception as e:
        return failedResponse(500, {"message": f"Error deleting post: {str(e)}"})

@router.post("/toggle_like/{post_id}")
def toggle_like_route(post_id: str, user: dict = Depends(verifyUser)):
    try:
        return toggle_like(post_id, user["_id"])
    except Exception as e:
        return failedResponse(500, {"message": f"Error toggling like: {str(e)}"})
