FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /code
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


# Then, use a final image without uv
FROM python:3.10-slim-bookworm
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.

# Copy the application from the builder
COPY --from=builder --chown=app:app /code /code

# Place executables in the environment at the front of the path
ENV PATH="/code/.venv/bin:$PATH"

# Run the FastAPI application by default

EXPOSE 8000
WORKDIR /code
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "[::]:8000", "app.main:app"]