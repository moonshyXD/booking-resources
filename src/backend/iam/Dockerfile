FROM python:3.13-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Настройка: заставляем uv ставить всё в системный Python и не создавать .venv
ENV UV_SYSTEM_PYTHON=1

# Копируем только файлы зависимостей
COPY pyproject.toml uv.lock* ./

# Синхронизируем зависимости.
# Мы добавляем uvicorn явно на случай, если его нет в pyproject.toml
RUN uv sync --no-cache && uv pip install uvicorn

# Копируем остальной код
COPY . .

EXPOSE 8012

# Используем `uv run`, это САМЫЙ надежный способ запуска
# Он сам найдет uvicorn, где бы тот ни лежал
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012"]