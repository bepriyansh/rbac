from bson import ObjectId
from datetime import datetime
from typing import Optional
from lib.mongodb import comments_collection
from lib.response import successResponse, failedResponse

def delete_replies(comment_id: str) -> None:
    try:
        replies = comments_collection.find({"parent_comment_id": comment_id})
        for reply in replies:
            delete_replies(reply["_id"]) 
        comments_collection.delete_many({"parent_comment_id": comment_id})
    except Exception as e:
        raise Exception(f"Failed to delete replies: {str(e)}")

def delete_comment(comment_id: str, user: dict) -> dict:
    try:
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            return failedResponse(404, {"message": "Comment not found."})

        if not (comment["user_id"] == user["_id"] or user["role"] == "admin"):
            return failedResponse(403, {"message": "Unauthorized action."})

        delete_replies(comment_id)
        result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count > 0:
            return successResponse(200, {"message": "Comment deleted successfully."})
        else:
            return failedResponse(500, {"message": "Failed to delete comment."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error deleting comment: {str(e)}"})

def create_comment(post_id: str, user_id: str, content: str, parent_comment_id: Optional[str] = None) -> dict:
    try:
        comment = {
            "post_id": post_id,
            "user_id": user_id,
            "content": content,
            "parent_comment_id": parent_comment_id,
            "created_at": datetime.now(),
            "likes": [],  
            "reply_count": 0,  
        }
        result = comments_collection.insert_one(comment)
        comment["_id"] = str(result.inserted_id)
        return successResponse(201, comment)
    except Exception as e:
        return failedResponse(500, {"message": f"Error creating comment: {str(e)}"})

def get_replies(comment_id: str) -> list:
    try:
        replies = comments_collection.find({"parent_comment_id": comment_id})
        return [{"_id": str(reply["_id"]), **reply} for reply in replies]
    except Exception as e:
        raise Exception(f"Error fetching replies: {str(e)}")

def get_comment_by_id(comment_id: str) -> dict:
    try:
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        if comment:
            comment["_id"] = str(comment["_id"])
            replies = get_replies(comment_id)
            comment["replies"] = replies
            comment["reply_count"] = len(replies)
            return successResponse(200, comment)
        return failedResponse(404, {"message": "Comment not found."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching comment: {str(e)}"})

def toggle_like(comment_id: str, user_id: str) -> dict:
    try:
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            return failedResponse(404, {"message": "Comment not found."})

        if user_id in comment["likes"]:
            comments_collection.update_one(
                {"_id": ObjectId(comment_id)},
                {"$pull": {"likes": user_id}}
            )
        else:
            comments_collection.update_one(
                {"_id": ObjectId(comment_id)},
                {"$addToSet": {"likes": user_id}}
            )

        comments_collection.update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"likes_count": len(comment["likes"])}}
        )
        return successResponse(200, {"message": "Like status updated successfully."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error toggling like: {str(e)}"})
