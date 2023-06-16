.PHONY: build-proto run-server run-client

build-proto:
	python3 -m grpc_tools.protoc -I ./proto --python_out=./proto --grpc_python_out=./proto ./proto/webhook.proto

run-server:
	python3 server.py

run-client:
	python3 client.py