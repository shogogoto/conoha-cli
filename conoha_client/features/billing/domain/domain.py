"""請求ドメイン."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from conoha_client.features._shared.util import TOKYO_TZ


class Deposit(BaseModel, frozen=True):
    """入金."""

    amount: int = Field(alias="deposit_amount")
    money_type: str = Field(alias="money_type")
    received: datetime = Field(alias="received_date")

    @field_validator("received")
    def validate(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate datetime."""
        return v.astimezone(TOKYO_TZ)
