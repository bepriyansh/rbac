from lib.mongodb import posts_collection, follow_relation_collection
from bson import ObjectId
from pymongo import DESCENDING
from datetime import datetime
from lib.response import successResponse, failedResponse

def create_post(user_id: str, content: str) -> dict:
    try:
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
        return successResponse(201, post)
    except Exception as e:
        return failedResponse(500, {"message": f"Error creating post: {str(e)}"})

def get_post_by_id(post_id: str) -> dict:
    try:
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            post["_id"] = str(post["_id"])
            return successResponse(200, post)
        return failedResponse(404, {"message": "Post not found."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching post: {str(e)}"})

def get_public_posts(page: int, page_size: int) -> list:
    try:
        skip = (page - 1) * page_size
        posts = posts_collection.find().sort("created_at", DESCENDING).skip(skip).limit(page_size)
        return successResponse(200, [{"_id": str(post["_id"]), **post} for post in posts])
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching posts: {str(e)}"})

def get_posts_from_following_people(user_id: str, page: int, page_size: int) -> list:
    try:
        following_ids = follow_relation_collection.find({"follower_id": user_id})
        following_ids = [relation["followed_id"] for relation in following_ids]

        skip = (page - 1) * page_size
        posts = posts_collection.find({"user_id": {"$in": following_ids}}).sort("created_at", DESCENDING).skip(skip).limit(page_size)
        return successResponse(200, [{"_id": str(post["_id"]), **post} for post in posts])
    except Exception as e:
        return failedResponse(500, {"message": f"Error fetching posts from following people: {str(e)}"})

def update_post(post_id: str, user: dict, content: str = None) -> dict:
    try:
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        if not post:
            return failedResponse(404, {"message": "Post not found."})

        if not (post["user_id"] == user["_id"] or user["role"] == "admin"):
            return failedResponse(403, {"message": "Unauthorized action."})

        update_fields = {"content": content, "updated_at": datetime.now()}
        result = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_fields})
        if result.modified_count > 0:
            return successResponse(200, {"message": "Post updated successfully."})
        return failedResponse(500, {"message": "Failed to update the post."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error updating post: {str(e)}"})

def delete_post(post_id: str, user: dict) -> dict:
    try:
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        if not post:
            return failedResponse(404, {"message": "Post not found."})

        if not (post["user_id"] == user["_id"] or user["role"] == "admin"):
            return failedResponse(403, {"message": "Unauthorized action."})

        result = posts_collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count > 0:
            return successResponse(200, {"message": "Post deleted successfully."})
        return failedResponse(500, {"message": "Failed to delete the post."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error deleting post: {str(e)}"})

def toggle_like(post_id: str, user_id: str) -> dict:
    try:
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        if not post:
            return failedResponse(404, {"message": "Post not found."})

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
        return successResponse(200, {"message": "Like status updated successfully."})
    except Exception as e:
        return failedResponse(500, {"message": f"Error toggling like: {str(e)}"})
