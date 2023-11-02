"""billing domain test."""

import json
from datetime import datetime
from functools import cache
from pathlib import Path

from conoha_client.features._shared.util import TOKYO_TZ
from conoha_client.features.billing.domain import Invoice, InvoiceList


@cache
def fixture_models() -> InvoiceList:
    """Fixture."""
    p = Path(__file__).resolve().parent / "fixture_invoice.json"
    ls = [Invoice.model_validate(d) for d in json.loads(p.read_text())]
    return InvoiceList(root=ls)


def test_next_due() -> None:
    """来月の請求."""
    now = datetime(2023, 9, 1, tzinfo=TOKYO_TZ)
    next_dues = fixture_models().next_month_dues(now)
    for d in next_dues:
        assert d.due.year == 2023  # noqa: PLR2004
        assert d.due.month == 10  # noqa: PLR2004
