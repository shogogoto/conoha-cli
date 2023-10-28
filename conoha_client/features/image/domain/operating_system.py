"""OS expression."""
from __future__ import annotations

from enum import Enum
from functools import cache
from typing import TYPE_CHECKING

from pydantic import BaseModel, RootModel

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


class Distribution(str, Enum):
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

    def version(self, image: Image) -> DistVersion:
        """Return version string."""
        self._check(image)
        sp = image.name.split("-")
        i = sp.index(self.value)
        return DistVersion(value=sp[i + 1])

    @staticmethod
    def _check(image: Image) -> None:
        if not image.os.is_linux():
            raise NotLinuxError


class DistVersion(BaseModel, frozen=True):
    """Distribution version."""

    value: str

    def is_latest(self) -> bool:
        """Is latest version."""
        return self.value == "latest"

    @classmethod
    def parse(cls, v: str) -> DistVersion:
        """Create from str."""
        return cls(value=v)


class Application(BaseModel, frozen=True):
    """Application."""

    value: str

    @classmethod
    @cache
    def null(cls) -> Application:
        """Null object pattern."""
        return cls(value="null")

    @classmethod
    def parse(cls, v: str) -> Application:
        """Create from str."""
        if v == "null":
            return cls.null()
        if v == "":
            return cls.null()
        return cls(value=v)


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
