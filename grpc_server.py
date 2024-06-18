from concurrent import futures

import grpc
from opentelemetry import trace
from opentelemetry.context import attach, detach
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator

import HealthStatus_pb2
import HealthStatus_pb2_grpc

tracer = trace.get_tracer(instrumenting_module_name="grpc_server")

class HealthServicer(HealthStatus_pb2_grpc.HealthServicer):
    def Check(self, request, context):
        with tracer.start_as_current_span("HealthCheck") as span:
            span.set_attribute('status', str(HealthStatus_pb2.HealthCheckResponse.SERVING))
            return HealthStatus_pb2.HealthCheckResponse(
                status=HealthStatus_pb2.HealthCheckResponse.SERVING
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    HealthStatus_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
