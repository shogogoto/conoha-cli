"""snapshot repository."""


from conoha_client.features.image.domain.image import ImageList
from conoha_client.features.image.repo import list_images


def list_snapshots() -> ImageList:
    """List snapshots."""
    return list_images().snapshots
