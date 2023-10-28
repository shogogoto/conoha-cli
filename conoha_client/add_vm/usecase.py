"""Usecase."""
from __future__ import annotations

import click


def get_password(value: str | None) -> str:
    """VMのrootパスワードをprompt or 環境変数から取得する."""
    if value is not None:
        return value
    msg = "VMのroot userのパスワードを入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def get_sshkey_name(value: str | None) -> str | None:
    """VMのsshkeyペア名をprompt or 環境変数から取得する."""
    if value is not None:
        return value
    msg = "VMに紐付けるsshkey名を入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)
