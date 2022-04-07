import asyncio
import json
from typing import TYPE_CHECKING, Type, Optional, AsyncGenerator

import aiohttp

from bxserum.provider import Provider
from bxserum.provider.wsrpc import JsonRpcRequest, JsonRpcResponse

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class WsProvider(Provider):
    # noinspection PyMissingConstructor
    def __init__(self, ip: str, port: int):
        self.endpoint = f"ws://{ip}:{port}/ws"
        self.request_id = 1
        self.request_lock = asyncio.Lock()

    async def _next_request_id(self) -> int:
        async with self.request_lock:
            previous = self.request_id
            self.request_id += 1
            return previous

    async def _create_request(
        self, route: str, request: "IProtoMessage"
    ) -> JsonRpcRequest:
        return JsonRpcRequest(
            await self._next_request_id(), _ws_endpoint(route), request
        )

    async def _unary_unary(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> "T":
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.endpoint) as ws:
                request = await self._create_request(route, request)
                await ws.send_json(request.to_json())

                raw_result = await ws.receive_json()
                rpc_result = JsonRpcResponse.from_json(raw_result)
                return _deserialize_result(rpc_result, response_type)

    async def _unary_stream(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> AsyncGenerator["T", None]:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.endpoint) as ws:
                request = await self._create_request(route, request)
                await ws.send_json(request.to_json())

                msg: aiohttp.WSMessage
                async for msg in ws:
                    rpc_result = JsonRpcResponse.from_json(json.loads(msg.data))
                    yield _deserialize_result(rpc_result, response_type)


def _ws_endpoint(route: str) -> str:
    return route.split("/")[-1]


def _deserialize_result(rpc_response: JsonRpcResponse, response_type: Type["T"]) -> "T":
    return response_type().from_dict(rpc_response.result)
