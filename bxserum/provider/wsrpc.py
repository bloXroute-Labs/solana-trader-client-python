from typing import Optional, Any, Dict

import betterproto

from bxserum.provider.wsrpc_error import RpcError

_rpc_version = "2.0"


class JsonRpcRequest:
    id: Optional[str]
    method_name: str
    params: betterproto.Message

    def __init__(
        self,
        request_id: int,
        method: str,
        params: betterproto.Message,
    ) -> None:
        self.id = str(request_id)
        self.method_name = method
        self.params = params
        self.json_rpc_version = _rpc_version

    def to_json(self) -> Dict[str, Any]:
        return {
            "jsonrpc": self.json_rpc_version,
            "id": self.id,
            "method": self.method_name,
            "params": self.params.to_dict(include_default_values=False),
        }


class JsonRpcResponse:
    id: Optional[str]
    result: Optional[Any]
    error: Optional[RpcError]

    def __init__(
        self,
        request_id: Optional[str],
        result: Optional[Any] = None,
        error: Optional[RpcError] = None,
    ) -> None:
        if (result is not None) and (error is not None):
            raise ValueError(
                "Cannot instantiate a JsonRpcResponse with both an error and a result."
            )

        self.id = request_id
        self.result = result
        self.error = error
        self.json_rpc_version = _rpc_version

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "JsonRpcResponse":
        if not ("result" not in payload) ^ ("error" not in payload):
            raise ValueError(
                "Cannot instantiate a message with neither (or both) a result and error."
            )

        rpc_error = payload.get("error", None)
        if rpc_error is not None:
            rpc_error = RpcError.from_json(rpc_error)

        return cls(
            payload.get("id", None),
            payload.get("result", None),
            rpc_error,
        )
