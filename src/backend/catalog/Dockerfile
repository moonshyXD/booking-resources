FROM python:3.13-slim
WORKDIR /usr/app/backend/catalog
COPY pyproject.toml .
RUN pip install .
COPY . .
EXPOSE 8013
