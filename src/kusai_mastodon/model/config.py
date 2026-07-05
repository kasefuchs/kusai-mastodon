from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel, Field


class GenerateConfig(BaseModel):
    limit: int = 25
    retries: int = 100
    min_words: int = 2
    max_words: int = 20


class StatusConfig(BaseModel):
    generate: GenerateConfig = Field(default_factory=GenerateConfig)
    visibility: str = "unlisted"


class TextChainConfig(BaseModel):
    max_context_size: int = 2


class TrainConfig(BaseModel):
    source: str = ""
    exclude_replies: bool = True
    exclude_reblogs: bool = True
    chain: TextChainConfig = Field(default_factory=TextChainConfig)


class InstanceConfig(BaseModel):
    api_url: str = ""
    client_id: str = ""
    client_secret: str = ""
    scopes: List[str] = Field(default_factory=list)


class UserConfig(BaseModel):
    post: StatusConfig = Field(default_factory=StatusConfig)
    reply: StatusConfig = Field(default_factory=StatusConfig)
    train: TrainConfig = Field(default_factory=TrainConfig)
    instance: InstanceConfig = Field(default_factory=InstanceConfig)


class Config(BaseModel):
    users: Dict[str, UserConfig] = Field(default_factory=dict)
    state_path: Path = Field(default=Path("state.json"))
