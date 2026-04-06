FROM python:3.12-slim AS build

ARG VCPKG_BRANCH=2026.03.18

# copy rootfs
COPY docker/rootfs/build/ /

# install deps
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --assume-yes && \
    apt-get install --assume-yes --no-install-recommends build-essential ca-certificates clang cmake curl git libabsl-dev libcli11-dev ninja-build nlohmann-json3-dev pkg-config pybind11-dev tar unzip zip && \
    apt-get clean --assume-yes

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# install vcpkg
ENV VCPKG_ROOT=/opt/vcpkg
ENV VCPKG_OVERLAY_PORTS=/opt/vcpkg-overlay-ports
ENV VCPKG_FORCE_SYSTEM_BINARIES=1

RUN mkdir -p $VCPKG_ROOT && cd $VCPKG_ROOT && \
    git clone --branch $VCPKG_BRANCH --filter=tree:0 https://github.com/microsoft/vcpkg.git . && \
    ./bootstrap-vcpkg.sh -disableMetrics

ENV PATH=${VCPKG_ROOT}:${PATH}
ENV CMAKE_ARGS="-DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"

# build app
WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-install-project --no-dev

COPY src ./src
RUN uv sync --no-dev

FROM python:3.12-slim AS app

# install deps
RUN apt-get update --assume-yes && \
    apt-get install --assume-yes --no-install-recommends libabsl-dev && \
    apt-get clean --assume-yes

# install app
WORKDIR /app

COPY --from=build /app ./

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src" \
    PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python3", "-m", "kusai_mastodon"]
