from bson import ObjectId
from datetime import datetime
from typing import Optional
from lib.mongodb import comments_collection

def delete_replies(comment_id: str) -> None:
    replies = comments_collection.find({"parent_comment_id": comment_id})
    for reply in replies:
        delete_replies(reply["_id"]) 
    comments_collection.delete_many({"parent_comment_id": comment_id})

def delete_comment(comment_id: str, user: dict) -> bool:
    comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        return {"success": False, "message": "Comment not found."}

    if not (comment["user_id"] != user["_id"] or user["role"] != "admin"):
        return {"success": False, "message": "Unauthorized action."}

    delete_replies(comment_id)
    result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
    return {"success": result.deleted_count > 0, "message": "Comment deleted successfully."}

def create_comment(post_id: str, user_id: str, content: str, parent_comment_id: Optional[str] = None) -> dict:
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
    return comment

def get_replies(comment_id: str) -> list:
    replies = comments_collection.find({"parent_comment_id": comment_id})
    return [{"_id": str(reply["_id"]), **reply} for reply in replies]

def get_comment_by_id(comment_id: str) -> dict:
    comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
    if comment:
        comment["_id"] = str(comment["_id"])
        replies = get_replies(comment_id)
        comment["replies"] = replies
        comment["reply_count"] = len(replies)
    return comment

def toggle_like(comment_id: str, user_id: str) -> bool:
    comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        return False

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
    return {"success":True}
