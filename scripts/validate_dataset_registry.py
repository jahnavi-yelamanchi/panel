import json
from pathlib import Path

REGISTRY_PATH = Path("data/registry/datasets.json")


def validate_registry(registry: dict[str, object]) -> None:
    datasets = registry.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        raise ValueError("registry must contain at least one dataset")

    ids: set[str] = set()
    for dataset in datasets:
        if not isinstance(dataset, dict):
            raise ValueError("dataset entries must be objects")
        dataset_id = dataset.get("id")
        if not isinstance(dataset_id, str) or not dataset_id:
            raise ValueError("dataset id is required")
        if dataset_id in ids:
            raise ValueError(f"duplicate dataset id: {dataset_id}")
        ids.add(dataset_id)
        if dataset.get("production_catalog") and dataset.get("id") != "partner-licensed":
            raise ValueError("only partner-licensed may be used in the production catalog")


def main() -> None:
    validate_registry(json.loads(REGISTRY_PATH.read_text()))


if __name__ == "__main__":
    main()

