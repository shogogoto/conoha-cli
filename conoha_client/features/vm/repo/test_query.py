"""test query."""

from __future__ import annotations

import json
from ipaddress import IPv4Address
from pathlib import Path
from typing import Callable
from uuid import UUID

import pytest

from conoha_client.features.vm.errors import NotFoundAddedVMError

from .query import find_added

VM_ID = "d9302160-27f5-42f8-8993-d2735d2b0c24"


@pytest.fixture()
def fixture_json() -> Callable[[], list[object]]:
    """list_imageのモック."""

    def func() -> list[object]:
        p = Path(__file__).resolve().parent / "fixture_servers20231006.json"
        return json.loads(p.read_text())

    return func


def test_find_ipv4(fixture_json: Callable) -> None:
    """Test."""
    added = find_added(UUID(VM_ID), dep=fixture_json)
    assert added.ipv4 == IPv4Address("157.7.78.59")


def test_invalid_find_ipv4(fixture_json: Callable) -> None:
    """Invalid case."""

    def mock_get_servers() -> list[object]:
        """2個目しか契約中VMが見つからない."""
        return [fixture_json()[1]]

    with pytest.raises(NotFoundAddedVMError):
        find_added(UUID(VM_ID), dep=mock_get_servers)
