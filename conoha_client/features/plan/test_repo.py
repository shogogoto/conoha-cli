"""test repository."""


import pytest

from .domain import Memory
from .errors import FlavorIdentificationError
from .repo import find_vmplan


def test_invalid_find_vmplan() -> None:
    """Invalid case."""

    def mock() -> list:
        return []

    with pytest.raises(FlavorIdentificationError):
        find_vmplan(Memory.GB1, mock)
