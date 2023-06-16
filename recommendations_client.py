from proto.recommendations_pb2 import BookCategory, RecommendationRequest
from proto.recommendations_pb2_grpc import RecommendationsStub
import grpc

# build connect with grpc server 50051 is the default port used for grpc
channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)
request = RecommendationRequest(
    user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
# 遠程過程調用
response = client.Recommend(request)
print(response)
