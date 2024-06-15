from concurrent import futures

import grpc
from opentelemetry import trace
from opentelemetry.context import attach, detach
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.propagate import extract
from opentelemetry.propagators.b3 import B3Format

import HealthStatus_pb2
import HealthStatus_pb2_grpc

tracer = trace.get_tracer(instrumenting_module_name="grpc_server")
GrpcInstrumentorServer().instrument()


class HealthServicer(HealthStatus_pb2_grpc.HealthServicer):
    def Check(self, request, context):
        carrier = dict(context.invocation_metadata())
        ctx = B3Format().extract(carrier)
        token = attach(ctx)
        try:
            with tracer.start_as_current_span("HealthCheck"):
                return HealthStatus_pb2.HealthCheckResponse(
                    status=HealthStatus_pb2.HealthCheckResponse.SERVING
                )
        finally:
            detach(token)


def serve():
    with tracer.start_as_current_span(
        "serving_grpc",
        kind=trace.SpanKind.SERVER,
        record_exception=True,
        set_status_on_exception=False,
    ) as span:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        HealthStatus_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), server)
        span.set_attribute("serving_grpc", span.get_span_context())
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()


if __name__ == "__main__":
    serve()
