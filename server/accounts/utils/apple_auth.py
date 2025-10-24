from datetime import datetime, timedelta
import jwt  # PyJWT
from decouple import config

def generate_apple_client_secret():
    team_id = config("APPLE_TEAM_ID")
    client_id = config("APPLE_CLIENT_ID")
    key_id = config("APPLE_KEY_ID")
    private_key = config("APPLE_PRIVATE_KEY").encode()

    headers = {
        "kid": key_id,
        "alg": "ES256",
    }

    payload = {
        "iss": team_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=180),
        "aud": "https://appleid.apple.com",
        "sub": client_id,
    }

    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm="ES256",
        headers=headers
    )

    return client_secret
