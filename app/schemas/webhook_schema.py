from datetime import datetime
from pydantic import BaseModel, HttpUrl


class WebhookCreate(BaseModel):
    name: str
    url: HttpUrl


class WebhookUpdate(BaseModel):
    name: str | None = None
    url: HttpUrl | None = None
    enabled: bool | None = None


class WebhookResponse(BaseModel):
    id: int
    name: str
    url: HttpUrl
    enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True