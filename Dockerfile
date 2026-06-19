FROM python:3.12-slim AS build

# install deps
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --assume-yes && \
    apt-get install --assume-yes --no-install-recommends build-essential ca-certificates clang cmake git libabsl-dev libxxhash-dev ninja-build nlohmann-json3-dev pkg-config pybind11-dev && \
    apt-get clean --assume-yes

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# build app
WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-install-project --no-dev

COPY src ./src
RUN uv sync --no-dev

FROM python:3.12-slim AS app

# install deps
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --assume-yes && \
    apt-get install --assume-yes --no-install-recommends libabsl20240722 && \
    apt-get clean --assume-yes

# install app
WORKDIR /app

COPY --from=build /app ./

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src" \
    PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python3", "-m", "kusai_mastodon"]
