FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m pip install --upgrade pip uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --no-cache --system -r pyproject.toml

COPY meme_bot .
COPY settings*.ini ./

ENTRYPOINT ["python", "main.py"]
