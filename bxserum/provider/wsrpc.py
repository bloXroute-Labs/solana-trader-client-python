from typing import Optional, Any, Dict

import betterproto




class JsonRpcRequest:
    id: Optional[str]
    method_name: str
    params: betterproto.Message

    def __init__(
        self,
        request_id: Optional[str],
        method: str,
        params: betterproto.Message,
    ) -> None:
        self.id = request_id
        self.method_name = method
        self.params = params
        self.json_rpc_version = "2.0"

    def to_json(self) -> Dict[str, Any]:
        return {
            "jsonrpc": self.json_rpc_version,
            "id": self.id,
            "method": self.method_name,
            "params": self.params.to_dict(include_default_values=True),
        }

# class JsonRpcResponse:
#     id: Optional[str]
#     result: Optional[Any]
#     error: Optional[RpcError]
