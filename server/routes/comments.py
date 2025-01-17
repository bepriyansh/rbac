from fastapi import APIRouter, Depends
from models.comment import CommentCreate, CommentResponse
from controllers.comments import create_comment, delete_comment, get_comment_by_id, toggle_like
from lib.verification import verifyUser
from lib.response import successResponse, failedResponse

router = APIRouter()

@router.post("/create", response_model=CommentResponse)
def create_comment_route(comment_create: CommentCreate, user: dict = Depends(verifyUser)):
    try:
        return create_comment(comment_create.post_id, user["_id"], comment_create.content, comment_create.parent_comment_id)
    except Exception as e:
        return failedResponse(400, {"message": str(e)})

@router.delete("/delete/{comment_id}")
def delete_comment_route(comment_id: str, user: dict = Depends(verifyUser)):
    try:
        return delete_comment(comment_id, user)
    except Exception as e:
        return failedResponse(400, {"message": str(e)})

@router.get("/comment/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str):
    try:
        return get_comment_by_id(comment_id)
    except Exception as e:
        return failedResponse(400, {"message": str(e)})

@router.post("/like/{comment_id}")
def like_comment(comment_id: str, user: dict = Depends(verifyUser)):
    try:
        return toggle_like(comment_id, user["_id"])
    except Exception as e:
        return failedResponse(400, {"message": str(e)})
