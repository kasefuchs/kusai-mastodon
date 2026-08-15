from typing import cast

import structlog
import typer

from kusai_mastodon.model import Context
from kusai_mastodon.model.state import ProgressState, UserState

app = typer.Typer()
logger = structlog.get_logger()


@app.command()
def clean(ctx: typer.Context, force: bool = False, reset_progress: bool = True):
    context = cast(Context, ctx.obj)

    for name, user_config in context.config.users.items():
        log = logger.bind(user=name)

        if not force:
            confirm = typer.confirm(f"Clear training data for user: {name}?")
            if not confirm:
                continue

        user_state = context.state.users[name]
        user_state.chain = UserState.create_chain(user_config)
        if reset_progress:
            user_state.progress = ProgressState()

        log.info("Cleaned user state", reset_progress=reset_progress)

    context.save()
