"""VM Image Domain."""
from __future__ import annotations

from uuid import UUID

from pydantic import AliasPath, BaseModel, Field


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str | None = Field(alias="name", description="名前")
    dist: str | None = Field(None, alias=AliasPath("metadata", "dst"))
    app: str | None = Field(None, alias=AliasPath("metadata", "app"))
    os: str | None = Field(None, alias=AliasPath("metadata", "os_type"))
