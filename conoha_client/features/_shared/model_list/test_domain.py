import pytest
from pydantic import BaseModel

from conoha_client.features._shared.model_list.domain import (
    BaseList,
    MultipleMatchError,
    NotMatchError,
    by,
)
from conoha_client.features._shared.view.domain import ExtraKeyError


class OneModel(BaseModel, frozen=True):
    """test model."""

    x: str
    y: str


class OneList(BaseList[OneModel]):
    """test model list."""


@pytest.fixture()
def nums() -> OneList:
    """Fixture."""
    ls = []
    for i, e in enumerate(range(5)):
        ls.append(OneModel(x=str(i), y=str(e * 2)))
    return OneList(root=ls)


@pytest.fixture()
def duplicate() -> OneList:
    """Fixture."""
    ls = [(OneModel(x="dup", y="same")) for _ in range(3)]
    return OneList(root=ls)


def test_find_one_by(nums: OneList) -> None:
    """Valid case."""
    assert nums.find_one_by(by("x", "1")) == nums[1]
    assert nums.find_one_or_none_by(by("x", "1")) == nums[1]


def test_no_one(nums: OneList) -> None:
    """Test case."""
    pred = by("x", "999")
    with pytest.raises(NotMatchError):
        nums.find_one_by(pred)

    assert nums.find_one_or_none_by(pred) is None


def test_extra_attr(nums: OneList) -> None:
    """Invalid case."""
    with pytest.raises(ExtraKeyError):
        nums.find_one_by(by("extra", 999))
    with pytest.raises(ExtraKeyError):
        nums.find_one_or_none_by(by("extra", 999))


def test_multi_match(duplicate: OneList) -> None:
    """Invalid case."""
    with pytest.raises(MultipleMatchError):
        duplicate.find_one_by(by("y", "same"))

    with pytest.raises(MultipleMatchError):
        duplicate.find_one_or_none_by(by("y", "same"))