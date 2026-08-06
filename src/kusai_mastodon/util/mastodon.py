from mastodon import Mastodon
from importlib.metadata import metadata, PackageNotFoundError

from kusai_mastodon.model.config import InstanceConfig
from kusai_mastodon.model.state import InstanceState


def get_app_metadata(app_name: str) -> tuple[str, str | None]:
    try:
        meta = metadata(app_name)
        return meta.get("Name") or app_name, meta.get("Project-URL", "").split(", ")[-1] or None
    except PackageNotFoundError:
        return app_name, None


def create_mastodon_client(config: InstanceConfig, state: InstanceState) -> Mastodon:
    client_id = config.client_id or state.client_id
    client_secret = config.client_secret or state.client_secret
    access_token = config.access_token or state.access_token

    if not access_token and not (client_id and client_secret):
        client_name, website = get_app_metadata(config.app_name)
        client_id, client_secret = Mastodon.create_app(
            client_name=client_name,
            website=website,
            scopes=config.scopes,
            api_base_url=config.api_url,
        )

        state.client_id = client_id
        state.client_secret = client_secret

    return Mastodon(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=config.api_url,
    )
