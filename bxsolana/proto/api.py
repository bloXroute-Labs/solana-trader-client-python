# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: api.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional

import betterproto
import grpclib


class MarketStatus(betterproto.Enum):
    MS_UNKNOWN = 0
    MS_ONLINE = 1


class Side(betterproto.Enum):
    S_UNKNOWN = 0
    S_BID = 1
    S_ASK = 2


class OrderType(betterproto.Enum):
    OT_MARKET = 0
    OT_LIMIT = 1
    OT_IOC = 2
    OT_POST = 3


class OrderStatus(betterproto.Enum):
    OS_UNKNOWN = 0
    OS_OPEN = 1
    OS_PARTIAL_FILL = 2
    OS_CANCELLED = 3
    OS_FILLED = 4


class Direction(betterproto.Enum):
    D_ASCENDING = 0
    D_DESCENDING = 1


class Step(betterproto.Enum):
    STEP0 = 0
    STEP1 = 1
    STEP2 = 2
    STEP3 = 3


@dataclass
class GetMarketsRequest(betterproto.Message):
    pass


@dataclass
class GetMarketsResponse(betterproto.Message):
    markets: Dict[str, "Market"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass
class Market(betterproto.Message):
    market: str = betterproto.string_field(1)
    status: "MarketStatus" = betterproto.enum_field(2)
    address: str = betterproto.string_field(3)
    base_mint: str = betterproto.string_field(4)
    quoted_mint: str = betterproto.string_field(5)
    base_decimals: int = betterproto.int64_field(6)
    quote_decimals: int = betterproto.int64_field(7)


@dataclass
class GetTickersRequest(betterproto.Message):
    market: str = betterproto.string_field(1)


@dataclass
class GetTickersResponse(betterproto.Message):
    tickers: List["Ticker"] = betterproto.message_field(1)


@dataclass
class Ticker(betterproto.Message):
    market: str = betterproto.string_field(1)
    market_address: str = betterproto.string_field(2)
    bid: float = betterproto.double_field(3)
    bid_size: float = betterproto.double_field(4)
    ask: float = betterproto.double_field(5)
    ask_size: float = betterproto.double_field(6)


@dataclass
class GetKlineRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    from_: datetime = betterproto.message_field(2)
    to: datetime = betterproto.message_field(3)
    resolution: str = betterproto.string_field(4)
    limit: int = betterproto.uint32_field(5)


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
class GetOrderbookRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    limit: int = betterproto.uint32_field(2)


@dataclass
class GetOrderbooksRequest(betterproto.Message):
    markets: List[str] = betterproto.string_field(1)
    limit: int = betterproto.uint32_field(2)


@dataclass
class GetOrderbookResponse(betterproto.Message):
    market: str = betterproto.string_field(1)
    market_address: str = betterproto.string_field(2)
    bids: List["OrderbookItem"] = betterproto.message_field(3)
    asks: List["OrderbookItem"] = betterproto.message_field(4)


@dataclass
class OrderbookItem(betterproto.Message):
    price: float = betterproto.double_field(1)
    size: float = betterproto.double_field(2)


@dataclass
class GetTradesRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    limit: int = betterproto.uint32_field(2)


@dataclass
class GetTradesResponse(betterproto.Message):
    trades: List["Trade"] = betterproto.message_field(1)


@dataclass
class Trade(betterproto.Message):
    side: "Side" = betterproto.enum_field(1)
    size: float = betterproto.double_field(2)
    price: float = betterproto.double_field(3)
    order_i_d: str = betterproto.string_field(4)
    is_maker: bool = betterproto.bool_field(5)


@dataclass
class GetServerTimeRequest(betterproto.Message):
    pass


@dataclass
class GetServerTimeResponse(betterproto.Message):
    timestamp: str = betterproto.string_field(1)


@dataclass
class GetAccountBalanceRequest(betterproto.Message):
    owner_address: str = betterproto.string_field(1)


@dataclass
class GetAccountBalanceResponse(betterproto.Message):
    tokens: List["TokenBalance"] = betterproto.message_field(1)


@dataclass
class TokenBalance(betterproto.Message):
    symbol: str = betterproto.string_field(1)
    address: str = betterproto.string_field(2)
    wallet_amount: float = betterproto.double_field(3)
    unsettled_amount: float = betterproto.double_field(4)
    open_orders_amount: float = betterproto.double_field(5)


@dataclass
class PostOrderRequest(betterproto.Message):
    owner_address: str = betterproto.string_field(1)
    payer_address: str = betterproto.string_field(2)
    market: str = betterproto.string_field(3)
    side: "Side" = betterproto.enum_field(4)
    type: List["OrderType"] = betterproto.enum_field(5)
    amount: float = betterproto.double_field(6)
    price: float = betterproto.double_field(7)
    open_orders_address: str = betterproto.string_field(8)
    client_order_i_d: int = betterproto.uint64_field(9)


@dataclass
class PostReplaceOrderRequest(betterproto.Message):
    owner_address: str = betterproto.string_field(1)
    payer_address: str = betterproto.string_field(2)
    market: str = betterproto.string_field(3)
    side: "Side" = betterproto.enum_field(4)
    type: List["OrderType"] = betterproto.enum_field(5)
    amount: float = betterproto.double_field(6)
    price: float = betterproto.double_field(7)
    open_orders_address: str = betterproto.string_field(8)
    client_order_i_d: int = betterproto.uint64_field(9)
    order_i_d: str = betterproto.string_field(10)


@dataclass
class PostOrderResponse(betterproto.Message):
    transaction: str = betterproto.string_field(1)
    open_orders_address: str = betterproto.string_field(2)


@dataclass
class PostCancelOrderRequest(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)
    side: "Side" = betterproto.enum_field(2)
    market_address: str = betterproto.string_field(3)
    owner_address: str = betterproto.string_field(4)
    open_orders_address: str = betterproto.string_field(5)


@dataclass
class PostCancelByClientOrderIDRequest(betterproto.Message):
    client_order_i_d: int = betterproto.uint64_field(1)
    market_address: str = betterproto.string_field(2)
    owner_address: str = betterproto.string_field(3)
    open_orders_address: str = betterproto.string_field(4)


@dataclass
class PostCancelOrderResponse(betterproto.Message):
    transaction: str = betterproto.string_field(1)


@dataclass
class PostCancelAllRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    owner_address: str = betterproto.string_field(2)
    open_orders_addresses: List[str] = betterproto.string_field(3)


@dataclass
class PostCancelAllResponse(betterproto.Message):
    transactions: List[str] = betterproto.string_field(1)


@dataclass
class PostSettleRequest(betterproto.Message):
    owner_address: str = betterproto.string_field(1)
    market: str = betterproto.string_field(2)
    base_token_wallet: str = betterproto.string_field(3)
    quote_token_wallet: str = betterproto.string_field(4)
    open_orders_address: str = betterproto.string_field(5)


@dataclass
class PostSettleResponse(betterproto.Message):
    transaction: str = betterproto.string_field(1)


@dataclass
class Settlement(betterproto.Message):
    symbol: str = betterproto.string_field(1)
    unsettled: float = betterproto.double_field(2)
    amount: float = betterproto.double_field(3)


@dataclass
class GetOrdersRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    status: "OrderStatus" = betterproto.enum_field(2)
    side: "Side" = betterproto.enum_field(3)
    types: List["OrderType"] = betterproto.enum_field(4)
    from_: datetime = betterproto.message_field(5)
    limit: int = betterproto.uint32_field(6)
    direction: "Direction" = betterproto.enum_field(7)
    address: str = betterproto.string_field(8)
    open_orders_address: str = betterproto.string_field(9)


@dataclass
class GetOrdersResponse(betterproto.Message):
    orders: List["Order"] = betterproto.message_field(1)


@dataclass
class Order(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)
    market: str = betterproto.string_field(2)
    side: "Side" = betterproto.enum_field(3)
    types: List["OrderType"] = betterproto.enum_field(4)
    price: float = betterproto.double_field(5)
    remaining_size: float = betterproto.double_field(6)
    created_at: datetime = betterproto.message_field(7)
    client_order_i_d: str = betterproto.string_field(8)
    open_order_account: str = betterproto.string_field(9)


@dataclass
class GetOrderStatusStreamRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    owner_address: str = betterproto.string_field(2)


@dataclass
class GetOrderStatusStreamResponse(betterproto.Message):
    slot: int = betterproto.int64_field(1)
    order_info: "GetOrderStatusResponse" = betterproto.message_field(2)


@dataclass
class GetOrderStatusResponse(betterproto.Message):
    market: str = betterproto.string_field(1)
    open_order_address: str = betterproto.string_field(2)
    order_i_d: str = betterproto.string_field(3)
    client_order_i_d: int = betterproto.uint64_field(4)
    quantity_released: float = betterproto.float_field(5)
    quantity_remaining: float = betterproto.float_field(6)
    price: float = betterproto.float_field(7)
    side: "Side" = betterproto.enum_field(8)
    order_status: "OrderStatus" = betterproto.enum_field(9)


@dataclass
class PostSubmitRequest(betterproto.Message):
    transaction: str = betterproto.string_field(1)
    skip_pre_flight: bool = betterproto.bool_field(2)


@dataclass
class PostSubmitResponse(betterproto.Message):
    signature: str = betterproto.string_field(1)


@dataclass
class GetOpenOrdersRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    limit: int = betterproto.uint32_field(2)
    address: str = betterproto.string_field(3)
    open_orders_address: str = betterproto.string_field(4)


@dataclass
class GetOpenOrdersResponse(betterproto.Message):
    orders: List["Order"] = betterproto.message_field(1)


@dataclass
class GetOrderByIDRequest(betterproto.Message):
    order_i_d: str = betterproto.string_field(1)
    market: str = betterproto.string_field(2)


@dataclass
class GetOrderByIDResponse(betterproto.Message):
    order: "Order" = betterproto.message_field(1)


@dataclass
class GetUnsettledRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    owner: str = betterproto.string_field(2)


@dataclass
class UnsettledAccountToken(betterproto.Message):
    address: str = betterproto.string_field(1)
    amount: float = betterproto.double_field(2)


@dataclass
class UnsettledAccount(betterproto.Message):
    account: str = betterproto.string_field(1)
    base_token: "UnsettledAccountToken" = betterproto.message_field(2)
    quote_token: "UnsettledAccountToken" = betterproto.message_field(3)


@dataclass
class GetUnsettledResponse(betterproto.Message):
    market: str = betterproto.string_field(1)
    unsettled: List["UnsettledAccount"] = betterproto.message_field(2)


@dataclass
class GetOrderbooksStreamResponse(betterproto.Message):
    slot: int = betterproto.int64_field(1)
    orderbook: "GetOrderbookResponse" = betterproto.message_field(2)


@dataclass
class GetTickersStreamResponse(betterproto.Message):
    slot: int = betterproto.int64_field(1)
    ticker: "GetTickersResponse" = betterproto.message_field(2)


@dataclass
class GetMarketDepthRequest(betterproto.Message):
    market: str = betterproto.string_field(1)
    depth: int = betterproto.int32_field(2)
    step: "Step" = betterproto.enum_field(3)


@dataclass
class GetMarketDepthStreamResponse(betterproto.Message):
    slot: int = betterproto.int64_field(1)
    tick: "MarketDepthTick" = betterproto.message_field(2)


@dataclass
class MarketDepthTick(betterproto.Message):
    prev_slot: int = betterproto.int64_field(1)
    asks: List["OrderbookItem"] = betterproto.message_field(2)
    bids: List["OrderbookItem"] = betterproto.message_field(3)


@dataclass
class GetTradesStreamResponse(betterproto.Message):
    slot: int = betterproto.int64_field(1)
    trades: "GetTradesResponse" = betterproto.message_field(2)


class ApiStub(betterproto.ServiceStub):
    async def get_markets(self) -> GetMarketsResponse:
        request = GetMarketsRequest()

        return await self._unary_unary(
            "/api.Api/GetMarkets",
            request,
            GetMarketsResponse,
        )

    async def get_tickers(self, *, market: str = "") -> GetTickersResponse:
        request = GetTickersRequest()
        request.market = market

        return await self._unary_unary(
            "/api.Api/GetTickers",
            request,
            GetTickersResponse,
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
        request = GetOrderbookRequest()
        request.market = market
        request.limit = limit

        return await self._unary_unary(
            "/api.Api/GetOrderbook",
            request,
            GetOrderbookResponse,
        )

    async def get_trades(
        self, *, market: str = "", limit: int = 0
    ) -> GetTradesResponse:
        request = GetTradesRequest()
        request.market = market
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

    async def get_account_balance(
        self, *, owner_address: str = ""
    ) -> GetAccountBalanceResponse:
        """account endpoints"""

        request = GetAccountBalanceRequest()
        request.owner_address = owner_address

        return await self._unary_unary(
            "/api.Api/GetAccountBalance",
            request,
            GetAccountBalanceResponse,
        )

    async def post_order(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: "Side" = 0,
        type: List["OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
    ) -> PostOrderResponse:
        """trade endpoints"""

        request = PostOrderRequest()
        request.owner_address = owner_address
        request.payer_address = payer_address
        request.market = market
        request.side = side
        request.type = type
        request.amount = amount
        request.price = price
        request.open_orders_address = open_orders_address
        request.client_order_i_d = client_order_i_d

        return await self._unary_unary(
            "/api.Api/PostOrder",
            request,
            PostOrderResponse,
        )

    async def post_submit(
        self, *, transaction: str = "", skip_pre_flight: bool = False
    ) -> PostSubmitResponse:
        request = PostSubmitRequest()
        request.transaction = transaction
        request.skip_pre_flight = skip_pre_flight

        return await self._unary_unary(
            "/api.Api/PostSubmit",
            request,
            PostSubmitResponse,
        )

    async def post_cancel_order(
        self,
        *,
        order_i_d: str = "",
        side: "Side" = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> PostCancelOrderResponse:
        request = PostCancelOrderRequest()
        request.order_i_d = order_i_d
        request.side = side
        request.market_address = market_address
        request.owner_address = owner_address
        request.open_orders_address = open_orders_address

        return await self._unary_unary(
            "/api.Api/PostCancelOrder",
            request,
            PostCancelOrderResponse,
        )

    async def post_cancel_by_client_order_i_d(
        self,
        *,
        client_order_i_d: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> PostCancelOrderResponse:
        request = PostCancelByClientOrderIDRequest()
        request.client_order_i_d = client_order_i_d
        request.market_address = market_address
        request.owner_address = owner_address
        request.open_orders_address = open_orders_address

        return await self._unary_unary(
            "/api.Api/PostCancelByClientOrderID",
            request,
            PostCancelOrderResponse,
        )

    async def post_cancel_all(
        self,
        *,
        market: str = "",
        owner_address: str = "",
        open_orders_addresses: List[str] = [],
    ) -> PostCancelAllResponse:
        request = PostCancelAllRequest()
        request.market = market
        request.owner_address = owner_address
        request.open_orders_addresses = open_orders_addresses

        return await self._unary_unary(
            "/api.Api/PostCancelAll",
            request,
            PostCancelAllResponse,
        )

    async def post_replace_by_client_order_i_d(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: "Side" = 0,
        type: List["OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
    ) -> PostOrderResponse:
        request = PostOrderRequest()
        request.owner_address = owner_address
        request.payer_address = payer_address
        request.market = market
        request.side = side
        request.type = type
        request.amount = amount
        request.price = price
        request.open_orders_address = open_orders_address
        request.client_order_i_d = client_order_i_d

        return await self._unary_unary(
            "/api.Api/PostReplaceByClientOrderID",
            request,
            PostOrderResponse,
        )

    async def post_replace_order(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: "Side" = 0,
        type: List["OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
        order_i_d: str = "",
    ) -> PostOrderResponse:
        request = PostReplaceOrderRequest()
        request.owner_address = owner_address
        request.payer_address = payer_address
        request.market = market
        request.side = side
        request.type = type
        request.amount = amount
        request.price = price
        request.open_orders_address = open_orders_address
        request.client_order_i_d = client_order_i_d
        request.order_i_d = order_i_d

        return await self._unary_unary(
            "/api.Api/PostReplaceOrder",
            request,
            PostOrderResponse,
        )

    async def post_settle(
        self,
        *,
        owner_address: str = "",
        market: str = "",
        base_token_wallet: str = "",
        quote_token_wallet: str = "",
        open_orders_address: str = "",
    ) -> PostSettleResponse:
        request = PostSettleRequest()
        request.owner_address = owner_address
        request.market = market
        request.base_token_wallet = base_token_wallet
        request.quote_token_wallet = quote_token_wallet
        request.open_orders_address = open_orders_address

        return await self._unary_unary(
            "/api.Api/PostSettle",
            request,
            PostSettleResponse,
        )

    async def get_orders(
        self,
        *,
        market: str = "",
        status: "OrderStatus" = 0,
        side: "Side" = 0,
        types: List["OrderType"] = [],
        from_: Optional[datetime] = None,
        limit: int = 0,
        direction: "Direction" = 0,
        address: str = "",
        open_orders_address: str = "",
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
        request.address = address
        request.open_orders_address = open_orders_address

        return await self._unary_unary(
            "/api.Api/GetOrders",
            request,
            GetOrdersResponse,
        )

    async def get_open_orders(
        self,
        *,
        market: str = "",
        limit: int = 0,
        address: str = "",
        open_orders_address: str = "",
    ) -> GetOpenOrdersResponse:
        request = GetOpenOrdersRequest()
        request.market = market
        request.limit = limit
        request.address = address
        request.open_orders_address = open_orders_address

        return await self._unary_unary(
            "/api.Api/GetOpenOrders",
            request,
            GetOpenOrdersResponse,
        )

    async def get_order_by_i_d(
        self, *, order_i_d: str = "", market: str = ""
    ) -> GetOrderByIDResponse:
        request = GetOrderByIDRequest()
        request.order_i_d = order_i_d
        request.market = market

        return await self._unary_unary(
            "/api.Api/GetOrderByID",
            request,
            GetOrderByIDResponse,
        )

    async def get_unsettled(
        self, *, market: str = "", owner: str = ""
    ) -> GetUnsettledResponse:
        request = GetUnsettledRequest()
        request.market = market
        request.owner = owner

        return await self._unary_unary(
            "/api.Api/GetUnsettled",
            request,
            GetUnsettledResponse,
        )

    async def get_orderbooks_stream(
        self, *, markets: List[str] = [], limit: int = 0
    ) -> AsyncGenerator[GetOrderbooksStreamResponse, None]:
        """streaming endpoints"""

        request = GetOrderbooksRequest()
        request.markets = markets
        request.limit = limit

        async for response in self._unary_stream(
            "/api.Api/GetOrderbooksStream",
            request,
            GetOrderbooksStreamResponse,
        ):
            yield response

    async def get_tickers_stream(
        self, *, market: str = ""
    ) -> AsyncGenerator[GetTickersStreamResponse, None]:
        request = GetTickersRequest()
        request.market = market

        async for response in self._unary_stream(
            "/api.Api/GetTickersStream",
            request,
            GetTickersStreamResponse,
        ):
            yield response

    async def get_market_depth_stream(
        self,
    ) -> AsyncGenerator[GetMarketDepthStreamResponse, None]:
        request = GetMarketsRequest()

        async for response in self._unary_stream(
            "/api.Api/GetMarketDepthStream",
            request,
            GetMarketDepthStreamResponse,
        ):
            yield response

    async def get_trades_stream(
        self, *, market: str = "", limit: int = 0
    ) -> AsyncGenerator[GetTradesStreamResponse, None]:
        request = GetTradesRequest()
        request.market = market
        request.limit = limit

        async for response in self._unary_stream(
            "/api.Api/GetTradesStream",
            request,
            GetTradesStreamResponse,
        ):
            yield response

    async def get_order_status_stream(
        self, *, market: str = "", owner_address: str = ""
    ) -> AsyncGenerator[GetOrderStatusStreamResponse, None]:
        request = GetOrderStatusStreamRequest()
        request.market = market
        request.owner_address = owner_address

        async for response in self._unary_stream(
            "/api.Api/GetOrderStatusStream",
            request,
            GetOrderStatusStreamResponse,
        ):
            yield response