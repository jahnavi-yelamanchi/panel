import json
from pathlib import Path

REGISTRY_PATH = Path("data/registry/datasets.json")
SOURCES_PATH = Path("data/registry/benchmark_sources.json")


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


def validate_sources(sources_document: dict[str, object]) -> None:
    sources = sources_document.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("source registry must contain at least one source")
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("source entries must be objects")
        if source.get("download_state") == "not-downloaded" and not source.get("source_url"):
            raise ValueError("downloadable source requires a source_url")


def main() -> None:
    validate_registry(json.loads(REGISTRY_PATH.read_text()))
    validate_sources(json.loads(SOURCES_PATH.read_text()))


if __name__ == "__main__":
    main()
