"""a Domain Model."""
from uuid import UUID

from pydantic import BaseModel, Field


class AddedVM(BaseModel, frozen=True):
    """新規追加されたVM."""

    vm_id: UUID = Field(alias="id")
