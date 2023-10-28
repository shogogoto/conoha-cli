"""Image DTO."""
from __future__ import annotations

import datetime
from enum import Enum
from functools import cached_property
from typing import Iterator
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, RootModel, field_validator

from conoha_client.features._shared.util import utc2jst
from conoha_client.features.image.domain.errors import NeitherWindowsNorLinuxError

from .operating_system import (
    Application,
    Distribution,
    DistVersion,
    FileSystem,
    OperatingSystem,
)


class ImageType(Enum):
    """VMイメージの種類."""

    SNAPSHOT = "snapshot"
    PRIOR = None  # 所与のイメージ


class MinDisk(Enum):
    """image container precondition."""

    SMALLEST = 30
    OTHERS = 100

    def is_smallest(self) -> bool:
        """Smallest."""
        return self == MinDisk.SMALLEST


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str = Field(alias="name", description="名前")
    dist: str = Field("", alias=AliasPath("metadata", "dst"))
    app: str = Field("null", alias=AliasPath("metadata", "app"))
    os: OperatingSystem = Field(alias=AliasPath("metadata", "os_type"))
    image_type: ImageType = Field(
        ImageType.PRIOR,
        alias=AliasPath("metadata", "image_type"),
    )
    created: str = Field(alias="created", description="作成日時")
    min_disk: MinDisk = Field(
        alias="minDisk",
        description="インスタンス化に必要なディスク容量",
    )

    @field_validator("created")
    def validate_created(cls, v: str) -> datetime:  # noqa: N805
        """Validate created datetime."""
        return utc2jst(v)

    @field_validator("os")
    def validate_os(cls, v: OperatingSystem) -> OperatingSystem:  # noqa: N805
        """OS type must be linux or windows."""
        if not (v.is_windows() or v.is_linux()):
            raise NeitherWindowsNorLinuxError
        return v

    @cached_property
    def fs(self) -> FileSystem:
        """File system."""
        return FileSystem.parse(self.name)


class BaseList(RootModel, frozen=True):
    """base."""

    root: list[Image]

    def __iter__(self) -> Iterator[Image]:
        """Behavior like list."""
        return iter(self.root)

    def __next__(self) -> Image:
        """Behavior like list."""
        return next(self.root)

    def __len__(self) -> int:
        """Count of elements."""
        return len(self.root)


class ImageList(BaseList):
    """イメージコンテナ."""

    @cached_property
    def priors(self) -> ImageList:
        """所与のイメージを返す."""
        ls = [img for img in self.root if img.image_type == ImageType.PRIOR]
        return ImageList(ls)

    @cached_property
    def snapshots(self) -> ImageList:
        """スナップショットを返す."""
        ls = [img for img in self.root if img.image_type == ImageType.SNAPSHOT]
        return ImageList(ls)

    @cached_property
    def windows(self) -> ImageList:
        """Filter windows os."""
        ls = [img for img in self.root if img.os.is_windows()]
        return ImageList(ls)

    @cached_property
    def linux(self) -> LinuxImageList:
        """Filter linux os."""
        ls = [img for img in self.root if img.os.is_linux()]
        return LinuxImageList(ls)


class LinuxImageList(BaseList):
    """linux image container."""

    root: list[Image]

    def filter_by_dist(self, dist: Distribution) -> LinuxImageList:
        """Filter by dist."""
        ls = [img for img in self.root if Distribution.create(img) == dist]
        return LinuxImageList(ls)

    def dist_versions(self, dist: Distribution) -> set[DistVersion]:
        """Dist versions set."""
        imgs = self.filter_by_dist(dist).root
        return {dist.version(img) for img in imgs}

    def filter_by_dist_version(
        self,
        dist: Distribution,
        dist_version: DistVersion,
    ) -> LinuxImageList:
        """Filter by dist with version."""
        ls = self.filter_by_dist(dist).root
        imgs = {img for img in ls if dist.version(img) == dist_version}
        return LinuxImageList(imgs)

    def applications(
        self,
        dist: Distribution,
        dist_version: DistVersion,
    ) -> set[Application]:
        """Available application for distribution."""
        ls = self.filter_by_dist_version(dist, dist_version)
        return {Application.parse(img) for img in ls}
