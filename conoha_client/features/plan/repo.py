"""VM Plan. API."""
from __future__ import annotations

from functools import cache
from typing import Callable
from uuid import UUID

from conoha_client.features import Endpoints
from conoha_client.features._shared.model_list.domain import ModelList, by
from conoha_client.features._shared.view.domain import model_filter

from .domain import Memory, VMPlan
from .errors import FlavorIdentificationError


@cache
def list_vmplans() -> list[VMPlan]:
    """MVプラン一覧を取得する."""
    res = Endpoints.COMPUTE.get("flavors/detail").json()
    return [VMPlan.model_validate(e) for e in res["flavors"]]


def find_vmplan(
    mem: Memory,
    dep: Callable[[], list[VMPlan]] = list_vmplans,
) -> VMPlan:
    """メモリ容量からFlavor IDをみつける."""
    plans = model_filter(dep(), "name", mem.expression)
    if len(plans) != 1:
        msg = f"{mem.value}GBのプランを特定できませんでした"
        raise FlavorIdentificationError(msg)
    return plans[0]


def find_memory(flavor_id: UUID) -> Memory:
    """memoryをflavor_idから逆引き."""
    return (
        ModelList[VMPlan](root=list_vmplans())
        .find_one_by(
            by("flavor_id", flavor_id),
        )
        .memory
    )
