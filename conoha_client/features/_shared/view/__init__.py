"""cli表示."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from conoha_client.features._shared.view.domain import model_filter

if TYPE_CHECKING:
    from pydantic import BaseModel


def jsonview(models: list[BaseModel], keys: set[str] | None) -> str:
    """他のCLIと連携しやすいようにserializeする.

    :param models: domain model list
    :param keys: property names for filter
    :return: json dumps
    """
    ms = [model_filter(m, keys) for m in models]
    return json.dumps(ms, indent=2)


# def tableview(models: list[BaseModel]):
#     """Decorate function returning model."""
