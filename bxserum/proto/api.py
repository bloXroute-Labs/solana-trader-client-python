# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: api.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional

import betterproto
import grpclib


@dataclass
class GetMarketsRequest(betterproto.Message):
    pass


@dataclass
class GetMarketsResponse(betterproto.Message):
    markets: Dict[str, "Ticker"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass
class GetTickerRequest(betterproto.Message):
    market: str = betterproto.string_field(1)


@dataclass
class GetTickerResponse(betterproto.Message):
    ticker: "Ticker" = betterproto.message_field(1)


@dataclass
class Ticker(betterproto.Message):
    market: str = betterproto.string_field(1)
    status: str = betterproto.string_field(2)
    market_address: str = betterproto.string_field(3)
    close: float = betterproto.double_field(4)
    open: float = betterproto.double_field(5)
    amount: float = betterproto.double_field(6)
    volume: float = betterproto.double_field(7)
    count: float = betterproto.double_field(8)
    bid: float = betterproto.double_field(9)
    bid_size: float = betterproto.double_field(10)
    ask: float = betterproto.double_field(11)
    ask_size: float = betterproto.double_field(12)


@dataclass
class GetKlineRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    from_: datetime = betterproto.message_field(2)
    to: datetime = betterproto.message_field(3)
    resolution: str = betterproto.string_field(4)
    limit: int = betterproto.int32_field(5)


@dataclass
class GetKlineResponse(betterproto.Message):
    market: str = betterproto.string_field(1)
    timestamp: datetime = betterproto.message_field(2)
    candles: List["Candle"] = betterproto.message_field(3)


@dataclass
class Candle(betterproto.Message):
    start_time: datetime = betterproto.message_field(1)
    update_time: datetime = betterproto.message_field(2)
    open: float = betterproto.double_field(3)
    close: float = betterproto.double_field(4)
    low: float = betterproto.double_field(5)
    high: float = betterproto.double_field(6)
    amount: float = betterproto.double_field(7)
    volume: float = betterproto.double_field(8)
    count: float = betterproto.double_field(9)


@dataclass
class GetOrderBookRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    limit: int = betterproto.int32_field(2)


@dataclass
class GetOrderbookResponse(betterproto.Message):
    market: str = betterproto.string_field(1)
    bids: List["OrderbookBid"] = betterproto.message_field(2)
    asks: List["OrderbookAsk"] = betterproto.message_field(3)


@dataclass
class OrderbookBid(betterproto.Message):
    price: float = betterproto.double_field(1)
    size: float = betterproto.double_field(2)


@dataclass
class OrderbookAsk(betterproto.Message):
    price: float = betterproto.double_field(1)
    size: float = betterproto.double_field(2)


@dataclass
class GetTradesRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    from_: datetime = betterproto.message_field(2)
    limit: int = betterproto.int32_field(3)


@dataclass
class GetTradesResponse(betterproto.Message):
    trades: List["Trade"] = betterproto.message_field(1)


@dataclass
class Trade(betterproto.Message):
    side: str = betterproto.string_field(1)
    size: float = betterproto.double_field(2)
    price: float = betterproto.double_field(3)
    created_at: datetime = betterproto.message_field(4)


@dataclass
class GetServerTimeRequest(betterproto.Message):
    pass


@dataclass
class GetServerTimeResponse(betterproto.Message):
    timestamp: datetime = betterproto.message_field(1)


@dataclass
class GetAccountBalanceRequest(betterproto.Message):
    pass


@dataclass
class GetAccountBalanceResponse(betterproto.Message):
    tokens: List["TokenBalance"] = betterproto.message_field(1)


@dataclass
class TokenBalance(betterproto.Message):
    symbol: str = betterproto.string_field(1)
    amount: float = betterproto.double_field(2)


@dataclass
class PostOrderRequest(betterproto.Message):
    address: str = betterproto.string_field(1)
    market: str = betterproto.string_field(2)
    type: str = betterproto.string_field(3)
    amount: float = betterproto.double_field(4)
    price: float = betterproto.double_field(5)


@dataclass
class PostOrderResponse(betterproto.Message):
    status: str = betterproto.string_field(1)
    order_i_d: str = betterproto.string_field(2)


@dataclass
class PostCancelOrderRequest(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)


@dataclass
class PostCancelOrderResponse(betterproto.Message):
    status: str = betterproto.string_field(1)


@dataclass
class PostCancelAllRequest(betterproto.Message):
    market: str = betterproto.string_field(1)


@dataclass
class PostCancelAllResponse(betterproto.Message):
    statuses: List[str] = betterproto.string_field(1)


@dataclass
class PostSettleRequest(betterproto.Message):
    symbol: str = betterproto.string_field(1)


@dataclass
class PostSettleResponse(betterproto.Message):
    status: str = betterproto.string_field(1)
    settlement: "Settlement" = betterproto.message_field(2)


@dataclass
class Settlement(betterproto.Message):
    symbol: str = betterproto.string_field(1)
    unsettled: float = betterproto.double_field(2)
    amount: float = betterproto.double_field(3)


@dataclass
class GetOrdersRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    status: str = betterproto.string_field(2)
    side: str = betterproto.string_field(3)
    types: List[str] = betterproto.string_field(4)
    from_: datetime = betterproto.message_field(5)
    limit: int = betterproto.int32_field(6)
    direction: str = betterproto.string_field(7)


@dataclass
class GetOrdersResponse(betterproto.Message):
    orders: List["Order"] = betterproto.message_field(1)


@dataclass
class Order(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)
    market: str = betterproto.string_field(2)
    side: str = betterproto.string_field(3)
    types: List[str] = betterproto.string_field(4)
    price: float = betterproto.double_field(5)
    size: float = betterproto.double_field(6)
    remaining_size: float = betterproto.double_field(7)
    created_at: datetime = betterproto.message_field(8)
    status: str = betterproto.string_field(9)


@dataclass
class GetOpenOrdersRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    side: str = betterproto.string_field(2)
    types: List[str] = betterproto.string_field(3)
    from_: datetime = betterproto.message_field(4)
    limit: int = betterproto.int32_field(5)
    direction: str = betterproto.string_field(6)


@dataclass
class GetOpenOrdersResponse(betterproto.Message):
    status: str = betterproto.string_field(1)
    orders: List["Order"] = betterproto.message_field(2)


@dataclass
class GetOrderByIDRequest(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)


@dataclass
class GetOrderByIDResponse(betterproto.Message):
    status: str = betterproto.string_field(1)
    order: "Order" = betterproto.message_field(2)


@dataclass
class GetUnsettledRequest(betterproto.Message):
    symbol: str = betterproto.string_field(1)


@dataclass
class GetUnsettledResponse(betterproto.Message):
    symbol: str = betterproto.string_field(1)
    unsettled: float = betterproto.double_field(2)


@dataclass
class GetOrderbookStreamResponse(betterproto.Message):
    block_height: int = betterproto.int64_field(1)
    orderbook: "GetOrderbookResponse" = betterproto.message_field(2)


@dataclass
class GetTickerStreamResponse(betterproto.Message):
    block_height: int = betterproto.int64_field(1)
    ticker: "GetTickerResponse" = betterproto.message_field(2)


@dataclass
class GetMarketDepthRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    depth: int = betterproto.int32_field(2)
    step: int = betterproto.int32_field(3)


@dataclass
class GetMarketDepthStreamResponse(betterproto.Message):
    block_height: int = betterproto.int64_field(1)
    tick: "MarketDepthTick" = betterproto.message_field(2)


@dataclass
class MarketDepthTick(betterproto.Message):
    prev_block_height: int = betterproto.int64_field(1)
    asks: List["OrderbookAsk"] = betterproto.message_field(2)
    bids: List["OrderbookBid"] = betterproto.message_field(3)


@dataclass
class GetTradesStreamResponse(betterproto.Message):
    block_height: int = betterproto.int64_field(1)
    trades: "GetTradesResponse" = betterproto.message_field(2)


class ApiStub(betterproto.ServiceStub):
    async def get_markets(self) -> GetMarketsResponse:
        request = GetMarketsRequest()

        return await self._unary_unary(
            "/api.Api/GetMarkets",
            request,
            GetMarketsResponse,
        )

    async def get_ticker(self, *, market: str = "") -> GetTickerResponse:
        request = GetTickerRequest()
        request.market = market

        return await self._unary_unary(
            "/api.Api/GetTicker",
            request,
            GetTickerResponse,
        )

    async def get_kline(
        self,
        *,
        market: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        resolution: str = "",
        limit: int = 0,
    ) -> GetKlineResponse:
        request = GetKlineRequest()
        request.market = market
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        request.resolution = resolution
        request.limit = limit

        return await self._unary_unary(
            "/api.Api/GetKline",
            request,
            GetKlineResponse,
        )

    async def get_orderbook(
        self, *, market: str = "", limit: int = 0
    ) -> GetOrderbookResponse:
        request = GetOrderBookRequest()
        request.market = market
        request.limit = limit

        return await self._unary_unary(
            "/api.Api/GetOrderbook",
            request,
            GetOrderbookResponse,
        )

    async def get_trades(
        self, *, market: str = "", from_: Optional[datetime] = None, limit: int = 0
    ) -> GetTradesResponse:
        request = GetTradesRequest()
        request.market = market
        if from_ is not None:
            request.from_ = from_
        request.limit = limit

        return await self._unary_unary(
            "/api.Api/GetTrades",
            request,
            GetTradesResponse,
        )

    async def get_server_time(self) -> GetServerTimeResponse:
        request = GetServerTimeRequest()

        return await self._unary_unary(
            "/api.Api/GetServerTime",
            request,
            GetServerTimeResponse,
        )

    async def get_account_balance(self) -> GetAccountBalanceResponse:
        """account endpoints"""

        request = GetAccountBalanceRequest()

        return await self._unary_unary(
            "/api.Api/GetAccountBalance",
            request,
            GetAccountBalanceResponse,
        )

    async def post_order(
        self,
        *,
        address: str = "",
        market: str = "",
        type: str = "",
        amount: float = 0,
        price: float = 0,
    ) -> PostOrderResponse:
        """trade endpoints"""

        request = PostOrderRequest()
        request.address = address
        request.market = market
        request.type = type
        request.amount = amount
        request.price = price

        return await self._unary_unary(
            "/api.Api/PostOrder",
            request,
            PostOrderResponse,
        )

    async def post_cancel_order(
        self, *, order_i_d: str = ""
    ) -> PostCancelOrderResponse:
        request = PostCancelOrderRequest()
        request.order_i_d = order_i_d

        return await self._unary_unary(
            "/api.Api/PostCancelOrder",
            request,
            PostCancelOrderResponse,
        )

    async def post_cancel_all(self, *, market: str = "") -> PostCancelAllResponse:
        request = PostCancelAllRequest()
        request.market = market

        return await self._unary_unary(
            "/api.Api/PostCancelAll",
            request,
            PostCancelAllResponse,
        )

    async def post_settle(self, *, symbol: str = "") -> PostSettleResponse:
        request = PostSettleRequest()
        request.symbol = symbol

        return await self._unary_unary(
            "/api.Api/PostSettle",
            request,
            PostSettleResponse,
        )

    async def get_orders(
        self,
        *,
        market: str = "",
        status: str = "",
        side: str = "",
        types: List[str] = [],
        from_: Optional[datetime] = None,
        limit: int = 0,
        direction: str = "",
    ) -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.market = market
        request.status = status
        request.side = side
        request.types = types
        if from_ is not None:
            request.from_ = from_
        request.limit = limit
        request.direction = direction

        return await self._unary_unary(
            "/api.Api/GetOrders",
            request,
            GetOrdersResponse,
        )

    async def get_open_orders(
        self,
        *,
        market: str = "",
        side: str = "",
        types: List[str] = [],
        from_: Optional[datetime] = None,
        limit: int = 0,
        direction: str = "",
    ) -> GetOpenOrdersResponse:
        request = GetOpenOrdersRequest()
        request.market = market
        request.side = side
        request.types = types
        if from_ is not None:
            request.from_ = from_
        request.limit = limit
        request.direction = direction

        return await self._unary_unary(
            "/api.Api/GetOpenOrders",
            request,
            GetOpenOrdersResponse,
        )

    async def get_order_by_i_d(self, *, order_i_d: str = "") -> GetOrderByIDResponse:
        request = GetOrderByIDRequest()
        request.order_i_d = order_i_d

        return await self._unary_unary(
            "/api.Api/GetOrderByID",
            request,
            GetOrderByIDResponse,
        )

    async def get_unsettled(self, *, symbol: str = "") -> GetUnsettledResponse:
        request = GetUnsettledRequest()
        request.symbol = symbol

        return await self._unary_unary(
            "/api.Api/GetUnsettled",
            request,
            GetUnsettledResponse,
        )

    async def get_orderbook_updates(
        self, *, market: str = "", limit: int = 0
    ) -> AsyncGenerator[GetOrderbookStreamResponse, None]:
        """streaming endpoints"""

        request = GetOrderBookRequest()
        request.market = market
        request.limit = limit

        async for response in self._unary_stream(
            "/api.Api/GetOrderbookUpdates",
            request,
            GetOrderbookStreamResponse,
        ):
            yield response

    async def get_ticker_updates(
        self, *, market: str = ""
    ) -> AsyncGenerator[GetTickerStreamResponse, None]:
        request = GetTickerRequest()
        request.market = market

        async for response in self._unary_stream(
            "/api.Api/GetTickerUpdates",
            request,
            GetTickerStreamResponse,
        ):
            yield response

    async def get_market_depth_updates(
        self,
    ) -> AsyncGenerator[GetMarketDepthStreamResponse, None]:
        request = GetMarketsRequest()

        async for response in self._unary_stream(
            "/api.Api/GetMarketDepthUpdates",
            request,
            GetMarketDepthStreamResponse,
        ):
            yield response

    async def get_trade_updates(
        self, *, market: str = "", from_: Optional[datetime] = None, limit: int = 0
    ) -> AsyncGenerator[GetTradesStreamResponse, None]:
        request = GetTradesRequest()
        request.market = market
        if from_ is not None:
            request.from_ = from_
        request.limit = limit

        async for response in self._unary_stream(
            "/api.Api/GetTradeUpdates",
            request,
            GetTradesStreamResponse,
        ):
            yield response
