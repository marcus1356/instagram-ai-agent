from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PostStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    POSTED = "posted"
    FAILED = "failed"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    trending_topic: Mapped[str] = mapped_column(String(255))
    caption: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500))
    image_prompt: Mapped[str] = mapped_column(Text)
    hashtags: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=PostStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
