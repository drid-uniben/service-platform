import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.enums import AttemptStatus


class ProviderAttempt(Base):
    __tablename__ = "provider_attempts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    storage_object_id: Mapped[str] = mapped_column(
        ForeignKey("storage_objects.id", ondelete="CASCADE"), index=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[AttemptStatus] = mapped_column(Enum(AttemptStatus), nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    storage_object = relationship("StorageObject", back_populates="attempts")
