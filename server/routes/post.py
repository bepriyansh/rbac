from fastapi import APIRouter, Depends
from models.post import PostIn, PostResponse
from controllers.posts import create_post, get_post_by_id, get_public_posts, get_posts_from_following_people, update_post, delete_post, toggle_like
from lib.verification import verifyUser

router = APIRouter()

@router.post("/create", response_model=PostResponse)
def create(post_in: PostIn, user: dict = Depends(verifyUser)):
    return create_post(user["_id"], post_in.content)

@router.get("/post/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    return get_post_by_id(post_id)

@router.get("/public_posts")
def get_public(page: int = 1, page_size: int = 10):
    return get_public_posts(page, page_size)

@router.get("/following_posts")
def get_following_posts(page: int = 1, page_size: int = 10, user: dict = Depends(verifyUser)):
    return get_posts_from_following_people(user["_id"], page, page_size)

@router.put("/post/{post_id}")
def update_post_route(post_id: str, post_in: PostIn, user: dict = Depends(verifyUser)):
    return update_post(post_id, user, post_in.content)

@router.delete("/post/{post_id}")
def delete_post_route(post_id: str, user: dict = Depends(verifyUser)):
    return delete_post(post_id, user)

@router.post("/toggle_like/{post_id}")
def toggle_like_route(post_id: str, user: dict = Depends(verifyUser)):
    return toggle_like(post_id, user["_id"])
