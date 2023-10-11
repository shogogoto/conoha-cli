"""VM Image Domain."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, field_validator

from conoha_client.features._shared.util import utc2jst


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

    @field_validator("created")
    def validate_created(cls, v: str) -> datetime:  # noqa: N805
        """Validate created datetime."""
        return utc2jst(v)
