FROM python:3.13-slim

WORKDIR /usr/app/backend

COPY ./shared ./shared

COPY ./booking/pyproject.toml ./booking/
RUN pip install --no-cache-dir ./booking


COPY ./booking ./booking

ENV PYTHONPATH=/usr/app/backend

EXPOSE 8014

CMD ["python", "-m", "uvicorn", "booking.main:app", "--host", "0.0.0.0", "--port", "8014"]