from concurrent import futures
from proto.webhook_pb2 import (
    BlockChain,
    Subscriber,
    WebhookRegistrationResponse,
    WebhookInquireResponse,
)
import grpc
from db import MongoConnector
from interceptor import AuthenticationInterceptor

import proto.webhook_pb2_grpc as webhook_pb2_grpc

mongoClient = MongoConnector()
scannerDb = mongoClient.getDB("webscanner")


class WebhookService(webhook_pb2_grpc.WebhookServiceServicer):
    def Register(self, request, context):
        return super().Register(request, context)

    def Unregister(self, request, context):
        return super().Unregister(request, context)

    def Inquire(self, request, context):
        query = {"webhook_url": request.webhook_url}
        try:
            subscribers = list(scannerDb["subscribers"].find(query))
        except Exception as e:
            # Handle any MongoDB query exceptions
            error_response = WebhookInquireResponse(
                success=False,
                message=f"Error querying subscribers: {str(e)}"
            )
            return error_response

        response = WebhookInquireResponse(
            success=True,
            message="Inquire successful",
        )

        try:
            for s in subscribers:
                subscriber = response.subscribers.add()
                subscriber.blockchain = BlockChain.Value(
                    s["blockchain"].upper())
                subscriber.wallet_address = s["wallet_address"]
                subscriber.webhook_url = s["webhook_url"]
        except Exception as e:
            # Handle any exceptions while populating the response
            error_response = WebhookInquireResponse(
                success=False,
                message=f"Error populating response: {str(e)}"
            )
            return error_response

        return response

    def DeleteAll(self, request, context):
        return super().DeleteAll(request, context)

    def GetHistory(self, request, context):
        return super().GetHistory(request, context)


def serve():
    authenticator = AuthenticationInterceptor(
        secret_key='cclemon',
        algorithm='HS256'
    )
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10), compression=grpc.Compression.Gzip, interceptors=(authenticator,))

    webhook_pb2_grpc.add_WebhookServiceServicer_to_server(
        WebhookService(), server
    )
    print('server start ')
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()  # run gRPC server
