from functools import cached_property
from pathlib import Path
from adblock.adblock import FilterSet
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


class AdblockConfig(BaseModel):
    format: str = "standard"
    filters: list[str] = Field(default_factory=list)

    @cached_property
    def filter_set(self):
        fs = FilterSet()
        fs.add_filters(self.filters, self.format)
        return fs


class TrainConfig(BaseModel):
    source: str = ""
    exclude_replies: bool = True
    exclude_reblogs: bool = True
    chain: TextChainConfig = Field(default_factory=TextChainConfig)
    adblock: AdblockConfig = Field(default_factory=AdblockConfig)


class InstanceConfig(BaseModel):
    api_url: str = ""
    app_name: str = "kusai-mastodon"
    client_id: str = ""
    client_secret: str = ""
    access_token: str = ""
    scopes: list[str] = Field(default_factory=list)


class UserConfig(BaseModel):
    post: StatusConfig = Field(default_factory=StatusConfig)
    reply: StatusConfig = Field(default_factory=StatusConfig)
    train: TrainConfig = Field(default_factory=TrainConfig)
    instance: InstanceConfig = Field(default_factory=InstanceConfig)


class Config(BaseModel):
    users: dict[str, UserConfig] = Field(default_factory=dict)
    state_path: Path = Path("state.json")
