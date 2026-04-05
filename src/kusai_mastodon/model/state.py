from dataclasses import dataclass, field
from typing import Dict, Optional

from kusai import (
    AbstractSerializable,
    SimpleTokenizer,
    BackoffMarkov,
    MemoryGraph,
    TextChain,
)
from mastodon.types_base import IdType

from .config import Config, UserConfig


@dataclass
class ProgressState(AbstractSerializable):
    max_id: Optional[IdType] = field(default=None)
    since_id: Optional[IdType] = field(default=None)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {"max_id": self.max_id, "since_id": self.since_id}

    def deserialize(self, data: Dict) -> bool:
        self.max_id = data["max_id"]
        self.since_id = data["since_id"]
        return True


@dataclass
class InstanceState(AbstractSerializable):
    access_token: str = field(default_factory=str)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {"access_token": self.access_token}

    def deserialize(self, data: Dict) -> bool:
        self.access_token = data["access_token"]
        return True


@dataclass
class UserState(AbstractSerializable):
    textchain: TextChain

    instance: InstanceState = field(default_factory=InstanceState)
    progress: ProgressState = field(default_factory=ProgressState)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "instance": self.instance.serialize(),
            "progress": self.progress.serialize(),
            "textchain": self.textchain.serialize(),
        }

    def deserialize(self, data: Dict) -> bool:
        success = True
        success &= self.instance.deserialize(data["instance"])
        success &= self.progress.deserialize(data["progress"])
        success &= self.textchain.deserialize(data["textchain"])
        return success

    @staticmethod
    def build(config: UserConfig) -> UserState:
        graph = MemoryGraph()
        markov = BackoffMarkov(
            graph, max_context_size=config.textchain.max_context_size
        )
        tokenizer = SimpleTokenizer()
        chain = TextChain(markov, tokenizer)

        return UserState(chain)


@dataclass
class State(AbstractSerializable):
    users: Dict[str, UserState] = field(default_factory=dict)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "users": {k: v.serialize() for k, v in self.users.items()},
        }

    def deserialize(self, data: Dict) -> bool:
        success = True
        for k, v in data["users"].items():
            success &= self.users[k].deserialize(v)

        return success

    @staticmethod
    def build(config: Config) -> State:
        return State(
            users={k: UserState.build(v) for k, v in config.users.items()},
        )
