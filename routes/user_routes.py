from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from controllers import user_controller
from dependencies.auth import get_current_user_id, require_same_user

# Creating users happens in /auth (register / sync), not here.
# There is intentionally no "list all users" endpoint: it would expose everyone's data.
router = APIRouter(prefix="/users", tags=["users"])


class UpdateUser(BaseModel):
    name: str


# /me must be declared BEFORE /{user_id}, or "me" would be treated as a user id.
@router.get("/me")
def get_me(current_user_id: str = Depends(get_current_user_id)):
    user = user_controller.get_user(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}", dependencies=[Depends(require_same_user)])
def get_user(user_id: str):
    user = user_controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", dependencies=[Depends(require_same_user)])
def update_user(user_id: str, payload: UpdateUser):
    return user_controller.update_user(user_id, payload.name)


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(require_same_user)])
def delete_user(user_id: str):
    user_controller.delete_user(user_id)
