from typing import List

import typer
from mastodon.return_types import Status
from rich.progress import Progress

from kusai_mastodon.util import (
    create_mastodon_client,
    wrap_chain_text,
    sanitize_status_content,
)

app = typer.Typer()


def _encode_statuses(statuses: List[Status]) -> List[str]:
    contents = [sanitize_status_content(i.content) for i in statuses]
    return [wrap_chain_text(i) for i in filter(None, contents)]


@app.command()
def train(ctx: typer.Context):
    with Progress() as progress:
        try:
            for name, user_config in ctx.obj.config.users.items():
                user_state = ctx.obj.state.users[name]
                client = create_mastodon_client(user_config.instance, user_state.instance)
                account = client.account_lookup(user_config.train.source)
                task = progress.add_task(f"Training {name}", total=account.statuses_count)

                if not (user_state.progress.since_id and user_state.progress.max_id):
                    statuses = client.account_statuses(
                        account,
                        exclude_reblogs=user_config.train.exclude_reblogs,
                        exclude_replies=user_config.train.exclude_replies,
                    )
                    if statuses:
                        user_state.progress.since_id = statuses[0].id
                        user_state.progress.max_id = statuses[-1].id
                        user_state.chain.train(_encode_statuses(statuses))

                        progress.update(task, advance=len(statuses))

                if user_state.progress.since_id is not None:
                    while True:
                        statuses = client.account_statuses(
                            account,
                            min_id=user_state.progress.since_id,
                            exclude_reblogs=user_config.train.exclude_reblogs,
                            exclude_replies=user_config.train.exclude_replies,
                        )
                        if not statuses:
                            break

                        user_state.progress.since_id = statuses[0].id
                        user_state.chain.train(_encode_statuses(statuses))

                        progress.update(task, advance=len(statuses))

                if user_state.progress.max_id is not None:
                    while True:
                        statuses = client.account_statuses(
                            account,
                            max_id=user_state.progress.max_id,
                            exclude_reblogs=user_config.train.exclude_reblogs,
                            exclude_replies=user_config.train.exclude_replies,
                        )
                        if not statuses:
                            break

                        user_state.progress.max_id = statuses[-1].id
                        user_state.chain.train(_encode_statuses(statuses))

                        progress.update(task, advance=len(statuses))

                progress.update(task, completed=True)

        finally:
            ctx.obj.save()
