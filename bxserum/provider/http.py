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
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_HTTP_PORT):
        self._endpoint = f"http://{host}:{port}/api/v1"
        self._session = aiohttp.ClientSession()
        self._private_key = transaction.load_private_key()

    async def connect(self):
        pass

    def private_key(self) -> keypair.Keypair:
        return self._private_key

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
            return await map_response(res, proto.GetOrderbookResponse())

    async def get_markets(self) -> proto.GetMarketsResponse:
        async with self._session.get(f"{self._endpoint}/market/markets") as res:
            return await map_response(res, proto.GetMarketsResponse())

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

    async def post_cancel_order(
        self,
        *,
        order_i_d: string = "",
        side: "proto.Side" = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> proto.PostCancelOrderResponse:
        request = proto.PostCancelOrderRequest(
            order_i_d,
            side,
            market_address,
            owner_address,
            open_orders_address,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/cancel", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_order_by_client_i_d(
        self,
        *,
        client_order_i_d: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> proto.PostCancelOrderByClientIDResponse:
        request = proto.PostCancelByClientOrderIDRequest(
            client_order_i_d,
            market_address,
            owner_address,
            open_orders_address,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/cancelbyid", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

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
