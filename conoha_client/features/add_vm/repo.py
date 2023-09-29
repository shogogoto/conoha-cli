"""VM Create API."""


from conoha_client.features._shared import Endpoints


def add_vm() -> None:
    """新規VM追加."""
    Endpoints.COMPUTE.post("servers")
