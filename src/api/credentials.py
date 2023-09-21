import os
import requests

def env_credentials():
    try:
        return {
            "auth": {
                "passwordCredentials": {
                    "username": os.environ["OS_USERNAME"],
                    "password": os.environ["OS_PASSWORD"]
                },
                "tenantId": os.environ["OS_TENANT_ID"]
            }
        }
    except KeyError as e:
        msg = "環境変数にConoHa VPSのAPI情報を設定してください:" \
            + "OS_USERNAME: APIユーザー名, " \
            + "OS_PASSWORD: APIユーザーのパスワード, " \
            + "OS_TENANT_ID： テナント情報のテナントID"
        raise KeyError(msg)

def issue_token_id()->str:
    url = 'https://identity.tyo3.conoha.io/v2.0/tokens'
    res = requests.post(url, json=env_credentials())
    return res.json()["access"]["token"]["id"]
