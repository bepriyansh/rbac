from lib.mongodb import posts_collection, follow_relation_collection
from bson import ObjectId
from pymongo import DESCENDING
from datetime import datetime

def create_post(user_id: str, content: str) -> dict:
    post = {
        "user_id": user_id,
        "content": content,
        "created_at": datetime.now(),
        "updated_at": None,
        "likes_count": 0,
        "comments_count": 0,
        "likes": []
    }
    result = posts_collection.insert_one(post)
    post["_id"] = str(result.inserted_id)
    return post

def get_post_by_id(post_id: str) -> dict:
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
    return post

def get_public_posts(page: int, page_size: int) -> list:
    skip = (page - 1) * page_size
    posts = posts_collection.find().sort("created_at", DESCENDING).skip(skip).limit(page_size)
    return [{"_id": str(post["_id"]), **post} for post in posts]

def get_posts_from_following_people(user_id: str, page: int, page_size: int) -> list:
    following_ids = follow_relation_collection.find({"follower_id": user_id})
    following_ids = [relation["followed_id"] for relation in following_ids]

    skip = (page - 1) * page_size
    posts = posts_collection.find({"user_id": {"$in": following_ids}}).sort("created_at", DESCENDING).skip(skip).limit(page_size)
    
    return [{"_id": str(post["_id"]), **post} for post in posts]

def update_post(post_id: str, user: dict, content: str = None) -> dict:
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return {"success": False, "message": "Post not found."}
    if post["user_id"] != user["_id"] or user["role"] != "admin":
        return {"success": False, "message": "Unauthorized action."}

    update_fields = {"content": content, "updated_at": datetime.now()}
    result = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_fields})
    if result.modified_count > 0:
        return {"success": True, "message": "Post updated successfully."}
    return {"success": False, "message": "Failed to update the post."}

def delete_post(post_id: str, user: dict) -> dict:
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return {"success": False, "message": "Post not found."}
    if post["user_id"] != user["_id"] or user["role"] != "admin":
        return {"success": False, "message": "Unauthorized action."}

    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count > 0:
        return {"success": True, "message": "Post deleted successfully."}
    return {"success": False, "message": "Failed to delete the post."}

def toggle_like(post_id: str, user_id: str) -> bool:
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return False
    if user_id in post["likes"]:
        posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"likes": user_id}, "$inc": {"likes_count": -1}}
        )
    else:
        posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$addToSet": {"likes": user_id}, "$inc": {"likes_count": 1}}
        )
    return True
