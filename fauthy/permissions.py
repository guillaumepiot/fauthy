from functools import wraps

from fastapi import HTTPException, status


def permissions_required(permission):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if permission not in kwargs["claims"]["permissions"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
