from dataclasses import dataclass
from datetime import UTC, date, datetime

from panel_api.entitlements import has_delivery_right, is_deliverable, mark_deleted


@dataclass
class Grant:
    territory: str
    surface: str
    valid_from: date
    valid_until: date | None = None
    revoked_at: datetime | None = None


@dataclass
class Asset:
    status: str
    created_at: datetime | None = None


def test_delivery_right_requires_active_unrevoked_grant() -> None:
    grant = Grant("US", "search", date(2026, 1, 1), date(2026, 12, 31))

    assert has_delivery_right([grant], "US", "search", date(2026, 7, 1))
    assert not has_delivery_right([grant], "US", "search", date(2026, 12, 31))


def test_revoked_or_quarantined_assets_are_not_deliverable() -> None:
    revoked = Grant("US", "search", date(2026, 1, 1), revoked_at=datetime.now(UTC))

    assert not has_delivery_right([revoked], "US", "search", date(2026, 7, 1))
    assert not is_deliverable(Asset(status="quarantined"), has_right=True)  # type: ignore[arg-type]


def test_deletion_marks_asset_unavailable() -> None:
    asset = Asset(status="accepted")

    mark_deleted(asset)  # type: ignore[arg-type]

    assert asset.status == "deleted"
