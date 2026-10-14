from controllers import user_controller


def sync_profile(claims: dict, name: str | None = None):
    """claims = decoded Firebase token (already verified by the auth dependency)."""
    return user_controller.get_or_create_user(
        uid=claims["uid"],
        email=claims.get("email"),
        name=name or claims.get("name"),
    )