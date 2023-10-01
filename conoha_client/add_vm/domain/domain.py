"""add vm domain."""
from __future__ import annotations

import operator
import re
from enum import Enum

from pydantic import BaseModel

from conoha_client.add_vm.domain.errors import ImageIdMappingMismatchWarning


# 数字始まりの変数名にできなのでアンダースコア
class Memory(str, Enum):
    """VMのメモリ容量."""

    _512MG = "0.5"
    _1GB = "1"
    _2GB = "2"
    _4GB = "4"
    _8GB = "8"
    _16GB = "16"
    _32GB = "32"
    _64GB = "64"

    @property
    def expression(self) -> str:
        """Flavor(VMプラン)を特定するための表現."""
        if self.is_smallest():
            return "m512d"
        return f"m{self.value}d"

    def is_smallest(self) -> bool:
        """最小のメモリか."""
        return self == Memory._512MG

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

    def version(self, img_name: str) -> Version:
        """VM Image名からバージョンを取得する."""
        sp = img_name.split("-")
        for_search = self.value.replace(".*", "")
        for_idx = next(filter(lambda x: for_search in x, sp))
        i = sp.index(for_idx)
        value = sp[i + 1]
        if self == OS.WINDOWS:
            value = "-".join(sp[i : i + 2])
        return Version(value=value)

    def app_with_version(self, img_name: str) -> tuple[str, str]:
        """VM Image名のvmi-{x}-{value}のxを返す."""
        res = self._regex.search(img_name)
        if res is None:
            return ("", "")
        s = res.start()
        sp = img_name[:s].split("-")  # 空文字ならNone
        tpl = tuple([e for e in sp if e != "vmi"])

        if len(tpl) == 0:
            return ("", "")
        multi = 2
        if len(tpl) > multi:
            return ("-".join(tpl[:-1]), tpl[-1])
        return tpl  # 基本len == 2になる想定


class Version(BaseModel, frozen=True):
    """VM Image OS or App Version."""

    value: str

    def is_match(self, img_name: str) -> bool:
        """イメージ名に{value}が含まれているか."""
        return self.value in img_name


class Application(BaseModel, frozen=True):
    """App for VM Image."""

    name: str
    version: str


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
        # models = []
        versions = self.available_os_versions(os)
        for v in versions:
            self.available_apps_per_os_version(os, v)
        return s

    def check_direct_sum(self) -> None:
        """OS.is_matchよってイメージ名が直和分割されるかチェック.

        OS名で利用可能なVMイメージを正しく絞るためには、
        OS名によるVMイメージのグルーピングがMECEになるべし
        dev Imageのみ例外
        """
        n = len(self.values) - 1  # Image.name == dev を除外
        cnt = 0
        for os in OS:
            cnt += len([im for im in self.values if os.is_match(im)])
        if n != cnt:
            msg = "マッピングできないimage idがありました"
            raise ImageIdMappingMismatchWarning(msg)
