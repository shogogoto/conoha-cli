import os
from enum import Enum


# ref: https://www.conoha.jp/docs/?btn_id=docs--sidebar_docs
class Endpoints(Enum):
    ACCOUNT  = ("account",          "v1")
    COMPUTE  = ("compute",          "v2")
    VOLUME   = ("block.storage",    "v2")
    DATABASE = ("database-hosting", "v1")
    IMAGE    = ("image-service",    "v2")
    DNS      = ("dns-service",      "v1.0")
    STORAGE  = ("object-storage",   "v1")
    IDENTITY = ("identity",         "v2.0")
    NETWORK  = ("networking",       "v2.0")

    def __init__(self, prefix:str, version:str) -> None:
        self.prefix  = prefix
        self.version = version

    def url(self, region:str, suffixes:list[str])->str:
        p = self.prefix
        v = self.version
        base = f"https://{p}.{region}.conoha.io/{v}"
        return os.path.join(base, *suffixes)
