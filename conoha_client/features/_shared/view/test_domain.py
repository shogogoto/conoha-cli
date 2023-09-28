from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel

from .domain import ExtraKeyError, model_filter


class TestModel(BaseModel):
    """for test."""

    x: str
    y: UUID


def test_model_filter() -> None:
    """Valid test."""
    m = TestModel(x="x", y=uuid4())
    assert model_filter(m, {"x"}) == {"x": "x"}
    assert model_filter(m, {"y"}) == {"y": str(m.y)}
    assert model_filter(m) == {"x": "x", "y": str(m.y)}


def test_invalid_model_filter() -> None:
    """Invalid test."""
    m = TestModel(x="x", y=uuid4())
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"extra"})
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"x", "extra"})
