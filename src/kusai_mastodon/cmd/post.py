import typer

app = typer.Typer()


@app.command()
def post(ctx: typer.Context, dry_run: bool = False):
    for name, user_config in ctx.obj.config.users.items():
        typer.secho(f"Posting for user: {name}", fg=typer.colors.CYAN, bold=True)

        user_state = ctx.obj.state.users[name]
        client = user_config.instance.client

        content = user_config.post.generate(user_state.chain)
        if content:
            typer.secho(f"Generated content: {content}", fg=typer.colors.BLUE)
            if not dry_run:
                status = client.status_post(content, visibility=user_config.post.visibility)

                typer.secho(f"Successfully posted: {status.url}", fg=typer.colors.GREEN)
        else:
            typer.secho(f"Failed to generate post content", fg=typer.colors.RED)
