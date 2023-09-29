"""VM Image Domain."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class Metadata(BaseModel, frozen=True):
    """VPSイメージのメタデータ."""

    dist: str | None = Field(
        default=None,
        alias="dst",
        description="ディストリビューション",
    )
    app: str | None = Field(default=None, alias="app", description="アプリケーション")
    # os: str | None = Field(..., alias="os_type", description="")
    # 全てlinだったので省く


class Image(BaseModel, frozen=True):
    """VPSイメージ."""

    image_id: UUID = Field(alias="id", description="イメージID")
    name: str | None = Field(alias="name", description="名前")
    metadata: Metadata = Field(alias="metadata", description="メタデータ")
