from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING

import aiohttp

from bxserum import proto
from bxserum.provider.base import Provider

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class HttpProvider(Provider):
    endpoint: str

    # noinspection PyMissingConstructor
    def __init__(self, ip: str, port: int):
        self.endpoint = f"http://{ip}:{port}/api/v1"

    async def get_orderbook(
        self, *, market: str = "", limit: int = 0
    ) -> proto.GetOrderbookResponse:
        request = proto.GetOrderBookRequest()
        request.market = market
        request.limit = limit

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.endpoint}/market/orderbooks/{request.market}") as res:
                response = await res.json()
                return proto.GetOrderbookResponse().from_dict(response)

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
        yield NotImplementedError("streams not supported for HTTP")
        raise NotImplementedError("streams not supported for HTTP")
