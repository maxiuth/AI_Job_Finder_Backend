from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers import user_controller

router = APIRouter(prefix="/users", tags=["users"])

class CreateUser(BaseModel):
    email: str
    name: str

class UpdateUser(BaseModel):
    name: str

@router.post("", status_code=201)
def create_user(payload: CreateUser):
    return user_controller.create_user(payload.email, payload.name)

@router.get("/{user_id}")
def get_user(user_id: str):
    user = user_controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("")
def list_users():
    return user_controller.list_users()

@router.patch("/{user_id}")
def update_user(user_id: str, payload: UpdateUser):
    return user_controller.update_user(user_id, payload.name)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    user_controller.delete_user(user_id)