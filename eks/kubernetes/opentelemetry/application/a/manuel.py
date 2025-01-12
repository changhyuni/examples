from flask import Flask, request
import requests
import os

from opentelemetry.propagate import extract, inject
from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

app = Flask(__name__)

# TracerProvider 및 Exporter 설정
set_tracer_provider(
    TracerProvider(
        resource=Resource(attributes={"service.name": "a"})
    )
)
tracer = get_tracer_provider().get_tracer(__name__)

B_HOST  = os.environ.get('B_HOST', 'b')
B_PORT  = os.environ.get('B_PORT', '7001')
HOST_IP = os.environ.get('HOST_IP', '10.0.0.0')

# Collector를 향한 OTLP Exporter 구성
otlp_exporter = OTLPSpanExporter(endpoint=f"http://{HOST_IP}:4318/v1/traces")
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

@app.route('/')
def call_app_b():
    ctx = extract(request.headers)
    attributes = collect_request_attributes(request.environ)

    with tracer.start_as_current_span(
        "a / call_b",
        context=ctx,
        kind=SpanKind.SERVER,
        attributes=attributes
    ) as span:
        url = f'http://{B_HOST}:{B_PORT}/'
        message = "A 입니다"

        # HTTP 요청 헤더에 Trace Context 주입
        headers = {}
        inject(headers)

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            message += " " + resp.text
        except Exception as e:
            print(f"[a] Error calling b: {e}")
            message += " (Error calling b)"
            span.record_exception(e)
            span.set_attribute("error", True)
        return message

if __name__ == '__main__':
    PORT = os.environ.get('PORT', '7000')
    app.run(host='0.0.0.0', port=int(PORT))
