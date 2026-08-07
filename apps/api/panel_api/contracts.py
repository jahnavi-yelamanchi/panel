from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Surface(StrEnum):
    DETAIL = "detail"
    MOODBOARD = "moodboard"
    SEARCH = "search"
    TRAINING = "training"


class MaturityRating(StrEnum):
    MATURE = "mature"
    SAFE = "safe"
    UNKNOWN = "unknown"


class RightsGrantInput(BaseModel):
    territory: str = Field(min_length=2, max_length=16)
    surface: Surface
    valid_from: date
    valid_until: date | None = None

    @model_validator(mode="after")
    def expiry_follows_start(self) -> "RightsGrantInput":
        if self.valid_until is not None and self.valid_until <= self.valid_from:
            raise ValueError("valid_until must be after valid_from")
        return self


class TitleManifestInput(BaseModel):
    partner_slug: str = Field(pattern=r"^[a-z0-9-]+$")
    partner_title_id: str = Field(min_length=1, max_length=128)
    display_title: str = Field(min_length=1, max_length=512)
    source_language: str = Field(pattern=r"^[a-z]{2,3}$")
    maturity_rating: MaturityRating = MaturityRating.UNKNOWN
    rights: list[RightsGrantInput] = Field(min_length=1)

    @model_validator(mode="after")
    def grants_are_unique(self) -> "TitleManifestInput":
        keys = {(grant.territory, grant.surface) for grant in self.rights}
        if len(keys) != len(self.rights):
            raise ValueError("rights may contain only one grant per territory and surface")
        return self


class AssetInput(BaseModel):
    object_key: str = Field(pattern=r"^quarantine/[a-z0-9][a-z0-9/_.-]*$")
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    byte_size: int = Field(gt=0)
    media_type: str = Field(pattern=r"^image/(jpeg|png|webp)$")
    original_filename: str = Field(min_length=1, max_length=512)


class QuarantineUploadInput(BaseModel):
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    media_type: str = Field(pattern=r"^image/(jpeg|png|webp)$")


class IngestionPackageInput(BaseModel):
    partner_name: str = Field(min_length=1, max_length=256)
    manifest: TitleManifestInput
    assets: list[AssetInput] = Field(min_length=1)


class IngestionResponse(BaseModel):
    title_id: UUID
    asset_ids: list[UUID]
    status: str
