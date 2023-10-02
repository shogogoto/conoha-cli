"""VM Image Domain."""
from __future__ import annotations

from uuid import UUID

from pydantic import AliasPath, BaseModel, Field


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str = Field(alias="name", description="名前")
    dist: str = Field("", alias=AliasPath("metadata", "dst"))
    app: str = Field("", alias=AliasPath("metadata", "app"))
    os: str = Field(alias=AliasPath("metadata", "os_type"))
