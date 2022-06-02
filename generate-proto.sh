#!/usr/bin/env bash

PROTOBUF_PATH=/Users/dumitrucantemir/Workspace/serum-api-deployment/serum-api/proto

protoc -I $PROTOBUF_PATH --python_betterproto_out=bxserum/proto $PROTOBUF_PATH/api.proto

