FROM python:3.13-slim

# Копируем бинарник uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /usr/app/backend/iam

# Настраиваем uv:
# Отключаем компиляцию байткода для ускорения сборки
ENV UV_COMPILE_BYTECODE=1
# Запрещаем uv скачивать другой Python (используем системный 3.13)
ENV UV_PYTHON_DOWNLOADS=0

# Копируем файлы конфигурации (uv.lock скопируется, если он есть)
COPY pyproject.toml uv.lock* ./

# Этап 1: Устанавливаем ТОЛЬКО зависимости из pyproject.toml.
# --no-install-project говорит uv не пытаться устанавливать сам твой код.
# Это идеально сохраняет кэш Docker!
RUN uv sync --no-install-project --no-dev

# Этап 2: Копируем остальной код микросервиса
COPY . .

# Этап 3: Доустанавливаем сам проект (если нужно)
RUN uv sync --no-dev

EXPOSE 8012

# Запускаем через uv run (он сам найдет виртуальное окружение и uvicorn внутри него)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012"]