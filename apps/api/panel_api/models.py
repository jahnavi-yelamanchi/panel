import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Partner(Base):
    __tablename__ = "partners"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    titles: Mapped[list["Title"]] = relationship(back_populates="partner")


class Title(Base):
    __tablename__ = "titles"
    __table_args__ = (UniqueConstraint("partner_id", "partner_title_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("partners.id"), index=True)
    partner_title_id: Mapped[str] = mapped_column(String(128))
    display_title: Mapped[str] = mapped_column(String(512))
    source_language: Mapped[str] = mapped_column(String(3))
    maturity_rating: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    partner: Mapped[Partner] = relationship(back_populates="titles")
    rights: Mapped[list["RightsGrant"]] = relationship(back_populates="title")


class RightsGrant(Base):
    __tablename__ = "rights_grants"
    __table_args__ = (UniqueConstraint("title_id", "territory", "surface", "valid_from"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("titles.id"), index=True)
    territory: Mapped[str] = mapped_column(String(16), index=True)
    surface: Mapped[str] = mapped_column(String(32), index=True)
    valid_from: Mapped[date] = mapped_column(Date)
    valid_until: Mapped[date | None] = mapped_column(Date)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    title: Mapped[Title] = relationship(back_populates="rights")
