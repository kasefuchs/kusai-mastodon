from typing import Optional, Any
from adblock import Engine
from pydantic import BaseModel, Field, ConfigDict, field_serializer, field_validator, ValidationInfo
from mastodon.types_base import IdType

from kusai import (
    SimpleTokenizer,
    BackoffMarkov,
    MemoryGraph,
    TextChain,
)

from .config import UserConfig


class ProgressState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    max_id: Optional[IdType] = None
    since_id: Optional[IdType] = None
    last_reply_id: Optional[IdType] = None


class UserState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    chain: TextChain = Field(default=None, validate_default=True)
    adblock: Engine = Field(default=None, exclude=True, validate_default=True)
    progress: ProgressState = Field(default_factory=ProgressState)

    @field_serializer("chain")
    def serialize_chain(self, chain: TextChain) -> dict[str, Any]:
        return chain.serialize()

    @field_validator("chain", mode="before")
    @classmethod
    def deserialize_chain(cls, value: Any, info: ValidationInfo) -> TextChain:
        assert info.context is not None
        user_config = info.context.get("user_config")

        chain = cls.create_chain(user_config)
        if value is not None:
            chain.deserialize(value)

        return chain

    @field_validator("adblock", mode="before")
    @classmethod
    def deserialize_adblock(cls, _: Any, info: ValidationInfo) -> Engine:
        assert info.context is not None
        user_config = info.context.get("user_config")

        return cls.create_adblock(user_config)

    @staticmethod
    def create_chain(config: UserConfig) -> TextChain:
        graph = MemoryGraph()
        markov = BackoffMarkov(graph, max_context_size=config.train.chain.max_context_size)
        tokenizer = SimpleTokenizer()

        return TextChain(markov, tokenizer)

    @staticmethod
    def create_adblock(config: UserConfig) -> Engine:
        return Engine(config.train.adblock.filter_set)


class State(BaseModel):
    users: dict[str, UserState] = Field(default_factory=dict, validate_default=True)

    @field_validator("users", mode="before")
    @classmethod
    def deserialize_users(cls, value: Any, info: ValidationInfo) -> dict[str, UserState]:
        assert info.context is not None
        config = info.context.get("config")

        users = {}
        for name, user_config in config.users.items():
            state = value.get(name, {})
            users[name] = UserState.model_validate(state, context={"user_config": user_config})

        return users
