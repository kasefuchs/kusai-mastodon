from bs4 import BeautifulSoup
from mastodon.return_types import Status
from adblock import Engine

from kusai_mastodon.model.enum import Marker
from kusai_mastodon.model.config import ExcludeConfig


def encode_statuses(statuses: list[Status], adblock: Engine) -> list[str]:
    contents = [sanitize_status_content(i.content, adblock) for i in statuses]
    return [Marker.wrap(i) for i in filter(None, contents)]


def filter_statuses(statuses: list[Status], exclude: ExcludeConfig) -> list[Status]:
    return [s for s in statuses if not exclude(s)]


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
