# src/models/profile.py

from datetime import datetime
from sqlalchemy import String, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connector import Base
from src.models.enums import GenderEnum, SoulmateGenderEnum, EvalEnum


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), unique=True, nullable=False
    )
    nu_id: Mapped[int] = mapped_column(
        String(32), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    course: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum), nullable=False
    )
    soulmate_gender: Mapped[SoulmateGenderEnum] = mapped_column(
        Enum(SoulmateGenderEnum), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )
    photo_url: Mapped[str] = mapped_column(
        String(256), nullable=False
    )
    rating: Mapped[float] = mapped_column(
        DECIMAL(4, 2), nullable=True, default=0.00
    )
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    user: Mapped['User'] = relationship(
        "User", back_populates="profile"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "nu_id": self.nu_id,
            "course": self.course,
            "description": self.description,
            "gender": self.gender,
            "soulmate_gender": self.soulmate_gender,
            "photo_url": self.photo_url,
            "registered_at": self.registered_at,
            "rating": self.rating
        }


class ProfileHistory(Base):
    __tablename__ = "profile_history"

    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    course: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum), nullable=False
    )
    soulmate_gender: Mapped[SoulmateGenderEnum] = mapped_column(
        Enum(SoulmateGenderEnum), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    photo_url: Mapped[str] = mapped_column(
        String(256), nullable=False
    )
    rating: Mapped[float] = mapped_column(
        DECIMAL(4, 2), nullable=True, default=0.00
    )
    valid_from: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    valid_to: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "profile_id": self.profile_id,
            "name": self.name,
            "course": self.course,
            "description": self.description,
            "gender": self.gender,
            "soulmate_gender": self.soulmate_gender,
            "photo_url": self.photo_url,
            "rating": self.rating,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
        }


class ProfileEval(Base):
    __tablename__ = "profile_evaluation"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False
    )
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), nullable=False, unique=True
    )

    lover_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), nullable=False, unique=True
    )

    evaluation: Mapped[EvalEnum] = mapped_column(
        Enum(EvalEnum), nullable=False
    )
