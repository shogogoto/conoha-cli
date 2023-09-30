"""VM Plan. API."""
from __future__ import annotations

from functools import cache

from conoha_client.features import Endpoints
from conoha_client.features._shared.domain import find_by_included_prop

from .domain import VMPlan


@cache
def list_vmplans() -> list[VMPlan]:
    """MVプラン一覧を取得する."""
    res = Endpoints.COMPUTE.get("flavors/detail").json()
    return [VMPlan.model_validate(e) for e in res["flavors"]]


def find_vmplan_by(attr_name: str, value: any) -> VMPlan | None:
    """key-valueにマッチしたプラン情報を返す."""
    return find_by_included_prop(list_vmplans(), attr_name, value)
