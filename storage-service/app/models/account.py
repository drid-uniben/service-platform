import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    api_keys = relationship("ApiKey", back_populates="account", cascade="all, delete-orphan")
    storage_objects = relationship("StorageObject", back_populates="account", cascade="all, delete-orphan")
    webhook_endpoints = relationship("WebhookEndpoint", back_populates="account", cascade="all, delete-orphan")
