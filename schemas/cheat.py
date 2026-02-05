from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class CheatCreate(BaseModel):
    title: str
    code: str
    notes: Optional[str] = None
    platform_ids: List[int] = []
    topic_ids: List[int] = []
    is_public: bool = True


class CheatUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    notes: Optional[str] = None
    platform_ids: Optional[List[int]] = None
    topic_ids: Optional[List[int]] = None
    is_public: Optional[bool] = None


class CheatResponse(BaseModel):
    id: int
    title: str
    code: str
    notes: Optional[str] = None
    is_public: bool
    platform_ids: List[int]
    topic_ids: List[int]
    model_config = ConfigDict(from_attributes=True)


class UserCheatResponse(BaseModel):
    user_id: int
    cheat_id: int
    is_favorite: bool
    personal_notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserCheatUpdate(BaseModel):
    is_favorite: Optional[bool] = None
    personal_notes: Optional[str] = None
