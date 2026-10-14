from datetime import datetime, timezone

from botocore.exceptions import ClientError

from models import user_model


def get_user(user_id: str):
    return user_model.get_user(user_id)


def update_user(user_id: str, name: str):
    return user_model.update_user(user_id, name)


def delete_user(user_id: str):
    # Note: this only deletes the DynamoDB profile. The Firebase account itself still exists
    # (delete it with firebase_admin.auth.delete_user(uid) if you want both gone).
    user_model.delete_user(user_id)


def get_or_create_user(uid: str, email: str | None, name: str | None):
    """Called after login: creates our DynamoDB profile the first time a Firebase user shows up."""
    existing = user_model.get_user(uid)
    if existing:
        return existing

    item = {
        "userId": uid,
        "email": email,
        "name": name or (email.split("@")[0] if email else "User"),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    # DynamoDB can't store None for a missing email, so drop empty values
    item = {k: v for k, v in item.items() if v is not None}

    try:
        return user_model.create_user(item)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Two requests raced; the other one created it first
            return user_model.get_user(uid)
        raise
