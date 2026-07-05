import typer

from kusai_mastodon.model.state import UserState

app = typer.Typer()


@app.command()
def clean(ctx: typer.Context, force: bool = False, reset_progress: bool = True):
    for name, user_config in ctx.obj.config.users.items():
        if not force:
            confirm = typer.confirm(typer.style(f"Clear training data for user: {name}?", fg=typer.colors.YELLOW))
            if not confirm:
                typer.echo(f"Skipping user: {name}")
                continue

        typer.secho(f"Cleaning state for user: {name}", fg=typer.colors.YELLOW)
        user_state = ctx.obj.state.users[name]

        user_state.chain = UserState.create_chain(user_config)
        if reset_progress:
            user_state.progress.since_id = None
            user_state.progress.max_id = None
            user_state.progress.last_reply_id = None

    ctx.obj.save()
