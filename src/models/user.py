import enum
from datetime import datetime

from sqlalchemy import BigInteger, DECIMAL, Enum

from src.database.connector import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, TIMESTAMP, ForeignKey


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    tg_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    is_vip: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class UserProfile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    nu_id: Mapped[int] = mapped_column(
        String(32), nullable=False
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

    soulmate_gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum), nullable=False
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
    registered_at: Mapped[datetime] = mapped_column(  # todo: replace deprecated time method
        TIMESTAMP, default=datetime.utcnow
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
