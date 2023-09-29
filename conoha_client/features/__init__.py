"""独立した機能のあつまり."""

from conoha_client.features.add_vm import add_vm_cli
from conoha_client.features.billing import billing_cli
from conoha_client.features.image import vm_image_cli
from conoha_client.features.list_vm import list_vm_cli
from conoha_client.features.plan import vm_plan_cli
from conoha_client.features.sshkey import sshkey_cli

__all__ = [
    "sshkey_cli",
    "list_vm_cli",
    "add_vm_cli",
    "vm_plan_cli",
    "vm_image_cli",
    "billing_cli",
]
