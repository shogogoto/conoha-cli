"""便利関数."""
from datetime import datetime

from dateutil import parser
from pytz import timezone


def utc2jst(utc_str: str) -> datetime:
    """UTC文字列をJST Datetimeへ変換."""
    tz = timezone("Asia/Tokyo")
    return parser.parse(utc_str) \
            .astimezone(tz)
