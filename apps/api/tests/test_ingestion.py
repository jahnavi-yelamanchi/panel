import pytest
from panel_api.contracts import AssetInput
from panel_api.ingestion import validate_uploaded_assets
from panel_api.storage import StoredObject


class FakeStorage:
    def __init__(self, stored: StoredObject) -> None:
        self.stored = stored

    def inspect(self, object_key: str) -> StoredObject:
        return self.stored


def asset() -> AssetInput:
    return AssetInput(
        object_key="quarantine/example/title-1/page-001.jpg",
        sha256="a" * 64,
        byte_size=42,
        media_type="image/jpeg",
        original_filename="page-001.jpg",
    )


def test_uploaded_asset_must_match_declared_provenance() -> None:
    validate_uploaded_assets([asset()], FakeStorage(StoredObject(byte_size=42, sha256="a" * 64)))


def test_uploaded_asset_rejects_checksum_mismatch() -> None:
    with pytest.raises(ValueError, match="checksum mismatch"):
        validate_uploaded_assets(
            [asset()], FakeStorage(StoredObject(byte_size=42, sha256="b" * 64))
        )
