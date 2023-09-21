import os

import pytest

from . import credentials as C


@pytest.mark.parametrize(
    "env_attr", [
        "OS_USERNAME",
        "OS_PASSWORD",
        "OS_TENANT_ID",
    ])
def test_invalid_env_credentials(monkeypatch, env_attr):
    if env_attr in os.environ:
        monkeypatch.delenv(env_attr)

    with pytest.raises(KeyError):
        C.env_credentials()


def test_invalid_env_region(monkeypatch):
    env_attr = "OS_CONOHA_REGION_NO"

    if env_attr in os.environ:
        monkeypatch.delenv(env_attr)

    with pytest.raises(KeyError):
        C.env_region()

    monkeypatch.setenv(env_attr, "NaN")
    with pytest.raises(ValueError):
        C.env_region()

