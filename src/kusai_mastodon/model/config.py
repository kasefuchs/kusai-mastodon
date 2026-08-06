from functools import cached_property
from pathlib import Path
from adblock.adblock import FilterSet
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from mastodon import Mastodon


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
