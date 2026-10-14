import logging

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as fb_auth

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """Verifies the Firebase ID token sent by React and returns its decoded claims.

    Useful claims: uid, email, email_verified, name (if the user has a display name).
    """
    if creds is None:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return fb_auth.verify_id_token(creds.credentials)
    except (
        ValueError,
        fb_auth.InvalidIdTokenError,
        fb_auth.ExpiredIdTokenError,
        fb_auth.RevokedIdTokenError,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except fb_auth.CertificateFetchError:
        logger.exception("Could not fetch Google's public keys to verify the token")
        raise HTTPException(status_code=503, detail="Auth service temporarily unavailable")


def get_current_user_id(user: dict = Depends(get_current_user)) -> str:
    return user["uid"]  # the Firebase uid is our userId in DynamoDB


def require_same_user(user_id: str, current_user_id: str = Depends(get_current_user_id)) -> str:
    """For routes shaped like /users/{user_id}/...: the URL's user must be the logged-in user."""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only access your own data")
    return current_user_id
