import pytest
from fastapi.testclient import TestClient
from panel_api.contracts import AssetInput
from panel_api.ingestion import validate_uploaded_assets
from panel_api.main import app
from panel_api.routes.ingestion import get_storage
from panel_api.storage import StoredObject


class FakeStorage:
    def __init__(self, stored: StoredObject) -> None:
        self.stored = stored

    def inspect(self, object_key: str) -> StoredObject:
        return self.stored

    def presigned_quarantine_upload(self, object_key: str, media_type: str, sha256: str) -> str:
        return f"https://uploads.example/{object_key}?sha256={sha256}"


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


def test_quarantine_upload_returns_an_opaque_quarantine_key() -> None:
    storage = FakeStorage(StoredObject(byte_size=0, sha256=""))
    app.dependency_overrides[get_storage] = lambda: storage
    try:
        response = TestClient(app).post(
            "/v1/uploads",
            json={"sha256": "a" * 64, "media_type": "image/jpeg"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["object_key"].startswith("quarantine/")
