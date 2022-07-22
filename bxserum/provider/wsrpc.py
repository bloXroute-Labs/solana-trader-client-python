from typing import Optional, Any, Dict, Type, TYPE_CHECKING

import betterproto
import jsonrpc

from bxserum.provider.wsrpc_error import RpcError

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from betterproto import T


class ProtoJsonRpcRequest(jsonrpc.JsonRpcRequest):
    def __init__(
        self, request_id: Optional[str], method: str, params: betterproto.Message
    ):
        super().__init__(
            request_id, method, params.to_dict(include_default_values=False)
        )


class ProtoJsonRpcResponse(jsonrpc.JsonRpcResponse[T]):
    _response_type: Type[T]

    def __init__(
        self,
        response_type: Type[T],
        request_id: Optional[str] = None,
        result: Optional[Any] = None,
        error: Optional[RpcError] = None,
    ):
        self._response_type = response_type
        super().__init__(request_id, result, error)

    def map_result(self, val: Any) -> T:
        return self._response_type().from_dict(val)
