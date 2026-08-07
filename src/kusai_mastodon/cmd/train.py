import typer
from kusai_mastodon.util import encode_statuses, filter_statuses
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, MofNCompleteColumn, TimeRemainingColumn

from kusai_mastodon.util import encode_statuses

app = typer.Typer()


@app.command()
def train(ctx: typer.Context):
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
    ) as progress:
        try:
            for name, user_config in ctx.obj.config.users.items():
                user_state = ctx.obj.state.users[name]
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
                        if train_statuses := filter_statuses(statuses, user_config.train.exclude):
                            user_state.chain.train(encode_statuses(train_statuses, user_state.adblock))

                        batch_size = len(statuses)
                        user_state.progress.count += batch_size
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

                progress.update(task, completed=True)

        finally:
            ctx.obj.save()
