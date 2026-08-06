from mastodon import Mastodon

from kusai_mastodon.model.config import InstanceConfig
from kusai_mastodon.model.state import InstanceState


def create_mastodon_client(config: InstanceConfig, state: InstanceState) -> Mastodon:
    client_id = config.client_id or state.client_id
    client_secret = config.client_secret or state.client_secret

    if not (client_id and client_secret):
        client_id, client_secret = Mastodon.create_app(
            client_name="kusai-mastodon",
            scopes=config.scopes,
            api_base_url=config.api_url,
        )

        state.client_id = client_id
        state.client_secret = client_secret

    return Mastodon(
        api_base_url=config.api_url,
        client_id=client_id,
        client_secret=client_secret,
        access_token=state.access_token,
    )
