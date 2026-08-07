from functools import cached_property
from pathlib import Path
from adblock.adblock import FilterSet
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from mastodon import Mastodon
from mastodon.return_types import Status
from kusai import TextChain

from .enum import Marker


class GenerateConfig(BaseModel):
    limit: int = 25
    retries: int = 100
    min_words: int = 2
    max_words: int = 20

    def __call__(self, chain: TextChain) -> str | None:
        for _ in range(self.retries):
            candidate = Marker.unwrap(chain.generate_text(Marker.STX, limit=self.limit))
            if self.min_words <= len(candidate.split()) <= self.max_words:
                return candidate

        return None


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


class ExcludeConfig(BaseModel):
    replies: bool = True
    reblogs: bool = True
    sensitive: bool = True

    def __call__(self, status: Status) -> bool:
        return bool(
            (self.reblogs and status.reblog)
            or (self.replies and status.in_reply_to_id)
            or (self.sensitive and status.sensitive)
        )


class TrainConfig(BaseModel):
    source: str = ""
    chain: TextChainConfig = Field(default_factory=TextChainConfig)
    adblock: AdblockConfig = Field(default_factory=AdblockConfig)
    exclude: ExcludeConfig = Field(default_factory=ExcludeConfig)


class InstanceConfig(BaseModel):
    api_url: str = ""
    access_token: str = ""

    @cached_property
    def client(self):
        return Mastodon(
            api_base_url=self.api_url,
            access_token=self.access_token,
        )


class UserConfig(BaseModel):
    post: StatusConfig = Field(default_factory=StatusConfig)
    reply: StatusConfig = Field(default_factory=StatusConfig)
    train: TrainConfig = Field(default_factory=TrainConfig)
    instance: InstanceConfig = Field(default_factory=InstanceConfig)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="KUSAI_MASTODON_",
        env_nested_delimiter="__",
    )

    users: dict[str, UserConfig] = Field(default_factory=dict)
    state_path: Path = Path("state.json")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings, file_secret_settings
