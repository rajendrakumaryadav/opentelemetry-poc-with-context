import logging

import grpc
from flask import Flask
from opentelemetry import trace
from opentelemetry.context import context
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators import b3
from opentelemetry.propagators.b3 import B3Format
from opentelemetry.trace import SpanContext

import HealthStatus_pb2
import HealthStatus_pb2_grpc

set_global_textmap(b3.B3Format())
app = Flask(__name__, template_folder="templates")

FlaskInstrumentor().instrument_app(app)
GrpcInstrumentorClient().instrument()

logger = logging.getLogger(__name__)

tracer = trace.get_tracer(__name__)


def get_users() -> dict:
    return [{"id": 1, "name": "Rajendra"}, {"id": 2, "name": "Ragini"}]


def check_backend() -> str:
    with tracer.start_as_current_span("check_backend") as span:
        with grpc.insecure_channel("grpc:50051") as channel:
            stub = HealthStatus_pb2_grpc.HealthStub(channel)
            carrier = {}
            B3Format().inject(carrier)
            metadata = [(k, v) for k, v in carrier.items()]
            response = stub.Check(
                HealthStatus_pb2.HealthCheckRequest(), metadata=metadata
            )
            span.set_attribute("health_status", str(response))
            logger.info(f"Health check response: {response}")
            return f"Health check response: {response}"


@app.route("/")
def index():
    logger.debug("Logging the backend status")
    logger.info(check_backend())
    users = get_users()
    return users


if __name__ == "__main__":
    logger.info("Application is live now.")
    app.run(debug=False, host="0.0.0.0", port=5000)
