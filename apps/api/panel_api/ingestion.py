from collections.abc import Sequence

from panel_api.contracts import AssetInput
from panel_api.storage import AssetStorage


def validate_uploaded_assets(assets: Sequence[AssetInput], storage: AssetStorage) -> None:
    for asset in assets:
        stored = storage.inspect(asset.object_key)
        if stored.byte_size != asset.byte_size:
            raise ValueError(f"asset size mismatch: {asset.object_key}")
        if stored.sha256 != asset.sha256:
            raise ValueError(f"asset checksum mismatch: {asset.object_key}")
