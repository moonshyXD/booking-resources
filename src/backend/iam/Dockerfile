FROM python:3.13-slim

WORKDIR /usr/app/backend

COPY ./iam/pyproject.toml ./iam/

RUN pip install --no-cache-dir ./iam

COPY ./shared ./shared
COPY ./iam ./iam

ENV PYTHONPATH=/usr/app/backend
EXPOSE 8012

CMD ["python", "-m", "uvicorn", "iam.main:app", "--host", "0.0.0.0", "--port", "8012"]