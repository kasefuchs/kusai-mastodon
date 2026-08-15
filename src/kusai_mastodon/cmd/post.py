from typing import cast

import structlog
import typer

from kusai_mastodon.model import Context

app = typer.Typer()
logger = structlog.get_logger()


@app.command()
def post(ctx: typer.Context, dry_run: bool = False):
    context = cast(Context, ctx.obj)

    for name, user_config in context.config.users.items():
        log = logger.bind(user=name, dry_run=dry_run)
        user_state = context.state.users[name]
        client = user_config.instance.client

        try:
            content = user_config.post.generate(user_state.chain)
            log.debug("Generated content", content=content)

            if not dry_run:
                status = client.status_post(
                    content, visibility=user_config.post.visibility
                )
                log.info("Successfully posted status", url=status.url, id=status.id)

        except Exception as e:
            log.error("Failed to post status", error=e, exc_info=True)
