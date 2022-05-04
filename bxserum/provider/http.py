from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING

import aiohttp

from bxserum import proto
from bxserum.provider.base import Provider
from bxserum.provider.constants import DEFAULT_HOST, DEFAULT_HTTP_PORT

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class HttpProvider(Provider):
    _endpoint: str
    _session: aiohttp.ClientSession

    # noinspection PyMissingConstructor
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_HTTP_PORT):
        self._endpoint = f"http://{host}:{port}/api/v1"
        self._session = aiohttp.ClientSession()

    async def connect(self):
        pass

    async def close(self):
        await self._session.close()

    async def get_orderbook(
        self, *, market: str = "", limit: int = 0
    ) -> proto.GetOrderbookResponse:
        request = proto.GetOrderBookRequest()
        request.market = market
        request.limit = limit

        async with self._session.get(
            f"{self._endpoint}/market/orderbooks/{request.market}"
        ) as res:
            response = await res.json()
            return proto.GetOrderbookResponse().from_dict(response)

    async def get_markets(self) -> proto.GetMarketsResponse:
        async with self._session.get(
            f"{self._endpoint}/market/markets"
        ) as res:
            response = await res.json()
            return proto.GetMarketsResponse().from_dict(response)

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
        # seems to require yield some result otherwise this isn't an async generator?
        yield NotImplementedError("streams not supported for HTTP")
        raise NotImplementedError("streams not supported for HTTP")
