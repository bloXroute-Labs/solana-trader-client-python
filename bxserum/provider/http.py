import datetime
from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING, List

import aiohttp
from solana import keypair

from bxserum import proto, transaction
from bxserum.provider.base import Provider
from bxserum.provider.constants import DEFAULT_HOST, DEFAULT_HTTP_PORT
from bxserum.provider.http_error import map_response

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class HttpProvider(Provider):
    _endpoint: str
    _session: aiohttp.ClientSession
    _private_key: keypair.Keypair

    # noinspection PyMissingConstructor
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_HTTP_PORT,
        private_key: Optional[str] = None,
    ):
        self._endpoint = f"http://{host}:{port}/api/v1"
        self._session = aiohttp.ClientSession()

        if private_key is None:
            self._private_key = transaction.load_private_key_from_env()
        else:
            self._private_key = transaction.load_private_key(private_key)

    async def connect(self):
        pass

    def private_key(self) -> keypair.Keypair:
        return self._private_key

    async def close(self):
        await self._session.close()

    async def get_markets(self) -> proto.GetMarketsResponse:
        async with self._session.get(f"{self._endpoint}/market/markets") as res:
            return await map_response(res, proto.GetMarketsResponse())

    async def get_orderbook(
        self, *, market: str = "", limit: int = 0
    ) -> proto.GetOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint}/market/orderbooks/{market}?limit={limit}"
        ) as res:
            return await map_response(res, proto.GetOrderbookResponse())

    async def get_tickers(self, *, market: str = "") -> proto.GetTickersResponse:
        async with self._session.get(
            f"{self._endpoint}/market/tickers/{market}"
        ) as res:
            return await map_response(res, proto.GetTickersResponse())

    async def get_orders(
        self,
        *,
        market: str = "",
        status: proto.OrderStatus = 0,
        side: proto.Side = 0,
        types: List[proto.OrderType] = [],
        from_: Optional[datetime.datetime] = None,
        limit: int = 0,
        direction: proto.Direction = 0,
        address: str = "",
    ) -> proto.GetOrdersResponse:
        raise NotImplementedError()

    async def get_open_orders(
        self,
        *,
        market: str = "",
        side: proto.Side = 0,
        types: List[proto.OrderType] = [],
        from_: Optional[datetime.datetime] = None,
        limit: int = 0,
        direction: proto.Direction = proto.Direction.D_ASCENDING,
        address: str = "",
    ) -> proto.GetOpenOrdersResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/orders/{market}"
            f"?address={address}"
            f"&side={side}"
            f"&types=OT_LIMIT"
            f"&direction={direction.name}"
        ) as res:
            return await map_response(res, proto.GetOpenOrdersResponse())

    async def get_order_by_i_d(self, *, order_i_d: str = "") -> proto.GetOrderByIDResponse:
        # TODO
        raise NotImplementedError()

    async def get_unsettled(
        self, *, market: str = "", owner: str = ""
    ) -> proto.GetUnsettledResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/unsettled/{market}"
            f"?owner={owner}"
        ) as res:
            return await map_response(res, proto.GetUnsettledResponse())

    async def post_order(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: "proto.Side" = 0,
        type: List["proto.OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
    ) -> proto.PostOrderResponse:
        request = proto.PostOrderRequest(
            owner_address,
            payer_address,
            market,
            side,
            type,
            amount,
            price,
            open_orders_address,
            client_order_i_d,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/place", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_submit(self, *, transaction: str = "") -> proto.PostSubmitResponse:
        request = proto.PostSubmitRequest(transaction)
        async with self._session.post(
            f"{self._endpoint}/trade/submit", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

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
