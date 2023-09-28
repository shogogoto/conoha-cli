"""sshkey Domain Objects."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from conoha_client.features._shared.util import now_jst

NAME_PREFIX = "conoha-client"


class KeyPair(BaseModel):
    """os-keypairs API Response Unit."""

    name: str
    public_key: str
    private_key: str | None = None

    @property
    def timestamp(self) -> str:
        """キーペア名のタイムスタンプ部分を返す."""
        return self.name.replace(f"{NAME_PREFIX}-", "")

    @classmethod
    def publish_name(cls) -> str:
        """新規登録用キーペア名を作成."""
        s = now_jst().strftime("%Y-%m-%d-%H-%M")
        return f"{NAME_PREFIX}-{s}"

    def write(self, path: str = "./") -> None:
        """キーペアをファイル出力する."""
        pri = Path(path) / f"id_rsa-{self.timestamp}"
        pub = pri.with_suffix(".pub")
        pub.write_text(self.public_key)

        if self.private_key is not None:
            pri.write_text(self.private_key)


class KeyPairAlreadyExistsError(Exception):
    """既に同一名のssh公開鍵が登録されている."""


class KeyPairNotFoundError(Exception):
    """sshキーペアが見つからない."""
