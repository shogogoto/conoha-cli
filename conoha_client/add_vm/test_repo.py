"""VM add repo test."""
from __future__ import annotations

import itertools
import json
from functools import cache
from pathlib import Path

from conoha_client.add_vm.domain.domain import Application
from conoha_client.features.image.domain import Image

from .domain import OS, Memory, OSVersion
from .repo import (
    find_available_os_latest_version,
    find_image_id,
    list_available_apps,
    list_available_os_versions,
)


@cache
def mock_names() -> list[str]:
    """Mock."""
    return IMAGE_NAME_SNAPSHOT_20230930


def test_list_available_os_versions() -> None:
    """Test for regression."""
    uv = list_available_os_versions(Memory.MG512, OS.UBUNTU, mock_names)
    expected = [
        OSVersion(value=v, os=OS.UBUNTU) for v in ["16.04", "20.04", "20.04.2", "22.04"]
    ]
    assert uv == expected

    uv2 = list_available_os_versions(Memory.GB64, OS.UBUNTU, mock_names)
    expected2 = [
        OSVersion(value=v, os=OS.UBUNTU)
        for v in ["16.04", "18.04", "20.04", "20.04.2", "22.04"]
    ]
    assert uv2 == expected2


def test_find_available_os_latest() -> None:
    """Test for regression."""
    v = find_available_os_latest_version(Memory.MG512, OS.UBUNTU, mock_names)
    assert v == OSVersion(value="22.04", os=OS.UBUNTU)


def test_list_available_apps() -> None:
    """Test for regression."""
    apps = list_available_apps(
        Memory.MG512,
        OS.ALMA,
        OSVersion(value="9.2", os=OS.ALMA),
        mock_names,
    )
    assert apps == [Application.none()]


def test_list_available_apps_by_latest() -> None:
    """Test for regression."""
    apps = list_available_apps(
        Memory.MG512,
        OS.UBUNTU,
        OSVersion(value="latest", os=OS.UBUNTU),
        mock_names,
    )
    assert apps == [Application.none()]


def test_find_image_id() -> None:
    """一意にimage idを見つける. 一番大事."""
    p = Path(__file__).resolve().parent / "fixture20231002.json"

    @cache
    def mock_list_images() -> list[Image]:
        return [
            Image.model_validate(
                {
                    "id": j["image_id"],
                    "name": j["name"],
                    "metadata": {
                        "dst": j["dist"],
                        "app": j["app"],
                        "os_type": j["os"],
                    },
                },
            )
            for j in json.loads(p.read_text())
        ]

    cnt = 0
    imgids = set()
    for mem, _os in itertools.product(Memory, OS):
        for os_v in list_available_os_versions(mem, _os, mock_names):
            for _app in list_available_apps(mem, _os, os_v, mock_names):
                im = find_image_id(mem, _os, os_v, _app, mock_list_images)
                imgids.add(im)
                cnt += 1

    # windowsの分を除外 -10
    # devを除外 -1
    assert len(imgids) == len(IMAGE_NAME_SNAPSHOT_20230930) - 10 - 1


IMAGE_NAME_SNAPSHOT_20230930 = [
    "vmi-gitlab-16.3.4-ubuntu-20.04-amd64-100gb",
    "vmi-rust-latest-ubuntu-20.04-amd64-100gb",
    "dev",
    "vmi-misskey-13.14.2-ubuntu-20.04-amd64-100gb",
    "vmi-7dtd-a21.1b16-ubuntu-20.04-amd64-100gb",
    "vmi-arch-20230714-amd64-100gb",
    "vmi-arch-20230714-amd64-30gb",
    "vmi-gptenginnier-0.0.7-ubuntu-20.04-amd64-100gb",
    "vmi-gptenginnier-0.0.7-ubuntu-20.04-amd64-30gb",
    "vmi-babyagi-latest-ubuntu-20.04-amd64-100gb",
    "vmi-babyagi-latest-ubuntu-20.04-amd64-30gb",
    "vmi-debian-12.0-amd64-100gb",
    "vmi-debian-12.0-amd64-30gb",
    "vmi-oraclelinux-9.2-amd64-100gb",
    "vmi-oraclelinux-9.2-amd64-30gb",
    "vmi-almalinux-9.2-amd64-100gb",
    "vmi-almalinux-9.2-amd64-30gb",
    "vmi-stablestudio-latest-ubuntu-20.04-amd64-100gb",
    "vmi-stablestudio-latest-ubuntu-20.04-amd64-30gb",
    "vmi-rockylinux-9.2-amd64-100gb",
    "vmi-rockylinux-9.2-amd64-30gb",
    "vmi-autogpt-v0.3.1-ubuntu-20.04-amd64-100gb",
    "vmi-autogpt-v0.3.1-ubuntu-20.04-amd64-30gb",
    "vmi-fedora-38-amd64-100gb",
    "vmi-fedora-38-amd64-30gb",
    "vmi-archivebox-0.2.4-ubuntu-20.04-amd64-100gb",
    "vmi-archivebox-0.2.4-ubuntu-20.04-amd64-30gb",
    "vmi-concretecms-9.2.0-ubuntu-20.04-amd64-100gb",
    "vmi-concretecms-9.2.0-ubuntu-20.04-amd64-30gb",
    "vmi-oraclelinux-8.7-amd64-100gb",
    "vmi-oraclelinux-8.7-amd64-30gb",
    "vmi-rockylinux-8.7-amd64-100gb",
    "vmi-rockylinux-8.7-amd64-30gb",
    "vmi-almalinux-8.7-amd64-100gb",
    "vmi-almalinux-8.7-amd64-30gb",
    "vmi-kusanagimanager9-0.5.2-centos-stream9-amd64-100gb",
    "vmi-drupal-10.0.5-ubuntu-20.04-amd64-100gb",
    "vmi-drupal-10.0.5-ubuntu-20.04-amd64-30gb",
    "vmi-centos-7.5-amd64-100gb",
    "vmi-centos-7.4-amd64-100gb",
    "vmi-centos-7.3-amd64-100gb",
    "vmi-centos-7.5-amd64-30gb",
    "vmi-centos-7.4-amd64-30gb",
    "vmi-centos-7.3-amd64-30gb",
    "vmi-centos-7.8-amd64-100gb",
    "vmi-centos-7.7-amd64-100gb",
    "vmi-centos-7.6-amd64-100gb",
    "vmi-centos-7.8-amd64-30gb",
    "vmi-centos-7.7-amd64-30gb",
    "vmi-centos-7.6-amd64-30gb",
    "vmi-centos-7.9-amd64-30gb",
    "vmi-centos-7.9-amd64-100gb",
    "vmi-ubuntu-20.04-amd64-100gb",
    "vmi-ubuntu-20.04-amd64-30gb",
    "vmi-oraclelinux-9.1-amd64-30gb",
    "vmi-oraclelinux-9.1-amd64-100gb",
    "vmi-mediawiki-1.39-ubuntu-20.04-amd64-30gb",
    "vmi-mediawiki-1.39-ubuntu-20.04-amd64-100gb",
    "vmi-nextcloud-25.0.3-ubuntu-20.04-amd64-100gb",
    "vmi-nextcloud-25.0.3-ubuntu-20.04-amd64-30gb",
    "vmi-rockylinux-9.1-amd64-100gb",
    "vmi-rockylinux-9.1-amd64-30gb",
    "vmi-almalinux-9.1-amd64-30gb",
    "vmi-almalinux-9.1-amd64-100gb",
    "vmi-minecraft-1.19.3-centos-7.9-amd64-100gb",
    "vmi-opensuse-15.4-amd64-30gb",
    "vmi-opensuse-15.4-amd64-100gb",
    "vmi-matomo-4.12.3-ubuntu-20.04-amd64-100gb",
    "vmi-matomo-4.12.3-ubuntu-20.04-amd64-30gb",
    "vmi-mastodon-4.0.2-ubuntu-20.04-amd64-100gb",
    "vmi-mastodon-4.0.2-ubuntu-20.04-amd64-30gb",
    "vmi-freebsd-13.1-zfs-amd64-100gb",
    "vmi-freebsd-13.1-zfs-amd64-30gb",
    "vmi-freebsd-13.1-ufs-amd64-100gb",
    "vmi-freebsd-13.1-ufs-amd64-30gb",
    "vmi-rockylinux-9.0-amd64-100gb",
    "vmi-almalinux-9.0-amd64-100gb",
    "vmi-oraclelinux-9.0-amd64-100gb",
    "vmi-rockylinux-9.0-amd64-30gb",
    "vmi-almalinux-9.0-amd64-30gb",
    "vmi-oraclelinux-9.0-amd64-30gb",
    "vmi-kusanagimanager9-0.5.1-centos-stream8-amd64-100gb",
    "vmi-ubuntu-22.04-amd64-30gb",
    "vmi-centos-stream9-amd64-30gb",
    "vmi-ubuntu-22.04-amd64-100gb",
    "vmi-centos-stream9-amd64-100gb",
    "vmi-assettocorsa-1.16-ubuntu-20.04-amd64-100gb",
    "vmi-factorio-latest-ubuntu-20.04-amd64-100gb",
    "vmi-terraria-latest-ubuntu-20.04-amd64-100gb",
    "vmi-tf2-7542465-ubuntu-20.04-amd64-100gb",
    "vmi-webmin-2.000-ubuntu-20.04-amd64-30gb",
    "vmi-webmin-2.000-ubuntu-20.04-amd64-100gb",
    "vmi-minecraftbe-latest-ubuntu-20.04-amd64-100gb",
    "vmi-minecraft-1.19.2-centos-7.9-amd64-100gb",
    "vmi-minecraft-manager-latest-1.4.1-ubuntu-20.04-amd64-100gb",
    "vmi-minecraftbe-manager-latest-1.4.1-ubuntu-20.04-amd64-100gb",
    "vmi-valheim-latest-ubuntu-20.04-amd64-100gb",
    "vmi-win-2022dce-amd64",
    "vmi-mattermost-7.0.1-ubuntu-20.04-amd64-100gb",
    "vmi-mattermost-7.0.1-ubuntu-20.04-amd64-30gb",
    "vmi-minecraft-1.19.1-centos-7.9-amd64-100gb",
    "vmi-win2019dce-rdsoffice2019",
    "vmi-win2019dce-rds",
    "vmi-win-2019dce-amd64",
    "vmi-win2016dce-rdsoffice2016",
    "vmi-win2016dce-rds",
    "vmi-win2016dce-sql2016web",
    "vmi-win-2016dce-amd64",
    "vmi-win2022dce-rdsoffice2021",
    "vmi-win2022dce-rds",
    "vmi-minecraft-1.18.0-centos-7.9-amd64-100gb",
    "vmi-kusanagimanager8-0.4.0-centos-7.9-amd64-100gb",
    "vmi-redis-5.0-centos-7.6-amd64-100gb",
    "vmi-redis-5.0-centos-7.6-amd64-30gb",
    "vmi-mongodb-4.0-centos-7.5-amd64-100gb",
    "vmi-mongodb-4.0-centos-7.5-amd64-30gb",
    "vmi-isucon7-qualify-ubuntu-16.04-amd64-100gb",
    "vmi-isucon7-qualify-ubuntu-16.04-amd64-30gb",
    "vmi-isucon8-qualify-centos-7.5-amd64-100gb",
    "vmi-isucon8-qualify-centos-7.5-amd64-30gb",
    "vmi-joomla-4.0.3-centos-7.9-amd64-100gb",
    "vmi-joomla-4.0.3-centos-7.9-amd64-30gb",
    "vmi-basercms-4.5.4-centos-7.9-amd64-100gb",
    "vmi-basercms-4.5.4-centos-7.9-amd64-30gb",
    "vmi-zbx-5.0-miraclelinux-8.4-amd64-100gb",
    "vmi-jenkins-2.289-centos-7.9-amd64-100gb",
    "vmi-jenkins-2.289-centos-7.9-amd64-30gb",
    "vmi-django-4.0.3-ubuntu-20.04.2-amd64-100gb",
    "vmi-django-4.0.3-ubuntu-20.04.2-amd64-30gb",
    "vmi-redmine-5.0.0-ubuntu-20.04-amd64-100gb",
    "vmi-redmine-5.0.0-ubuntu-20.04-amd64-30gb",
    "vmi-owncloud-10.9.1-ubuntu-20.04-amd64-100gb",
    "vmi-owncloud-10.9.1-ubuntu-20.04-amd64-30gb",
    "vmi-rails-7.0.2.3-ubuntu-20.04.2-amd64-100gb",
    "vmi-rails-7.0.2.3-ubuntu-20.04.2-amd64-30gb",
    "vmi-zabbix-6.0-ubuntu-20.04-amd64-100gb",
    "vmi-zabbix-6.0-ubuntu-20.04-amd64-30gb",
    "vmi-lemp-latest-ubuntu-20.04-amd64-100gb",
    "vmi-lemp-latest-ubuntu-20.04-amd64-30gb",
    "vmi-laravel-9.2.0-ubuntu-20.04-amd64-100gb",
    "vmi-laravel-9.2.0-ubuntu-20.04-amd64-30gb",
    "vmi-cacti-nagios-1.2.17.4.4.6-centos-7.9-amd64-100gb",
    "vmi-cacti-nagios-1.2.17.4.4.6-centos-7.9-amd64-30gb",
    "vmi-prometheus-grafana-2.30.3-8.2.1-ubuntu-20.04-amd64-100gb",
    "vmi-prometheus-grafana-2.30.3-8.2.1-ubuntu-20.04-amd64-30gb",
    "vmi-nodejs-17.4.0-ubuntu-20.04-amd64-100gb",
    "vmi-nodejs-17.4.0-ubuntu-20.04-amd64-30gb",
    "vmi-dokku-0.27.5-ubuntu-20.04-amd64-100gb",
    "vmi-dokku-0.27.5-ubuntu-20.04-amd64-30gb",
    "vmi-kusanagi-latest-centos-7.8-amd64-100gb",
    "vmi-kusanagi-latest-centos-7.8-amd64-30gb",
    "vmi-kusanagi9-9.0.9-centos-8-amd64-100gb",
    "vmi-kusanagi9-9.0.9-centos-8-amd64-30gb",
    "vmi-metabase-0.41.5-ubuntu-20.04-amd64-100gb",
    "vmi-metabase-0.41.5-ubuntu-20.04-amd64-30gb",
    "vmi-lamp-latest-ubuntu-20.04-amd64-100gb",
    "vmi-lamp-latest-ubuntu-20.04-amd64-30gb",
    "vmi-docker-20.10-ubuntu-20.04-amd64-100gb",
    "vmi-docker-20.10-ubuntu-20.04-amd64-30gb",
    "vmi-jitsi-2.0.5142-ubuntu-18.04-amd64-100gb",
    "vmi-ark-346.12-ubuntu-20.04-amd64-100gb",
    "vmi-minecraft-1.12.2-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.13.0-centos-7.5-amd64-100gb",
    "vmi-minecraft-1.13.1-centos-7.5-amd64-100gb",
    "vmi-minecraft-1.13.2-centos-7.5-amd64-100gb",
    "vmi-minecraft-1.14.0-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.14.1-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.14.2-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.14.3-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.14.4-centos-7.6-amd64-100gb",
    "vmi-minecraft-1.15.0-centos-7.7-amd64-100gb",
    "vmi-minecraft-1.15.1-centos-7.7-amd64-100gb",
    "vmi-minecraft-1.15.2-centos-7.7-amd64-100gb",
    "vmi-minecraft-1.16.0-centos-7.8-amd64-100gb",
    "vmi-minecraft-1.16.1-centos-7.8-amd64-100gb",
    "vmi-minecraft-1.16.2-centos-7.8-amd64-100gb",
    "vmi-minecraft-1.16.3-centos-7.8-amd64-100gb",
    "vmi-minecraft-1.16.4-centos-7.8-amd64-100gb",
    "vmi-minecraft-1.16.5-centos-7.9-amd64-100gb",
    "vmi-minecraft-1.17.0-centos-7.9-amd64-100gb",
    "vmi-minecraft-1.17.1-centos-7.9-amd64-100gb",
    "vmi-minecraft-1.18.1-centos-7.9-amd64-100gb",
    "vmi-minecraft-1.18.2-centos-7.9-amd64-100gb",
    "vmi-minecraft-1.19.0-centos-7.9-amd64-100gb",
    "vmi-netbsd-9.1-amd64-30gb",
    "vmi-netbsd-9.1-amd64-100gb",
    "vmi-openbsd-7.0-amd64-30gb",
    "vmi-openbsd-7.0-amd64-100gb",
    "vmi-centos-7.1-amd64-30gb",
    "vmi-centos-7.1-amd64-100gb",
    "vmi-centos-7.2-amd64-30gb",
    "vmi-centos-7.2-amd64-100gb",
    "vmi-oraclelinux-8.3-amd64-100gb",
    "vmi-oraclelinux-8.3-amd64-30gb",
    "vmi-almalinux-8.3-amd64-100gb",
    "vmi-almalinux-8.3-amd64-30gb",
    "vmi-almalinux-8.4-amd64-100gb",
    "vmi-almalinux-8.4-amd64-30gb",
    "vmi-oraclelinux-8.4-amd64-100gb",
    "vmi-oraclelinux-8.4-amd64-30gb",
    "vmi-debian-11.0-amd64-100gb",
    "vmi-debian-11.0-amd64-30gb",
    "vmi-centos-stream-8-latest-amd64-100gb",
    "vmi-centos-stream-8-latest-amd64-30gb",
    "vmi-debian-10.10-amd64-100gb",
    "vmi-debian-10.10-amd64-30gb",
    "vmi-rockylinux-8.5-amd64-100gb",
    "vmi-rockylinux-8.5-amd64-30gb",
    "vmi-almalinux-8.5-amd64-100gb",
    "vmi-almalinux-8.5-amd64-30gb",
    "vmi-rockylinux-8.4-amd64-100gb",
    "vmi-rockylinux-8.4-amd64-30gb",
    "vmi-oraclelinux-8.5-amd64-100gb",
    "vmi-oraclelinux-8.5-amd64-30gb",
    "vmi-miraclelinux-8.4-amd64-100gb",
    "vmi-miraclelinux-8.4-amd64-30gb",
    "vmi-rockylinux-8.6-amd64-100gb",
    "vmi-rockylinux-8.6-amd64-30gb",
    "vmi-almalinux-8.6-amd64-100gb",
    "vmi-almalinux-8.6-amd64-30gb",
    "vmi-oraclelinux-8.6-amd64-100gb",
    "vmi-oraclelinux-8.6-amd64-30gb",
]
