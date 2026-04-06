from bs4 import BeautifulSoup

from kusai_mastodon.model import Marker


def wrap_chain_text(text: str) -> str:
    return f"{Marker.STX.value} {text.strip()} {Marker.ETX.value}"


def unwrap_chain_text(text: str) -> str:
    return text.lstrip(Marker.STX.value).rstrip(Marker.ETX.value).strip()


# noinspection PyUnresolvedReferences,PyTypeChecker,PyArgumentList
def sanitize_status_content(content: str) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup.find_all(class_="gts-system-message"):
        tag.decompose()

    for a in soup.find_all("a"):
        classes = a.get("class", [])
        if "mention" in classes or "hashtag" in classes:
            a.replace_with(a.get_text(separator="\u200b", strip=True))
        else:
            a.replace_with(a.get("href", ""))

    return soup.get_text(separator=" ", strip=True)
