import json
from pathlib import Path

import pytest

from scripts.validate_dataset_registry import validate_registry


def test_registry_allows_only_partner_catalog_data() -> None:
    registry = json.loads(Path("data/registry/datasets.json").read_text())

    validate_registry(registry)


def test_registry_rejects_unlicensed_catalog_data() -> None:
    with pytest.raises(ValueError, match="only partner-licensed"):
        validate_registry(
            {
                "datasets": [
                    {"id": "manga109", "production_catalog": True},
                ]
            }
        )
