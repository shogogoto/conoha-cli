"""watch domain event."""

from enum import IntEnum, auto


class EventType(IntEnum):
    """domain event type."""

    STOPPED = auto()
    SAVED = auto()
    REMOVED = auto()
