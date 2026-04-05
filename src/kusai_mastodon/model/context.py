import json
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import Config
from .state import State


@dataclass
class Context:
    config: Config
    state: State

    @classmethod
    def load(cls, config_path: Path) -> Context:
        config = Config()
        with open(config_path, "rb") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            config.deserialize(data)

        state = State.build(config)
        try:
            with open(config.state_path, "r") as f:
                data = json.load(f)
                state.deserialize(data)
        except FileNotFoundError:
            pass

        return cls(config, state)

    def save(self):
        with open(self.config.state_path, "w") as f:
            json.dump(self.state.serialize(), f)
