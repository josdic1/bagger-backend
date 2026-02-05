from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaxonomyCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    type: Optional[str] = None  # only for Platform


class PlatformUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[str] = None


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class PlatformResponse(BaseModel):
    id: int
    name: str
    slug: str
    type: str
    model_config = ConfigDict(from_attributes=True)


class TopicResponse(BaseModel):
    id: int
    name: str
    slug: str
    model_config = ConfigDict(from_attributes=True)
