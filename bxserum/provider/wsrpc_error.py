import enum
from typing import Optional, Dict, Any

# copied mostly from bxcommon/src/bxcommon/rpc/rpc_errors.py
# should create a small package for this


class RpcErrorCode(enum.Enum):
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


ERROR_MESSAGE_MAPPINGS = {
    RpcErrorCode.PARSE_ERROR: "Parse error",
    RpcErrorCode.INVALID_REQUEST: "Invalid request",
    RpcErrorCode.METHOD_NOT_FOUND: "Invalid method",
    RpcErrorCode.INVALID_PARAMS: "Invalid params",
    RpcErrorCode.INTERNAL_ERROR: "Internal error",
}


class RpcError(Exception):
    def __init__(
        self,
        code: RpcErrorCode,
        request_id: Optional[str],
        data: Optional[Any],
        message: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.code = code
        if message:
            self.message = message
        else:
            self.message = ERROR_MESSAGE_MAPPINGS[code]
        self.data = data
        self.id = request_id

    def to_json(self) -> Dict[str, Any]:
        fields = {
            "code": self.code.value,
            "message": self.message,
        }
        if self.data is not None:
            fields["data"] = self.data
        return fields

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "RpcError":
        return cls(
            RpcErrorCode(payload["code"]),
            None,
            payload.get("data"),
            payload.get("message"),
        )


class RpcParseError(RpcError):
    def __init__(
        self, request_id: Optional[str] = None, data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.PARSE_ERROR, request_id, data)


class RpcInvalidRequest(RpcError):
    def __init__(self, request_id: Optional[str], data: Optional[Any] = None) -> None:
        super().__init__(RpcErrorCode.INVALID_REQUEST, request_id, data)


class RpcMethodNotFound(RpcError):
    def __init__(self, request_id: Optional[str], data: Optional[Any] = None) -> None:
        super().__init__(RpcErrorCode.METHOD_NOT_FOUND, request_id, data)


class RpcInvalidParams(RpcError):
    def __init__(self, request_id: Optional[str], data: Optional[Any] = None) -> None:
        super().__init__(RpcErrorCode.INVALID_PARAMS, request_id, data)


class RpcInternalError(RpcError):
    def __init__(self, request_id: Optional[str], data: Optional[Any] = None) -> None:
        super().__init__(RpcErrorCode.INTERNAL_ERROR, request_id, data)


