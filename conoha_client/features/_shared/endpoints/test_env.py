"""Test getting env vars."""

import os

import pytest
from _pytest.monkeypatch import MonkeyPatch

from . import environments


@pytest.mark.parametrize(
    "env_attr",
    [
        "OS_USERNAME",
        "OS_PASSWORD",
        "OS_TENANT_ID",
    ],
)
def test_invalid_env_credentials(
    monkeypatch: MonkeyPatch,
    env_attr: str,
) -> None:
    """環境変数が不足しているときにエラー."""
    if env_attr in os.environ:
        monkeypatch.delenv(env_attr)

    with pytest.raises(KeyError):
        environments.env_credentials()


def test_invalid_env_region(monkeypatch: MonkeyPatch) -> None:
    """OS_CONOHA_REGION_NOにtyo?の数字が入っているか."""
    env_attr = "OS_CONOHA_REGION_NO"

    if env_attr in os.environ:
        monkeypatch.delenv(env_attr)

    with pytest.raises(KeyError):
        environments.env_region()

    monkeypatch.setenv(env_attr, "NaN")
    with pytest.raises(ValueError, match=env_attr):
        environments.env_region()
