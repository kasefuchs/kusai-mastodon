from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from kusai import AbstractSerializable


@dataclass
class PostConfig(AbstractSerializable):
    retries: int = field(default=250)
    min_words: int = field(default=2)
    max_words: int = field(default=20)
    visibility: str = field(default="unlisted")

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "retries": self.retries,
            "min_words": self.min_words,
            "max_words": self.max_words,
            "visibility": self.visibility,
        }

    def deserialize(self, data: Dict) -> bool:
        self.retries = data["retries"]
        self.min_words = data["min_words"]
        self.max_words = data["max_words"]
        self.visibility = data["visibility"]
        return True


@dataclass
class TrainConfig(AbstractSerializable):
    source: str = field(default_factory=str)
    exclude_replies: bool = field(default=True)
    exclude_reblogs: bool = field(default=True)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "source": self.source,
            "exclude_replies": self.exclude_replies,
            "exclude_reblogs": self.exclude_reblogs,
        }

    def deserialize(self, data: Dict) -> bool:
        self.source = data["source"]
        self.exclude_replies = data["exclude_replies"]
        self.exclude_reblogs = data["exclude_reblogs"]
        return True


@dataclass
class TextChainConfig(AbstractSerializable):
    max_context_size: int = field(default=2)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "max_context_size": self.max_context_size,
        }

    def deserialize(self, data: Dict) -> bool:
        self.max_context_size = data["max_context_size"]
        return True


@dataclass
class InstanceConfig(AbstractSerializable):
    api_url: str = field(default_factory=str)
    client_id: str = field(default_factory=str)
    client_secret: str = field(default_factory=str)
    scopes: list[str] = field(default_factory=list)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "api_url": self.api_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": self.scopes,
        }

    def deserialize(self, data: Dict) -> bool:
        self.api_url = data["api_url"]
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]
        self.scopes = data["scopes"]
        return True


@dataclass
class UserConfig(AbstractSerializable):
    post: PostConfig = field(default_factory=PostConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    instance: InstanceConfig = field(default_factory=InstanceConfig)
    textchain: TextChainConfig = field(default_factory=TextChainConfig)

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "post": self.post.serialize(),
            "train": self.train.serialize(),
            "instance": self.instance.serialize(),
            "textchain": self.textchain.serialize(),
        }

    def deserialize(self, data: Dict) -> bool:
        success = True
        success &= self.post.deserialize(data["post"])
        success &= self.train.deserialize(data["train"])
        success &= self.instance.deserialize(data["instance"])
        success &= self.textchain.deserialize(data["textchain"])
        return success


@dataclass
class Config(AbstractSerializable):
    users: Dict[str, UserConfig] = field(default_factory=dict)
    state_path: Path = field(default=Path("state.json"))

    def __post_init__(self):
        super().__init__()

    def serialize(self) -> Dict:
        return {
            "users": {k: v.serialize() for k, v in self.users.items()},
            "state_path": self.state_path.as_posix(),
        }

    def deserialize(self, data: Dict) -> bool:
        success = True

        self.users.clear()
        for k, v in data["users"].items():
            user = UserConfig()
            success &= user.deserialize(v)
            self.users[k] = user

        self.state_path = Path(data["state_path"])

        return success
