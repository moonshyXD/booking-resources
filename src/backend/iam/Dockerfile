FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /usr/app/backend/iam
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=0
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project --no-dev
COPY . .
RUN uv sync --no-dev
EXPOSE 8012
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012"]