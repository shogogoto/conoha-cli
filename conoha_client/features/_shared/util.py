"""便利関数."""
from datetime import datetime

from dateutil import parser
from pytz import timezone

TOKYO_TZ = timezone("Asia/Tokyo")


def utc2jst(utc_str: str) -> datetime:
    """UTC文字列をJST Datetimeへ変換."""
    return parser.parse(utc_str).astimezone(TOKYO_TZ)


def now_jst() -> datetime:
    """JSTの現在時刻を取得(マイクロ秒以下はゼロ埋め)."""
    return datetime.now(TOKYO_TZ).replace(microsecond=0)


__all__ = ["utc2jst", "now_jst"]
