# src/models/user.py

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connector import Base



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

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False
    )
