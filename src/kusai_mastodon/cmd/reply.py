from contextlib import suppress
from typing import cast

import structlog
import typer

from kusai_mastodon.model import Context

app = typer.Typer()
logger = structlog.get_logger()


@app.command()
def reply(ctx: typer.Context, dry_run: bool = False):
    context = cast(Context, ctx.obj)

    try:
        for name, user_config in context.config.users.items():
            log = logger.bind(user=name, dry_run=dry_run)
            user_state = context.state.users[name]
            client = user_config.instance.client

            notifications = client.notifications(
                types=["mention"],
                limit=100,
                since_id=user_state.progress.last_reply_id,
            )

            for notification in reversed(notifications):
                if not notification.status or notification.account.bot:
                    continue

                reply_log = log.bind(
                    target_account=notification.account.acct,
                    target_status_id=notification.status.id,
                    notification_id=notification.id,
                )

                try:
                    content = user_config.reply.generate(user_state.chain)
                    reply_log.debug("Generated content", content=content)

                    if not dry_run:
                        reply_status = client.status_post(
                            status=f"@{notification.account.acct} {content}",
                            in_reply_to_id=notification.status.id,
                            visibility=user_config.reply.visibility,
                        )

                        reply_log.info(
                            "Successfully replied",
                            url=reply_status.url,
                            id=reply_status.id,
                        )

                except Exception as e:
                    reply_log.error("Failed to reply", error=e, exc_info=True)

                if not dry_run:
                    user_state.progress.last_reply_id = notification.id
                    with suppress(Exception):
                        client.notifications_dismiss(notification.id)
    finally:
        context.save()
