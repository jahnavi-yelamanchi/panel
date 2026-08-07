import uuid
from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from panel_api.contracts import (
    IngestionPackageInput,
    IngestionResponse,
    QuarantineUploadInput,
)
from panel_api.db import get_session_factory
from panel_api.ingestion import validate_uploaded_assets
from panel_api.models import Asset, AssetEvent, Partner, RightsGrant, Title
from panel_api.storage import AssetStorage

router = APIRouter(prefix="/v1", tags=["ingestion"])


def get_db() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_storage() -> AssetStorage:
    return AssetStorage()


@router.post("/uploads")
def create_quarantine_upload(
    upload: QuarantineUploadInput,
    storage: Annotated[AssetStorage, Depends(get_storage)],
) -> dict[str, str]:
    object_key = f"quarantine/{uuid.uuid4().hex}"
    return {
        "object_key": object_key,
        "upload_url": storage.presigned_quarantine_upload(
            object_key, upload.media_type, upload.sha256
        ),
    }


@router.post("/ingestions", response_model=IngestionResponse, status_code=status.HTTP_201_CREATED)
def ingest_package(
    package: IngestionPackageInput,
    db: Annotated[Session, Depends(get_db)],
    storage: Annotated[AssetStorage, Depends(get_storage)],
) -> IngestionResponse:
    try:
        validate_uploaded_assets(package.assets, storage)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error

    partner = db.scalar(select(Partner).where(Partner.slug == package.manifest.partner_slug))
    if partner is None:
        partner = Partner(slug=package.manifest.partner_slug, name=package.partner_name)
        db.add(partner)
        db.flush()

    title = db.scalar(
        select(Title).where(
            Title.partner_id == partner.id,
            Title.partner_title_id == package.manifest.partner_title_id,
        )
    )
    if title is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="partner title already ingested"
        )

    title = Title(
        partner_id=partner.id,
        partner_title_id=package.manifest.partner_title_id,
        display_title=package.manifest.display_title,
        source_language=package.manifest.source_language,
        maturity_rating=package.manifest.maturity_rating,
    )
    db.add(title)
    db.flush()

    for grant in package.manifest.rights:
        db.add(
            RightsGrant(
                title_id=title.id,
                territory=grant.territory,
                surface=grant.surface,
                valid_from=grant.valid_from,
                valid_until=grant.valid_until,
            )
        )

    assets: list[Asset] = []
    for asset_input in package.assets:
        asset = Asset(title_id=title.id, status="quarantined", **asset_input.model_dump())
        db.add(asset)
        db.flush()
        db.add(AssetEvent(asset_id=asset.id, event_type="quarantined"))
        assets.append(asset)

    db.commit()
    return IngestionResponse(
        title_id=title.id,
        asset_ids=[asset.id for asset in assets],
        status="quarantined",
    )
