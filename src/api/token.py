"""認証周りの処理."""

import requests

from . import endpoints
from .environments import env_credentials


def issue_token_id() -> str:
    """ConoHa API用のトークンを発行する."""
    url = endpoints.Endpoints.IDENTITY.url("tokens")
    res = requests.post(url, json=env_credentials(), timeout=3.0)
    return res.json()["access"]["token"]["id"]
