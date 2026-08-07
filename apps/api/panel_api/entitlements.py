from collections.abc import Iterable
from datetime import date

from panel_api.models import Asset, RightsGrant


def has_delivery_right(
    grants: Iterable[RightsGrant], territory: str, surface: str, on_date: date
) -> bool:
    return any(
        grant.revoked_at is None
        and grant.surface == surface
        and grant.territory in {territory, "GLOBAL"}
        and grant.valid_from <= on_date
        and (grant.valid_until is None or grant.valid_until > on_date)
        for grant in grants
    )


def is_deliverable(asset: Asset, has_right: bool) -> bool:
    return asset.status == "accepted" and has_right


def mark_deleted(asset: Asset) -> None:
    asset.status = "deleted"
