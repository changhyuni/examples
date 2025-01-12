FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install Flask requests
RUN pip install opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-flask
RUN opentelemetry-bootstrap -a install

CMD ["opentelemetry-instrument", "python", "programmatic.py"]