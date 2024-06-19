FROM python:latest
WORKDIR /app
# COPY requirements.txt requirements.txt
RUN pip install flask opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-exporter-otlp-proto-http opentelemetry-sdk opentelemetry-api grpcio-tools>1.64.1 grpcio>1.64.1 python-dotenv
RUN opentelemetry-bootstrap -a install
RUN pip install opentelemetry-propagator-b3 requests opentelemetry-instrumentation-requests
COPY . /app/
RUN python -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. HealthStatus.proto
EXPOSE 5000
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger:4317"
CMD ["opentelemetry-instrument", "--traces_exporter", "otlp,console", "--metrics_exporter", "otlp,console", "--logs_exporter", "console", "--service_name", "app-poc", "python", "app.py"]
