from typing import cast

import typer

from kusai_mastodon.model import Context

app = typer.Typer()


@app.command()
def post(ctx: typer.Context, dry_run: bool = False):
    context = cast(Context, ctx.obj)

    for name, user_config in context.config.users.items():
        typer.secho(f"Posting for user: {name}", fg=typer.colors.CYAN, bold=True)

        user_state = context.state.users[name]
        client = user_config.instance.client

        try:
            content = user_config.post.generate(user_state.chain)
            typer.secho(f"Generated content: {content}", fg=typer.colors.BLUE)
            if not dry_run:
                status = client.status_post(
                    content, visibility=user_config.post.visibility
                )

                typer.secho(f"Successfully posted: {status.url}", fg=typer.colors.GREEN)

        except Exception as e:
            typer.secho(
                f"Failed to generate content: {e}",
                fg=typer.colors.RED,
                err=True,
            )
