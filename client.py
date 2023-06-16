from proto.webhook_pb2 import BlockChain, WebhookRegistrationRequest, WebhookInquireRequest
import grpc
import proto.webhook_pb2_grpc as webhook_pb2_grpc


def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = webhook_pb2_grpc.WebhookServiceStub(channel)

    # Add token to request header
    metadata = [('authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6MTIzfQ.VN3rdvWj7P580jzeUKHf7BekkIGA8RBzO9ZswJ5QzgA')]
    # Register a subscriber
    registration_request = WebhookRegistrationRequest(
        blockchain=BlockChain.ETHEREUM,
        wallet_address="0x43C7AC9Cc89C4E11176087B42d5659b790BAf733",
        webhook_url="https://553b-36-225-73-127.ngrok-free.app"
    )
    registration_response = stub.Register(
        registration_request, metadata=metadata)
    if registration_response.success:
        print("Registration successful")
    else:
        print("Registration failed:", registration_response.message)

    # Inquire subscribers
    inquire_request = WebhookInquireRequest(
        webhook_url="https://553b-36-225-73-127.ngrok-free.app"
    )
    inquire_response = stub.Inquire(inquire_request, metadata=metadata)
    if inquire_response.success:
        print("Inquire successful")
        for subscriber in inquire_response.subscribers:
            print("Blockchain:", subscriber.blockchain)
            print("Wallet Address:", subscriber.wallet_address)
            print("Webhook URL:", subscriber.webhook_url)
    else:
        print("Inquire failed:", inquire_response.message)


if __name__ == "__main__":
    run_client()
