FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_NO_DEV=1

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY pyproject.toml uv.lock ./
RUN uv pip install --no-cache --system -r pyproject.toml

COPY meme_bot .
COPY settings*.ini ./

ENTRYPOINT ["python", "main.py"]
