"""VM Create API."""
from __future__ import annotations

from functools import cache
from operator import attrgetter
from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel

from conoha_client.features.image.domain.image import LinuxImageList
from conoha_client.features.image.repo import list_images
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand

from .domain import filter_memory, select_uniq

if TYPE_CHECKING:
    from conoha_client.features.image.domain import (
        Application,
        DistVersion,
        Image,
    )

from conoha_client.features.image.domain import (
    Distribution,  # noqa: TCH001
)
from conoha_client.features.plan.domain import Memory  # noqa: TCH001

Callback = Callable[[], LinuxImageList]


def list_linux_images() -> LinuxImageList:
    """Find linux images."""
    return list_images().priors.linux


@cache
def _filter_memory(
    dep: Callable,
    memory: Memory,
) -> LinuxImageList:
    """For cache without memory leak."""
    return filter_memory(dep(), memory)


@cache
def _available_vers(
    dep: Callable,
    memory: Memory,
    dist: Distribution,
) -> set[DistVersion]:
    """For cache without memory leak."""
    return _filter_memory(dep, memory).dist_versions(dist)


class DistQuery(BaseModel, frozen=True):
    """Linux image query to add new VM."""

    memory: Memory
    dist: Distribution
    dep: Callback = list_linux_images

    def _filter_mem(self) -> LinuxImageList:
        return _filter_memory(self.dep, self.memory)

    def available_vers(self) -> set[DistVersion]:
        """List availabe distribution versions."""
        return _available_vers(self.dep, self.memory, self.dist)
        # return self._filter_mem().dist_versions(self.dist)

    def latest_ver(self) -> DistVersion:
        """Latest availabe distribution version."""
        return sorted(self.available_vers(), key=attrgetter("value"))[-1]

    def apps(self, dist_ver: DistVersion) -> set[Application]:
        """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
        if dist_ver.is_latest():
            dist_ver = self.latest_ver()
        return self._filter_mem().applications(self.dist, dist_ver)

    def identify(
        self,
        dist_ver: DistVersion,
        app: Application,
    ) -> Image:
        """Linux Imageを一意に検索する."""
        if dist_ver.is_latest():
            dist_ver = self.latest_ver()

        return select_uniq(
            self.dep(),
            self.memory,
            self.dist,
            dist_ver,
            app,
        )


def add_vm_command(
    memory: Memory,
    dist: Distribution,
    ver: DistVersion,
    app: Application,
    admin_pass: str,
) -> AddVMCommand:
    """Add VM Command with identified Image."""
    q = DistQuery(memory=memory, dist=dist)
    img = q.identify(ver, app)
    return AddVMCommand(
        flavor_id=find_vmplan(memory).flavor_id,
        image_id=img.image_id,
        admin_pass=admin_pass,
    )
