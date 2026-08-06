import typer

from kusai_mastodon.util import generate_status_content

app = typer.Typer()


@app.command()
def reply(ctx: typer.Context, dry_run: bool = False):
    try:
        for name, user_config in ctx.obj.config.users.items():
            typer.secho(f"Replying as user: {name}", fg=typer.colors.CYAN, bold=True)

            user_state = ctx.obj.state.users[name]
            client = user_config.instance.client

            notifications = client.notifications(
                types=["mention"],
                limit=100,
                since_id=user_state.progress.last_reply_id,
            )

            for notification in reversed(notifications):
                if not notification.status:
                    continue

                typer.secho(
                    f"Replying to {notification.account.username} (Status: {notification.status.id})",
                    fg=typer.colors.MAGENTA,
                )

                if notification.account.bot:
                    typer.secho("Skipping bot", fg=typer.colors.YELLOW)
                else:
                    content = generate_status_content(user_state.chain, user_config.reply.generate)
                    if content:
                        text = f"@{notification.account.acct} {content}"
                        typer.secho(f"Generated reply: {text}", fg=typer.colors.BLUE)

                        if not dry_run:
                            reply_status = client.status_post(
                                status=text,
                                in_reply_to_id=notification.status.id,
                                visibility=user_config.reply.visibility,
                            )

                            typer.secho(f"Successfully replied: {reply_status.url}", fg=typer.colors.GREEN)
                    else:
                        typer.secho(f"Failed to generate reply content", fg=typer.colors.RED)

                if not dry_run:
                    user_state.progress.last_reply_id = notification.id
    finally:
        ctx.obj.save()
