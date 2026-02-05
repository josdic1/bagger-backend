from pydantic import BaseModel
from typing import List
from .auth import UserResponse
from .taxonomy import PlatformResponse, TopicResponse
from .cheat import CheatResponse, UserCheatResponse


class CheatPlatformLink(BaseModel):
    cheat_id: int
    platform_id: int


class CheatTopicLink(BaseModel):
    cheat_id: int
    topic_id: int


class BootstrapResponse(BaseModel):
    user: UserResponse
    platforms: List[PlatformResponse]
    topics: List[TopicResponse]
    cheats: List[CheatResponse]
    cheat_platforms: List[CheatPlatformLink]
    cheat_topics: List[CheatTopicLink]
    user_cheats: List[UserCheatResponse]
