"""add vm domain."""
from __future__ import annotations

import operator
import re
from enum import Enum

from pydantic import BaseModel

from conoha_client.add_vm.domain.errors import (
    ApplicationUnexpectedError,
    ApplicationWithoutVersionError,
    OSVersionExtractError,
)


# 数字始まりの変数名にできなので単位をprefixにした
class Memory(str, Enum):
    """VMのメモリ容量."""

    MG512 = "0.5"
    GB1 = "1"
    GB2 = "2"
    GB4 = "4"
    GB8 = "8"
    GB16 = "16"
    GB32 = "32"
    GB64 = "64"

    @property
    def expression(self) -> str:
        """Flavor(VMプラン)を特定するための表現."""
        if self.is_smallest():
            return "m512d"
        return f"m{self.value}d"

    def is_smallest(self) -> bool:
        """最小のメモリか."""
        return self == Memory.MG512

    def is_match(self, img_name: str) -> bool:
        """valueがイメージ名に含まれているか."""
        if self.is_smallest():
            return "30gb" in img_name
        return "100gb" in img_name


class OS(str, Enum):
    """os of VM Image."""

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
    WINDOWS = "win.*"

    @property
    def _regex(self) -> re.Pattern:
        """ハイフンで挟んでいるのはarchとarchiveを区別するため."""
        return re.compile(rf"\-{self.value}-")

    def is_match(self, img_name: str) -> bool:
        """valueがイメージ名に含まれているか."""
        result = self._regex.findall(img_name)
        return len(result) > 0

    def _check_match(self, img_name: str) -> None:
        """OS名がなければエラー."""
        if not self.is_match(img_name):
            msg = f"引数の文字列にOS名{self.value}が含まれていません.:{img_name}"
            raise OSVersionExtractError(msg)

    def version(self, img_name: str) -> Version:
        """VM Image名からバージョンを取得する."""
        self._check_match(img_name)

        sp = img_name.split("-")
        for_search = self.value.replace(".*", "")
        try:
            for_idx = next(filter(lambda x: for_search in x, sp))
        except StopIteration as e:
            msg = f"{self.value}のバージョンが引数の文字列に含まれいません:{img_name}"
            raise OSVersionExtractError(msg) from e
        i = sp.index(for_idx)
        value = sp[i + 1]
        if self == OS.WINDOWS:
            value = "-".join(sp[i : i + 2])
        return Version(value=value)

    def app_with_version(self, img_name: str) -> Application:
        """VM Image名のvmi-{x}-{value}のxを返す."""
        self._check_match(img_name)
        res = self._regex.search(img_name)
        if res is None:
            return Application.none()
        s = res.start()
        sp = img_name[:s].split("-")  # 空文字ならNone
        tpl = tuple([e for e in sp if e != "vmi"])

        if len(tpl) == 0:
            return Application.none()
        if len(tpl) == 1:
            msg = f"アプリバージョンが含まれていません: {img_name}"
            raise ApplicationWithoutVersionError(msg)
        if len(tpl) == 2:  # noqa: PLR2004
            return Application(
                name=tpl[0],
                version=tpl[1],
            )
        if len(tpl) > 2:  # noqa: PLR2004
            return Application(
                name="-".join(tpl[:-1]),
                version=tpl[-1],
            )
        raise ApplicationUnexpectedError


class Version(BaseModel, frozen=True):
    """VM Image OS or App Version.

    RootModelにしないのは,
    view_optionsでlist[dict[str,str]]にパースできる必要があるため
    """

    value: str

    def is_match(self, img_name: str) -> bool:
        """イメージ名に{value}が含まれているか."""
        return self.value in img_name


class Application(BaseModel, frozen=True):
    """App for VM Image."""

    name: str
    version: str

    def is_match(self, img_name: str) -> bool:
        """イメージ名にname,versionがともに含まれているか."""
        return self.name in img_name and self.version.is_match(img_name)

    @classmethod
    def none(cls) -> Application:
        """空情報."""
        v = "NONE"
        return cls(name=v, version=v)


class ImageNames(BaseModel, frozen=True):
    """VM Image名一覧."""

    values: list[str]

    def available_os_versions(self, os: OS) -> list[Version]:
        """対応バージョン一覧を取得する."""
        s = set(filter(os.is_match, self.values))
        versions = {os.version(n) for n in s}
        return sorted(versions, key=operator.attrgetter("value"))

    def available_apps(self, os: OS) -> set[str]:
        """OS versionに対応したアプリケーション."""
        s = set(filter(os.is_match, self.values))
        versions = self.available_os_versions(os)
        for v in versions:
            self.available_apps_per_os_version(os, v)
        return s
