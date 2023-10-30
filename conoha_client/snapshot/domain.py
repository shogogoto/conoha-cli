"""snapshot domain."""


from typing import Any, Callable

from conoha_client.features.image.domain.image import Image


def by(attr: str, value: Any) -> Callable[[Image], bool]:  # noqa: ANN401
    """Create image predicate."""

    def pred(img: Image) -> bool:
        return getattr(img, attr) == value

    return pred
