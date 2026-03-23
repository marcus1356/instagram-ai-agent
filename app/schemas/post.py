from datetime import datetime

from pydantic import BaseModel

from app.models.post import PostStatus


class PostBase(BaseModel):
    trending_topic: str
    caption: str
    image_url: str
    image_prompt: str
    hashtags: str
    status: PostStatus


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    posted_at: datetime | None = None

    model_config = {"from_attributes": True}


class GenerateRequest(BaseModel):
    topic_override: str | None = None  # força um tópico específico (opcional)