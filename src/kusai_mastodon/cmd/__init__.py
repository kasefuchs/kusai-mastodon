from pathlib import Path

import typer

from kusai_mastodon.model import Context

from .login import app as login_app
from .train import app as train_app
from .reply import app as reply_app
from .post import app as post_app

app = typer.Typer()
app.add_typer(login_app)
app.add_typer(train_app)
app.add_typer(reply_app)
app.add_typer(post_app)


@app.callback()
def main(ctx: typer.Context, config_path: Path = Path("config.yaml")):
    ctx.obj = Context.load(config_path)


__all__ = ("app",)
