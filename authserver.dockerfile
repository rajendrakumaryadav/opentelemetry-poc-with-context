FROM python:latest
WORKDIR /app
RUN pip install flask opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-exporter-otlp-proto-http opentelemetry-sdk opentelemetry-api grpcio-tools>1.64.1 grpcio>1.64.1 opentelemetry-instrumentation-requests python-dotenv
RUN opentelemetry-bootstrap -a install
RUN pip install opentelemetry-propagator-b3 pydantic opentelemetry-instrumentation-flask
COPY . /app/
EXPOSE 50051
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger:4317"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["opentelemetry-instrument", "--traces_exporter", "otlp,console", "--metrics_exporter", "otlp,console", "--logs_exporter", "console", "--service_name", "auth_server", "python", "user_auth.py"]
