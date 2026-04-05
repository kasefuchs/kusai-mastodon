from mastodon import Mastodon

from kusai_mastodon.model.config import InstanceConfig
from kusai_mastodon.model.state import InstanceState


def create_mastodon_client(config: InstanceConfig, state: InstanceState) -> Mastodon:
    return Mastodon(
        api_base_url=config.api_url,
        client_id=config.client_id,
        client_secret=config.client_secret,
        access_token=state.access_token,
    )
