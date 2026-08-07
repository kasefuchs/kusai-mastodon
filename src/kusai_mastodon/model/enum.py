from enum import StrEnum


class Marker(StrEnum):
    STX = "\ue002"
    ETX = "\ue003"

    @classmethod
    def wrap(cls, text: str) -> str:
        return f"{cls.STX} {text.strip()} {cls.ETX}"

    @classmethod
    def unwrap(cls, text: str) -> str:
        return text.lstrip(cls.STX).rstrip(cls.ETX).strip()
