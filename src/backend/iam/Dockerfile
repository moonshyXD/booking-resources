FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-cache && uv pip install uvicorn
COPY . .
EXPOSE 8012
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012"]