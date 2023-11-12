"""watch domain event."""

from datetime import datetime
from enum import IntEnum, auto
from uuid import UUID

from pydantic import BaseModel, Field

from conoha_client.features._shared.util import now_jst


class EventType(IntEnum):
    """domain event type."""

    STOPPED = auto()
    SAVED = auto()
    REMOVED = auto()


class VMWatchEvent(BaseModel, frozen=True):
    """VM event by Watcher."""

    ev_type: EventType
    vm_id: UUID
    occurred: datetime = Field(default_factory=now_jst)


class VMStopped(VMWatchEvent, frozen=True):
    """VM was stopped by watcher."""

    ev_type: EventType = EventType.STOPPED


class VMSaved(VMWatchEvent, frozen=True):
    """VM was snapshot by watcher."""

    ev_type: EventType = EventType.SAVED
    snapshot_id: UUID


class VMRemoved(VMWatchEvent, frozen=True):
    """VM was removed by watcher."""

    ev_type: EventType = EventType.REMOVED
