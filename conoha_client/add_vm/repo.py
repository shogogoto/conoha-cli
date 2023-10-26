"""VM Create API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel

from conoha_client.add_vm.domain.domain import filter_memory, select_uniq
from conoha_client.features.image.domain.image import ImageList, LinuxImageList
from conoha_client.features.image.repo import list_images

if TYPE_CHECKING:
    from conoha_client.features.image.domain import Image

from conoha_client.features.image.domain.operating_system import (
    Distribution,  # noqa: TCH001
)
from conoha_client.features.plan.domain import Memory  # noqa: TCH001

Callback = Callable[[], LinuxImageList]


def list_linux_images() -> LinuxImageList:
    """Fix in future."""
    return ImageList(list_images()).priors.linux


class DistQuery(BaseModel, frozen=True):
    """Linux image query to add new VM."""

    memory: Memory
    dist: Distribution
    dep: Callback = list_linux_images

    def _filter_mem(self) -> LinuxImageList:
        return filter_memory(self.dep(), self.memory)

    def available_vers(self) -> set[str]:
        """List availabe distribution versions."""
        return self._filter_mem().dist_versions(self.dist)

    def latest_ver(self) -> str:
        """Latest availabe distribution version."""
        return sorted(self.available_vers())[-1]

    def apps(self, dist_ver: str) -> set[str]:
        """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
        return self._filter_mem().applications(self.dist, dist_ver)

    def identify(self, dist_ver: str, app: str) -> Image:
        """Linux Imageを一意に検索する."""
        return select_uniq(
            self.dep(),
            self.memory,
            self.dist,
            dist_ver,
            app,
        )
