"""OS expression."""
from __future__ import annotations

from enum import Enum

from pydantic import RootModel


class OperatingSystem(RootModel, frozen=True):
    """OS.

    Enumにしなかった理由:
    windowsを表す文字列表現が複数あったため
    """

    root: str

    def is_windows(self) -> bool:
        """WINDOWS OS or not."""
        return "win" in self.root[:3]

    def is_linux(self) -> bool:
        """Linux OS or not."""
        return self.root == "lin"


class FileSystem(Enum):
    """Imageのファイルシステム."""

    UFS = "ufs"  # UNIX由来の伝統的なやつ
    ZFS = "zfs"  # 次世代
    UNKNOWN = ""

    @classmethod
    def parse(cls, value: str) -> FileSystem:
        """Instantiate."""
        if cls.UFS.value in value:
            return cls.UFS
        if cls.ZFS.value in value:
            return cls.ZFS
        return cls.UNKNOWN
