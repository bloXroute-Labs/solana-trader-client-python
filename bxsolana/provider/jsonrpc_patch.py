import enum
from jsonrpc.types.server_error import RpcErrorCode, message_map, RpcError


class NewRpcErrorCode(enum.Enum):
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    AUTHORIZATION_ERROR = -32004
    RATE_LIMIT_ERROR = -32005
    STREAM_LIMIT_ERROR = -32006

    def message(self) -> str:
        return message_map[self]


RpcErrorCode = NewRpcErrorCode  # noqa: F811

message_map = {  # noqa: F811
    NewRpcErrorCode.PARSE_ERROR: "Parse error",
    NewRpcErrorCode.INVALID_REQUEST: "Invalid request",
    NewRpcErrorCode.METHOD_NOT_FOUND: "Invalid method",
    NewRpcErrorCode.INVALID_PARAMS: "Invalid params",
    NewRpcErrorCode.INTERNAL_ERROR: "Internal error",
    NewRpcErrorCode.AUTHORIZATION_ERROR: "Invalid account ID",
    NewRpcErrorCode.RATE_LIMIT_ERROR: "Rate limit reached",
    NewRpcErrorCode.STREAM_LIMIT_ERROR: "Max number of subscriptions error",
}

# Save the original from_json method
original_from_json = RpcError.from_json


# Define a new from_json method
@classmethod
def new_from_json(cls, payload: dict):
    code = payload.get("code")
    message = payload.get("message", "")
    data = payload.get("data")
    request_id = payload.get("id")

    if code in [e.value for e in RpcErrorCode]:
        return cls(RpcErrorCode(code), request_id, data, message=message)
    else:
        # Fallback (shouldn't happen)
        return original_from_json(cls, payload)


# Patch the RpcError class with the new from_json method
RpcError.from_json = new_from_json
