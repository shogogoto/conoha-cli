"""Image DTO."""


import datetime
from enum import Enum
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, RootModel, field_validator

from conoha_client.features._shared.util import utc2jst
from conoha_client.features.image.domain.errors import NeitherWindowsNorLinuxError


class ImageType(Enum):
    """VMイメージの種類."""

    SNAPSHOT = "snapshot"
    PRIOR = None  # 所与のイメージ


class OperatingSystem(RootModel):
    """OS."""

    model_config = ConfigDict(frozen=True)
    root: str

    def is_windows(self) -> bool:
        """WINDOWS OS or not."""
        return "win" in self.root[:3]

    def is_linux(self) -> bool:
        """Linux OS or not."""
        return self.root == "lin"


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str = Field(alias="name", description="名前")
    dist: str = Field("", alias=AliasPath("metadata", "dst"))
    app: str = Field("", alias=AliasPath("metadata", "app"))
    os: OperatingSystem = Field(alias=AliasPath("metadata", "os_type"))
    image_type: ImageType = Field(
        ImageType.PRIOR,
        alias=AliasPath("metadata", "image_type"),
    )
    created: str = Field(alias="created", description="作成日時")
    minDisk: int = Field(  # noqa: N815
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
