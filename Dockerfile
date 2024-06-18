FROM python:latest
WORKDIR /app
# COPY requirements.txt requirements.txt
RUN pip install flask opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-exporter-otlp-proto-http opentelemetry-sdk opentelemetry-api grpcio-tools>1.64.1 grpcio>1.64.1 python-dotenv
RUN opentelemetry-bootstrap -a install
RUN pip install opentelemetry-propagator-b3 requests opentelemetry-instrumentation-requests
COPY . /app/
RUN python -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. HealthStatus.proto
EXPOSE 5000
RUN echo "Working in ${pwd}"
CMD ["opentelemetry-instrument", "--traces_exporter", "otlp_proto_http", "--metrics_exporter", "console", "--logs_exporter", "console", "--service_name", "app-poc", "python", "app.py"]
