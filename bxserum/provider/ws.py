from typing import TYPE_CHECKING, Type, Optional, AsyncGenerator

import aiohttp

from bxserum.provider import Provider
from bxserum.provider.wsrpc import JsonRpcRequest

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class WsProvider(Provider):
    # noinspection PyMissingConstructor
    def __init__(self, ip: str, port: int):
        self.endpoint = f"ws://{ip}:{port}/ws"

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
                ws_endpoint = route.split("/")[-1]
                await ws.send_json(JsonRpcRequest("1", ws_endpoint, request).to_json())
                result = await ws.receive_json()
                return result

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
                async for msg in ws:
                    yield msg
