"""認証周りの処理."""

import requests

from . import endpoints
from . import environments as e


def issue_token_id() -> str:
    """ConoHa API用のトークンを発行する."""
    url = endpoints.Endpoints.IDENTITY.url("tokens")
    res = requests.post(url, json=e.env_credentials(), timeout=3.0)
    return res.json()["access"]["token"]["id"]
