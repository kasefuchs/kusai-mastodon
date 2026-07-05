import typer
from mastodon import MastodonUnauthorizedError

from kusai_mastodon.util import create_mastodon_client

app = typer.Typer()


@app.command()
def login(ctx: typer.Context, force: bool = False):
    for name, user_config in ctx.obj.config.users.items():
        user_state = ctx.obj.state.users[name]
        client = create_mastodon_client(user_config.instance, user_state.instance)

        typer.secho(f"Authorising user: {name}", fg=typer.colors.CYAN, bold=True)

        try:
            client.preferences()

            if not force:
                typer.secho("Already authorized", fg=typer.colors.GREEN)
                continue
        except MastodonUnauthorizedError:
            pass

        auth_url = client.auth_request_url(scopes=user_config.instance.scopes)
        typer.secho("Opening browser for authorization...", fg=typer.colors.BLUE)
        typer.echo(f"If it didn’t open, visit: {auth_url}")
        typer.launch(auth_url)

        access_code = typer.prompt(typer.style("Enter access code", fg=typer.colors.YELLOW))
        user_state.instance.access_token = client.log_in(code=access_code, scopes=user_config.instance.scopes)

    ctx.obj.save()
