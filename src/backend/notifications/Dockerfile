FROM python:3.13-slim

WORKDIR /usr/app/backend

COPY ./notifications/pyproject.toml ./notifications/

RUN pip install --no-cache-dir ./notifications

# 3. Копируем остальное
COPY ./shared ./shared
COPY ./notifications ./notifications

ENV PYTHONPATH=/usr/app/backend
EXPOSE 8011

CMD ["python", "-m", "uvicorn", "notifications.main:app", "--host", "0.0.0.0", "--port", "8011"]