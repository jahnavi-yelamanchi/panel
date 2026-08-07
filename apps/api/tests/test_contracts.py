from datetime import date

import pytest
from pydantic import ValidationError

from panel_api.contracts import TitleManifestInput


def manifest() -> dict[str, object]:
    return {
        "partner_slug": "example-publisher",
        "partner_title_id": "title-123",
        "display_title": "Example Title",
        "source_language": "ja",
        "rights": [
            {"territory": "US", "surface": "search", "valid_from": "2026-01-01"},
        ],
    }


def test_manifest_accepts_a_future_expiry() -> None:
    payload = manifest()
    rights = payload["rights"]
    assert isinstance(rights, list)
    rights[0]["valid_until"] = "2026-12-31"

    result = TitleManifestInput.model_validate(payload)

    assert result.rights[0].valid_from == date(2026, 1, 1)


def test_manifest_rejects_expiry_on_start_date() -> None:
    payload = manifest()
    rights = payload["rights"]
    assert isinstance(rights, list)
    rights[0]["valid_until"] = "2026-01-01"

    with pytest.raises(ValidationError, match="valid_until must be after valid_from"):
        TitleManifestInput.model_validate(payload)
