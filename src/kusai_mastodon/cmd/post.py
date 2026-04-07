import typer

from kusai_mastodon.util import (
    create_mastodon_client,
    generate_status_content,
)

app = typer.Typer()


@app.command()
def post(ctx: typer.Context, dry_run: bool = False):
    for name, user_config in ctx.obj.config.users.items():
        typer.secho(f"Posting for user: {name}", fg=typer.colors.CYAN, bold=True)

        user_state = ctx.obj.state.users[name]
        client = create_mastodon_client(user_config.instance, user_state.instance)

        content = generate_status_content(user_state.chain, user_config.post.generate)
        if content:
            typer.secho(f"Generated content: {content}", fg=typer.colors.BLUE)
            if not dry_run:
                status = client.status_post(
                    content, visibility=user_config.post.visibility
                )

                typer.secho(f"Successfully posted: {status.url}", fg=typer.colors.GREEN)
        else:
            typer.secho(
                f"Failed to generate post content",
                fg=typer.colors.RED,
            )
