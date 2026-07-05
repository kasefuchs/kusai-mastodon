import json
from dataclasses import dataclass
from typing import Self
from pathlib import Path

import yaml

from .config import Config
from .state import State


@dataclass
class Context:
    config: Config
    state: State

    @classmethod
    def load(cls, config_path: Path) -> Self:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

        config = Config.model_validate(config_data)

        state_data = {}
        try:
            with open(config.state_path, "r", encoding="utf-8") as f:
                state_data = json.load(f)
        except FileNotFoundError:
            pass

        state = State.model_validate(state_data, context={"config": config})

        return cls(config, state)

    def save(self):
        with open(self.config.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state.model_dump(), f)
