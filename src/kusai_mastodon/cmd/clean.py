from typing import cast

import typer

from kusai_mastodon.model import Context
from kusai_mastodon.model.state import ProgressState, UserState

app = typer.Typer()


@app.command()
def clean(ctx: typer.Context, force: bool = False, reset_progress: bool = True):
    context = cast(Context, ctx.obj)

    for name, user_config in context.config.users.items():
        if not force:
            confirm = typer.confirm(
                typer.style(
                    f"Clear training data for user: {name}?", fg=typer.colors.YELLOW
                )
            )
            if not confirm:
                typer.echo(f"Skipping user: {name}")
                continue

        typer.secho(f"Cleaning state for user: {name}", fg=typer.colors.YELLOW)
        user_state = context.state.users[name]

        user_state.chain = UserState.create_chain(user_config)
        if reset_progress:
            user_state.progress = ProgressState()

    context.save()
