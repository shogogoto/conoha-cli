"""add vm domain."""
from __future__ import annotations

from typing import TYPE_CHECKING

from conoha_client.features.image.domain import (
    Application,
    Distribution,
    DistVersion,
    FileSystem,
)
from conoha_client.features.image.domain.image import Image, LinuxImageList

from .errors import (
    ImageIdentifyError,
)

if TYPE_CHECKING:
    from conoha_client.features.image.domain.image import MinDisk
    from conoha_client.features.plan.domain import Memory


def allows_capacity(mindisk: MinDisk, mem: Memory) -> bool:
    """片方がsmallestの場合は許されない."""
    return not (mindisk.is_smallest() ^ mem.is_smallest())


def filter_memory(lins: LinuxImageList, mem: Memory) -> LinuxImageList:
    """RAM容量でイメージをフィルターする."""
    imgs = [img for img in lins if allows_capacity(img.min_disk, mem)]
    return LinuxImageList(imgs)


def select_uniq(
    lins: LinuxImageList,
    mem: Memory,
    dist: Distribution,
    dist_version: DistVersion,
    app: Application,
) -> Image:
    """Select uniq Image."""
    lins = filter_memory(lins, mem).filter_by_dist_version(dist, dist_version)
    lins_app = [img for img in lins if img.application == app]
    cnt_hits = len(lins_app)

    if cnt_hits != 1:
        if dist == Distribution.FREEBSD:
            # 取り合えず新型の優れてそうな方を返す
            # UFSが選びたいなら直接ID指定しろ
            return next(im for im in lins if im.fs == FileSystem.ZFS)
        msg = (
            "検索結果が一意になりませんでした"
            f":hits={cnt_hits}:{mem},{dist}:{dist_version},app={app}"
        )
        raise ImageIdentifyError(msg)
    return lins_app[0]
