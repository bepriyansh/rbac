from typing import Any

def successResponse(status_code: int, data: Any) -> dict:
    """
    Returns a standardized success response.
    
    Parameters:
    - status_code: The HTTP status code to return.
    - data: The data to be returned in the response body.
    
    Returns:
    - dict: A dictionary with success = True, the status code, and the data.
    """
    return {
        "success": True,
        "status": status_code,
        "data": data
    }

def failedResponse(status_code: int, data: Any) -> dict:
    """
    Returns a standardized failure response.
    
    Parameters:
    - status_code: The HTTP status code to return.
    - data: The error message or failure data.
    
    Returns:
    - dict: A dictionary with success = False, the status code, and the error data.
    """
    return {
        "success": False,
        "status": status_code,
        "data": data
    }
