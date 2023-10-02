"""VM Plan. API."""
from __future__ import annotations

from functools import cache

from conoha_client.features import Endpoints
from conoha_client.features._shared.domain import first_model_by
from conoha_client.features._shared.view.domain import check_include_keys

from .domain import VMPlan


@cache
def list_vmplans() -> list[VMPlan]:
    """MVプラン一覧を取得する."""
    res = Endpoints.COMPUTE.get("flavors/detail").json()
    return [VMPlan.model_validate(e) for e in res["flavors"]]


def first_vmplan_by(attr_name: str, value: any) -> VMPlan | None:
    """key-valueにマッチしたプラン情報を返す."""

    def pred(e: VMPlan) -> bool:
        check_include_keys(e, {attr_name})
        return value in str(getattr(e, attr_name))

    return first_model_by(list_vmplans(), pred)
