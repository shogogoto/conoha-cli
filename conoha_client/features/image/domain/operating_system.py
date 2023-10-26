"""OS expression."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import RootModel

from conoha_client.features.image.domain.errors import (
    DistributionNotFoundInImageNameError,
    NotLinuxError,
)

if TYPE_CHECKING:
    from conoha_client.features.image.domain.image import Image

# from .errors import OSIdentificationError


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


class Distribution(Enum):
    """linux distribution."""

    CENTOS = "centos"
    UBUNTU = "ubuntu"
    DEBIAN = "debian"
    ROCKY = "rockylinux"
    ALMA = "almalinux"
    ORACLE = "oraclelinux"
    MIRACLE = "miraclelinux"
    FREEBSD = "freebsd"
    FEDORA = "fedora"
    OPENSUKE = "opensuse"
    ARCH = "arch"
    NETBSD = "netbsd"
    OPENBSD = "openbsd"

    @classmethod
    def create(cls, image: Image) -> Distribution:
        """instantiate."""
        cls._check(image)
        for dist in Distribution:
            if dist.value in image.name:
                return dist
        msg = f"{image.name}からlinuxディストリビューションが見つかりませんでした"
        raise DistributionNotFoundInImageNameError(msg)

    def version(self, image: Image) -> str:
        """Return version string."""
        self._check(image)
        sp = image.name.split("-")
        i = sp.index(self.value)
        return sp[i + 1]

    @staticmethod
    def _check(image: Image) -> None:
        if not image.os.is_linux():
            raise NotLinuxError


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
