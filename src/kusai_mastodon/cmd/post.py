import typer

from kusai_mastodon.util import create_mastodon_client, unwrap_chain_text
from kusai_mastodon.model import Marker

app = typer.Typer()


@app.command()
def post(ctx: typer.Context, dry_run: bool = False):
    for name, user_config in ctx.obj.config.users.items():
        user_state = ctx.obj.state.users[name]
        client = create_mastodon_client(user_config.instance, user_state.instance)

        typer.secho(f"Posting for user: {name}", fg=typer.colors.CYAN, bold=True)

        content = None
        for _ in range(user_config.post.retries):
            candidate = unwrap_chain_text(
                user_state.textchain.generate_text(Marker.STX.value)
            )

            words = len(candidate.split())
            if user_config.post.min_words <= words <= user_config.post.max_words:
                content = candidate
                break

        if content:
            typer.secho(f"Generated content: {content}", fg=typer.colors.BLUE)
            if not dry_run:
                status = client.status_post(
                    content, visibility=user_config.post.visibility
                )

                typer.secho(f"Successfully posted: {status.url}", fg=typer.colors.GREEN)
        else:
            typer.secho(
                f"Failed to generate content after {user_config.post.retries} retries",
                fg=typer.colors.RED,
            )
