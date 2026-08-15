from typing import cast

import structlog
import typer
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from kusai_mastodon.model import Context
from kusai_mastodon.util import encode_statuses, filter_statuses

app = typer.Typer()
logger = structlog.get_logger()


@app.command()
def train(ctx: typer.Context):
    context = cast(Context, ctx.obj)

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
    ) as progress:
        try:
            for name, user_config in context.config.users.items():
                log = logger.bind(user=name)
                user_state = context.state.users[name]
                client = user_config.instance.client
                account = client.account_lookup(user_config.train.source)

                task = progress.add_task(
                    f"Training {name}",
                    total=account.statuses_count,
                    completed=user_state.progress.count,
                )

                def step(**kwargs):
                    statuses = client.account_statuses(
                        account,
                        exclude_reblogs=user_config.train.exclude.reblogs,
                        exclude_replies=user_config.train.exclude.replies,
                        **kwargs,
                    )
                    if statuses:
                        if train_statuses := filter_statuses(
                            statuses, user_config.train.exclude
                        ):
                            user_state.chain.train(
                                encode_statuses(train_statuses, user_state.adblock)
                            )

                        batch_size = len(statuses)
                        user_state.progress.count += batch_size

                        log.debug(
                            "Fetched status batch",
                            batch_size=batch_size,
                            trained_size=len(train_statuses),
                        )
                        progress.update(task, advance=batch_size)

                    return statuses

                if not (user_state.progress.since_id and user_state.progress.max_id):
                    statuses = step()
                    if statuses:
                        user_state.progress.since_id = statuses[0].id
                        user_state.progress.max_id = statuses[-1].id

                if user_state.progress.since_id is not None:
                    while statuses := step(min_id=user_state.progress.since_id):
                        user_state.progress.since_id = statuses[0].id

                if user_state.progress.max_id is not None:
                    while statuses := step(max_id=user_state.progress.max_id):
                        user_state.progress.max_id = statuses[-1].id

                log.info(
                    "Completed training",
                    total_statuses=account.statuses_count,
                    trained_count=user_state.progress.count,
                )
                progress.update(task, completed=True)

        finally:
            context.save()
