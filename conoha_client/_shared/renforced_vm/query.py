"""query VM with detail info."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from conoha_client.features._shared.model_list.domain import ModelList, by
from conoha_client.features.image.repo import list_images
from conoha_client.features.plan.domain import VMPlan
from conoha_client.features.plan.repo import list_vmplans
from conoha_client.features.vm.repo.query import list_vms

from .domain import ReinforcedVM

if TYPE_CHECKING:
    from conoha_client.features.image.domain.image import Image


def list_reinforced_vms() -> list[ReinforcedVM]:
    """List vm."""
    ls = []
    vms = list_vms()
    for vm in reversed(vms):
        d = (
            vm.model_dump()
            | find_image(vm.image_id).model_dump()
            | find_vmplan(vm.flavor_id).model_dump()
        )
        d["ipv4"] = vm.ipv4
        d["elapsed"] = vm.elapsed_from_created()
        ls.append(ReinforcedVM.model_validate(d))
    return ls


def find_reinforced_vm_by_id(vm_id: UUID) -> ReinforcedVM:
    return ModelList[ReinforcedVM](root=list_reinforced_vms()).find_one_by(
        by("vm_id", vm_id),
    )


def find_image(image_id: UUID) -> Image:
    """Find image by id."""
    return list_images().find_one_by(by("image_id", image_id))


def find_vmplan(flavor_id: UUID) -> VMPlan:
    """Find VMplan by id."""
    return ModelList[VMPlan](root=list_vmplans()).find_one_by(
        by("flavor_id", flavor_id),
    )
