from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from controllers import auth_controller
from dependencies.auth import get_current_user

# There is NO /register or /login here: Firebase handles those in the React app.
# This route only links a Firebase account to a profile row in DynamoDB.
router = APIRouter(prefix="/auth", tags=["auth"])


class SyncRequest(BaseModel):
    name: str | None = Field(default=None, max_length=100)


@router.post("/sync")
def sync(payload: SyncRequest | None = None, claims: dict = Depends(get_current_user)):
    """Call once right after every login/sign-up. Creates the profile if it doesn't exist yet,
    otherwise returns the existing one."""
    return auth_controller.sync_profile(claims, payload.name if payload else None)
