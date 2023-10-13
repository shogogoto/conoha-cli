"""test repository."""


import pytest

from conoha_client.features.plan.domain import Memory
from conoha_client.features.plan.errors import FlavorIdentificationError
from conoha_client.features.plan.repo import find_vmplan


def test_invalid_find_vmplan() -> None:
    """Invalid case."""

    def mock() -> list:
        return []

    with pytest.raises(FlavorIdentificationError):
        find_vmplan(Memory.GB1, mock)
