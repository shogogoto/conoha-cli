"""Image DTO."""


import datetime
from enum import Enum
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, field_validator

from conoha_client.features._shared.util import utc2jst


class ImageType(Enum):
    """VMイメージの種類."""

    SNAPSHOT = "snapshot"
    PRIOR = None


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str = Field(alias="name", description="名前")
    dist: str = Field("", alias=AliasPath("metadata", "dst"))
    app: str = Field("", alias=AliasPath("metadata", "app"))
    os: str = Field(alias=AliasPath("metadata", "os_type"))
    created: str = Field(alias="created", description="作成日時")
    minDisk: int = Field(  # noqa: N815
        alias="minDisk",
        description="インスタンス化に必要なディスク容量",
    )
    image_type: ImageType = Field(None, alias=AliasPath("metadata", "image_type"))

    @field_validator("created")
    def validate_created(cls, v: str) -> datetime:  # noqa: N805
        """Validate created datetime."""
        return utc2jst(v)
