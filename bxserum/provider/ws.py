import asyncio
import json
from typing import TYPE_CHECKING, Type, Optional, AsyncGenerator

import aiohttp

from bxserum.provider import Provider
from bxserum.provider.base import NotConnectedException
from bxserum.provider.constants import DEFAULT_HOST, DEFAULT_WS_PORT
from bxserum.provider.wsrpc import JsonRpcRequest, JsonRpcResponse

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class WsProvider(Provider):
    _ws: Optional[aiohttp.ClientWebSocketResponse] = None

    _endpoint: str
    _session: aiohttp.ClientSession
    _request_id: int
    _request_lock: asyncio.Lock

    # noinspection PyMissingConstructor
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_WS_PORT):
        self._endpoint = f"ws://{host}:{port}/ws"
        self._session = aiohttp.ClientSession()
        self._request_id = 1
        self._request_lock = asyncio.Lock()

    async def connect(self):
        if self._ws is None:
            self._ws = await self._session.ws_connect(self._endpoint)

    async def close(self):
        ws = self._ws
        if ws is not None:
            await ws.close()

    async def _next_request_id(self) -> int:
        async with self._request_lock:
            previous = self._request_id
            self._request_id += 1
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
        ws = self._ws
        if ws is None:
            raise NotConnectedException()

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
        ws = self._ws
        if ws is None:
            raise NotConnectedException()

        request = await self._create_request(route, request)
        await ws.send_json(request.to_json())

        # https://bloxroute.atlassian.net/browse/BX-4123 this doesn't really work since it'll intercept all kinds of message
        msg: aiohttp.WSMessage
        async for msg in ws:
            rpc_result = JsonRpcResponse.from_json(json.loads(msg.data))
            yield _deserialize_result(rpc_result, response_type)


def _ws_endpoint(route: str) -> str:
    return route.split("/")[-1]


def _deserialize_result(rpc_response: JsonRpcResponse, response_type: Type["T"]) -> "T":
    return response_type().from_dict(rpc_response.result)
