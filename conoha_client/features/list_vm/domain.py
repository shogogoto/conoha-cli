"""VM Domain."""

from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field


class VMStatus(Enum):
    """契約中Serverの状態."""

    ACTIVE = "ACTIVE"
    SHUTOFF = "SHUTOFF"
    REBOOT = "REBOOT"
    BUILD = "BUILD"

    def is_shutoff(self) -> bool:
        """シャットダウン済みか否か."""
        return self == VMStatus.SHUTOFF


class Server(BaseModel, frozen=True):
    """契約中のサーバー."""

    name: str = Field(alias="name")
    vm_id: UUID = Field(alias="id", description="このIDに請求が紐づいている")
    status: VMStatus = Field(alias="status")
    created_at: datetime = Field(alias="created")
    updated_at: datetime = Field(alias="updated")
    image_id: UUID = Field(alias=AliasPath("image", "id"))
    flavor_id: UUID = Field(alias=AliasPath("flavor", "id"))

    # def elapsed_from_created(self) -> timedelta:
    #     """作成時からの経過時間を秒以下を省いて計算する."""
    #     return now_jst() - self.created_at
    @property
    def ipv4(self) -> IPv4Address:
        """ipv4 from name."""
        return IPv4Address(self.name.replace("-", "."))
