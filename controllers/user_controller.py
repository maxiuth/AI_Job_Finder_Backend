import uuis
from datetime import datetime, timezone
from models import user_model

def create_user(email: str, name_str):
    item = {
        "userId": str(uid.uuid4()),
        "email": email,
        "name": name,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    return user_model.create_user(item)

def get_user(user_id: str):
    return user_model.get_user(user_id)

def list_users():
    return user_model.list_users()

def update_user(user_id: str, name: str):
    return user_model.update_user(user_id, name)

def delete_user(user_id: str):
    user_model.delete_user(user_id)