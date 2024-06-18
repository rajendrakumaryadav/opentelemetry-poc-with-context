import logging

import grpc
import requests
from flask import Flask, request
from opentelemetry import baggage, context, propagators, trace
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.instrumentation.asgi import collect_request_attributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator

import HealthStatus_pb2
import HealthStatus_pb2_grpc

app = Flask(__name__, template_folder="templates")


logger = logging.getLogger(__name__)

tracer = trace.get_tracer(__name__)

def get_users() -> dict:
    return [{"id": 1, "name": "Rajendra"}, {"id": 2, "name": "Arindam"}]


def check_backend() -> str:
        carrier = {}
        with tracer.start_as_current_span('check_backend') as span:
            with grpc.insecure_channel("grpc:50051") as channel:
                stub = HealthStatus_pb2_grpc.HealthStub(channel)
                response = stub.Check(
                    HealthStatus_pb2.HealthCheckRequest()
                )
                propagator = TraceContextTextMapPropagator()
                propagator.inject(carrier, context=None)
                logger.info(f"Health check response: {response}")
                return f"Health check response: {response}"


@app.route("/")
def index():
    with tracer.start_as_current_span('in the index') as span:
        logger.debug("Logging the backend status")
        response = requests.post(
            "http://auth:5000/auth", data={"data": "data"}
        )

        logging.info(response.json())
        if response.status_code == 200:
            logger.info("Received the data, you are authorized")
        else:
            return {"auth": False}
        logger.info(check_backend())
        users = get_users()
        return users


if __name__ == "__main__":
    logger.info("Application is live now.")
    app.run(debug=False, host="0.0.0.0", port=5000)
