"""add VM domain test."""
from __future__ import annotations

from conoha_client.features.image.domain.image import MinDisk
from conoha_client.features.plan.domain import Memory

from .domain import allows_capacity


def test_allow_capacity() -> None:
    """cases."""
    for mem in Memory:
        if mem.is_smallest():
            assert allows_capacity(MinDisk.SMALLEST, mem)
        else:
            assert allows_capacity(MinDisk.OTHERS, mem)
