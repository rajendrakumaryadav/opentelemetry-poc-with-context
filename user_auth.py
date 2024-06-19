import logging

from flask import Flask, request
from opentelemetry import context, trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from pydantic import BaseModel

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Get a tracer with the application name
tracer = trace.get_tracer(__name__)


class User(BaseModel):
    username: str
    password: str


class AuthFailException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


user = User(**{"username": "Rajendra", "password": "password"})


@app.route("/auth", methods=["POST"])
def auth():
    # Start a new span within the extracted context
    # with tracer.start_as_current_span("auth") as span:
        # Capture additional information about the request
        # span.set_attribute("http.method", request.method)
        # span.set_attribute("http.url", request.url)

        # Perform authentication logic
        if user.username == "Rajendra" and user.password == "password":
            # span.set_status(trace.StatusCode.OK)  # Set success status
            return {"auth": True}
        else:
            # span.set_status(trace.StatusCode.ERROR)  # Set error status
            # span.set_attribute("error.message", "Auth Failed")
            raise AuthFailException("Auth Failed")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
