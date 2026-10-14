import os

import firebase_admin
from firebase_admin import credentials


def init_firebase():
    """Initializes the Firebase Admin SDK once. It's only used to verify ID tokens."""
    if firebase_admin._apps:
        return

    cred_path = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        raise RuntimeError(
            "Set FIREBASE_CREDENTIALS in .env to the path of your Firebase service-account JSON "
            "(Firebase console > Project settings > Service accounts > Generate new private key)."
        )
    firebase_admin.initialize_app(credentials.Certificate(cred_path))
