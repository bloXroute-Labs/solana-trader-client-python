from typing import Type, TYPE_CHECKING

import grpclib.const
from grpclib import client

from bxserum.provider.base import Provider, T

if TYPE_CHECKING:
    from grpclib._protocols import IProtoMessage


class GrpcProvider(Provider):
    def __init__(self, ip: str, port: int):
        self.channel = client.Channel(ip, port)

    async def request(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ):
        async with self.channel.request(
            route, grpclib.const.Cardinality.UNARY_UNARY, type(request), response_type
        ) as stream:
            await stream.send_message(request, end=True)
            response = await stream.recv_message()
            assert response is not None
            return response

    async def stream(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ):
        # TODO: request kwargs
        async with self.channel.request(
            route, grpclib.const.Cardinality.UNARY_STREAM, type(request), response_type
        ) as stream:
            await stream.send_message(request, end=True)
            async for message in stream:
                yield message

    def close(self):
        self.channel.close()
