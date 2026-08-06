from typing import Optional

from bs4 import BeautifulSoup
from kusai import TextChain
from mastodon.return_types import Status
from adblock import Engine

from kusai_mastodon.model.enum import Marker
from kusai_mastodon.model.config import GenerateConfig


def wrap_chain_text(text: str) -> str:
    return f"{Marker.STX.value} {text.strip()} {Marker.ETX.value}"


def unwrap_chain_text(text: str) -> str:
    return text.lstrip(Marker.STX.value).rstrip(Marker.ETX.value).strip()


def sanitize_status_content(content: str, adblock: Engine) -> str:
    soup = BeautifulSoup(content, "html.parser")

    ids = {str(tag.id) for tag in soup.find_all(id=True) if tag.get("id")}
    classes = {c for tag in soup.find_all(class_=True) for c in tag.get_attribute_list("class") if c}

    selectors = adblock.hidden_class_id_selectors(list(classes), list(ids), set())
    for selector in selectors:
        for element in soup.select(selector):
            element.decompose()

    for a in soup.find_all("a"):
        classes = a.get("class") or []

        if "mention" in classes or "hashtag" in classes:
            a.replace_with(a.get_text(separator="\u200b", strip=True))
        else:
            href = a.get("href", "")
            if isinstance(href, str):
                a.replace_with(href)

    return soup.get_text(separator=" ", strip=True)


def encode_statuses(statuses: list[Status], adblock: Engine) -> list[str]:
    contents = [sanitize_status_content(i.content, adblock) for i in statuses]
    return [wrap_chain_text(i) for i in filter(None, contents)]


def generate_status_content(textchain: TextChain, config: GenerateConfig) -> Optional[str]:
    for _ in range(config.retries):
        candidate = unwrap_chain_text(textchain.generate_text(Marker.STX.value, limit=config.limit))
        if config.min_words <= len(candidate.split()) <= config.max_words:
            return candidate

    return None
