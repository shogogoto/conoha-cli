"""認証周りの処理."""
import os

import requests

from . import endpoints


def env_credentials() -> dict:
    """環境変数からトークン発行用認証情報を作成する."""
    try:
        return {
            "auth": {
                "passwordCredentials": {
                    "username": os.environ["OS_USERNAME"],
                    "password": os.environ["OS_PASSWORD"],
                },
                "tenantId": os.environ["OS_TENANT_ID"],
            },
        }
    except KeyError as e:
        msg = (
            "環境変数にConoHa VPSのAPI情報を設定してください:"
            "OS_USERNAME: APIユーザー名, "
            "OS_PASSWORD: APIユーザーのパスワード, "
            "OS_TENANT_ID: テナント情報のテナントID"
        )
        raise KeyError(msg) from e


def env_region() -> str:
    """ConoHa VPSのリージョンを環境変数から取得する."""
    no_str = ""
    try:
        no_str = os.environ["OS_CONOHA_REGION_NO"]
    except KeyError as e:
        msg = (
            "環境変数OS_CONOHA_REGION_NOに"
            "ConoHa VPSのリージョン番号を指定してください"
        )
        raise KeyError(msg) from e

    if not str.isdigit(no_str):
        msg = "OS_CONOHA_REGION_NO環境変数には数字を入力してください"
        raise ValueError(msg)

    return f"tyo{no_str}"


def issue_token_id() -> str:
    """ConoHa API用のトークンを発行する."""
    url = "https://identity.tyo3.conoha.io/v2.0/tokens"
    url = endpoints.Endpoints.IDENTITY.url(env_region(), ["tokens"])
    res = requests.post(url, json=env_credentials(), timeout=3.0)
    return res.json()["access"]["token"]["id"]
