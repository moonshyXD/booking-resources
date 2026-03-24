FROM python:3.13-slim

WORKDIR /usr/app/backend

COPY ./shared ./shared

COPY ./catalog/pyproject.toml ./catalog/
RUN pip install --no-cache-dir ./catalog

COPY ./catalog ./catalog

ENV PYTHONPATH=/usr/app/backend

EXPOSE 8013

CMD ["python", "-m", "uvicorn", "catalog.main:app", "--host", "0.0.0.0", "--port", "8013"]