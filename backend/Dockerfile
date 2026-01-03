FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt update && apt install -y gcc python3-dev build-essential

COPY . .


RUN uv sync --frozen --no-cache

EXPOSE 2468
CMD [".venv/bin/uvicorn","src.main:app", "--port", "2468", "--host", "0.0.0.0", "--ws-ping-timeout", "60"]