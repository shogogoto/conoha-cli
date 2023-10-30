import pytest
from pydantic import BaseModel

from conoha_client.features._shared.model_list.domain import (
    BaseList,
    MultipleMatchError,
    NotMatchError,
    by,
)
from conoha_client.features._shared.view.domain import ExtraKeyError


class TestModel(BaseModel, frozen=True):
    """test model."""

    x: str
    y: str


class TestList(BaseList[TestModel]):
    """test model list."""


@pytest.fixture()
def nums() -> TestList:
    """Fixture."""
    ls = []
    for i, e in enumerate(range(5)):
        ls.append(TestModel(x=str(i), y=str(e * 2)))
    return TestList(root=ls)


@pytest.fixture()
def duplicate() -> TestList:
    """Fixture."""
    ls = [(TestModel(x="dup", y="same")) for _ in range(3)]
    return TestList(root=ls)


def test_find_one_by(nums: TestList) -> None:
    """Valid case."""
    assert nums.find_one_by(by("x", "1")) == nums[1]
    assert nums.find_one_or_none_by(by("x", "1")) == nums[1]


def test_no_one(nums: TestList) -> None:
    """Test case."""
    pred = by("x", "999")
    with pytest.raises(NotMatchError):
        nums.find_one_by(pred)

    assert nums.find_one_or_none_by(pred) is None


def test_extra_attr(nums: TestList) -> None:
    """Invalid case."""
    with pytest.raises(ExtraKeyError):
        nums.find_one_by(by("extra", 999))
    with pytest.raises(ExtraKeyError):
        nums.find_one_or_none_by(by("extra", 999))


def test_multi_match(duplicate: TestList) -> None:
    """Invalid case."""
    with pytest.raises(MultipleMatchError):
        duplicate.find_one_by(by("y", "same"))

    with pytest.raises(MultipleMatchError):
        duplicate.find_one_or_none_by(by("y", "same"))
