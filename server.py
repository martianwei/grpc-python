from concurrent import futures
from proto.webhook_pb2 import (
    Subscriber,
    WebhookRegistrationResponse,
    WebhookInquireResponse,
    WebhookDeleteAllResponse,
    WebhookGetHistoryResponse,
)
import grpc
from db import MongoConnector
from interceptor import AuthenticationInterceptor
from datetime import datetime
import proto.webhook_pb2_grpc as webhook_pb2_grpc
import requests

mongoClient = MongoConnector()
scannerDb = mongoClient.getDB("webscanner")


class WebhookService(webhook_pb2_grpc.WebhookServiceServicer):
    def Register(self, request, context):
        try:
            res = requests.post(
                url=request.webhook_url,
                json={
                    "blockchain": request.blockchain,
                    "wallet_address": request.wallet_address,
                    "transactions": [],
                },
                timeout=5,
            )
            res.raise_for_status()  # Raise an exception if response status code is not 2xx

            query = {
                "blockchain": request.blockchain,
                "wallet_address": request.wallet_address,
                "webhook_url": request.webhook_url,
            }
            update = {
                "$set": {
                    "blockchain": request.blockchain,
                    "wallet_address": request.wallet_address,
                    "webhook_url": request.webhook_url,
                    "retry_count": 0,
                    "status": "active",
                    "is_delete": False,
                    "updated_at": int(datetime.timestamp(datetime.now())),
                },
                "$setOnInsert": {
                    "created_at": int(datetime.timestamp(datetime.now())),
                }
            }
            scannerDb["subscribers"].update_one(query, update, upsert=True)

            return WebhookRegistrationResponse(
                success=True,
                message="Register successful",
                subscriber=Subscriber(
                    blockchain=request.blockchain,
                    wallet_address=request.wallet_address,
                    webhook_url=request.webhook_url,
                ),
            )
        except requests.exceptions.RequestException as e:
            return WebhookRegistrationResponse(
                success=False,
                message=f"Error registering webhook: {str(e)}"
            )
        except Exception as e:
            return WebhookRegistrationResponse(
                success=False,
                message=f"Unknown error occurred during webhook registration: {str(e)}"
            )

    def Unregister(self, request, context):
        try:
            query = {
                "blockchain": request.blockchain,
                "wallet_address": request.wallet_address,
                "webhook_url": request.webhook_url
            }
            subscriber = scannerDb["subscribers"].find_one_and_delete(query)

            if subscriber:
                return WebhookRegistrationResponse(
                    success=True,
                    message="Unregister successful",
                    subscriber=Subscriber(
                        blockchain=subscriber["blockchain"],
                        wallet_address=subscriber["wallet_address"],
                        webhook_url=subscriber["webhook_url"],
                    ),
                )
            else:
                return WebhookRegistrationResponse(
                    success=False,
                    message="subscriber doesn't exist",
                )
        except Exception as e:
            return WebhookRegistrationResponse(
                success=False,
                message=f"Error occurred during unregister: {str(e)}"
            )

    def Inquire(self, request, context):
        try:
            query = {"webhook_url": request.webhook_url}
            subscribers = list(scannerDb["subscribers"].find(query))

            response = WebhookInquireResponse(
                success=True,
                message="Inquire successful",
            )

            for s in subscribers:
                subscriber = response.subscribers.add()
                subscriber.blockchain = s["blockchain"]
                subscriber.wallet_address = s["wallet_address"]
                subscriber.webhook_url = s["webhook_url"]

            return response
        except Exception as e:
            error_response = WebhookInquireResponse(
                success=False,
                message=f"Error occurred during inquiry: {str(e)}"
            )
            return error_response

    def DeleteAll(self, request, context):
        try:
            subscribers = scannerDb["subscribers"].delete_many({})
            transactions = scannerDb["transactions"].delete_many({})

            response = WebhookDeleteAllResponse(
                success=True,
                message="Delete all successful",
                deleted_subscribers_count=subscribers.deleted_count,
                deleted_transactions_count=transactions.deleted_count,
            )

            return response
        except Exception as e:
            error_response = WebhookDeleteAllResponse(
                success=False,
                message=f"Error deleting subscribers: {str(e)}"
            )
            return error_response

    def GetHistory(self, request, context):
        try:
            query = {
                "blockchain": request.blockchain,
                "wallet_address": request.wallet_address,
            }
            subscriber = scannerDb["subscribers"].find_one(query)
            if not subscriber:
                return WebhookGetHistoryResponse(
                    success=False,
                    message="Subscriber not found",
                )
            tx_query = {
                "subscriber_id": str(subscriber["_id"]),
                "block_number": {
                    "$gte": request.start_block if request.start_block else 0,
                    "$lte": request.end_block if request.end_block else 999999999999999999,
                }
            }
            transactions = list(scannerDb["transactions"].find(
                tx_query).sort("timestamp", 1))

            response = WebhookGetHistoryResponse(
                success=True,
                message="GetHistory successful",
            )

            for t in transactions:
                txn = response.transactions.add()
                txn.blockchain = t["chain"]
                txn.txn_hash = t["txn_hash"]
                txn.type = t["type"]
                txn.block_number = t["block_number"]
                txn.timestamp = t["timestamp"]
                txn.address_from = t["address_from"]
                txn.address_to = t["address_to"]
                txn.amount = t["value"]
                txn.token_symbol = t["symbol"]
                txn.decimal = t["decimal"]
                txn.contract_address = t["contract_address"]
                txn.txn_fee = t["txn_fee"]

            return response
        except Exception as e:
            error_response = WebhookGetHistoryResponse(
                success=False,
                message=f"Error occurred during history retrieval: {str(e)}"
            )
            return error_response


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
