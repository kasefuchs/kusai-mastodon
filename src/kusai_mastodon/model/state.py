from typing import Dict, Optional, Any
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


class InstanceState(BaseModel):
    access_token: str = ""


class UserState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    chain: TextChain
    instance: InstanceState = Field(default_factory=InstanceState)
    progress: ProgressState = Field(default_factory=ProgressState)

    @field_serializer("chain")
    def serialize_chain(self, chain: TextChain) -> Dict[str, Any]:
        return chain.serialize()

    @field_validator("chain", mode="before")
    @classmethod
    def deserialize_chain(cls, value: Any, info: ValidationInfo) -> TextChain:
        assert info.context is not None
        user_config = info.context.get("user_config")

        chain = cls.create_chain(user_config)
        chain.deserialize(value)

        return chain

    @staticmethod
    def create_chain(config: UserConfig) -> TextChain:
        graph = MemoryGraph()
        markov = BackoffMarkov(graph, max_context_size=config.train.chain.max_context_size)
        tokenizer = SimpleTokenizer()

        return TextChain(markov, tokenizer)


class State(BaseModel):
    users: Dict[str, UserState] = Field(default_factory=dict)

    @field_validator("users", mode="before")
    @classmethod
    def deserialize_users(cls, value: Any, info: ValidationInfo) -> Any:
        assert info.context is not None
        config = info.context.get("config")

        users = {}
        for name, user_config in config.users.items():
            state = value.get(name, {})
            users[name] = UserState.model_validate(state, context={"user_config": user_config})

        return users
