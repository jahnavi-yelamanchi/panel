import pytest
from panel_api.contracts import AssetInput
from pydantic import ValidationError


def test_asset_requires_quarantine_prefix_and_hash() -> None:
    asset = AssetInput(
        object_key="quarantine/example/title-1/page-001.jpg",
        sha256="a" * 64,
        byte_size=42,
        media_type="image/jpeg",
        original_filename="page-001.jpg",
    )

    assert asset.object_key.startswith("quarantine/")


def test_asset_rejects_non_quarantine_upload() -> None:
    with pytest.raises(ValidationError):
        AssetInput(
            object_key="accepted/page-001.jpg",
            sha256="a" * 64,
            byte_size=42,
            media_type="image/jpeg",
            original_filename="page-001.jpg",
        )
