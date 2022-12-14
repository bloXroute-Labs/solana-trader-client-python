import datetime
import os
from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING, List

import aiohttp
from solana import keypair

from bxsolana_trader_proto import api as proto
from .. import transaction
from . import constants
from .base import Provider
from .http_error import map_response

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class HttpProvider(Provider):
    _endpoint: str
    _session: aiohttp.ClientSession
    _private_key: Optional[keypair.Keypair]

    # noinspection PyMissingConstructor
    def __init__(
        self,
        endpoint: str = constants.MAINNET_API_HTTP,
        auth_header: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self._endpoint = f"{endpoint}/api/v1"

        if auth_header is None:
            auth_header = os.environ["AUTH_HEADER"]

        self._session = aiohttp.ClientSession()
        self._session.headers["authorization"] = auth_header

        if private_key is None:
            try:
                self._private_key = transaction.load_private_key_from_env()
            except EnvironmentError:
                self._private_key = None
        else:
            self._private_key = transaction.load_private_key(private_key)

    async def connect(self):
        pass

    def private_key(self) -> Optional[keypair.Keypair]:
        return self._private_key

    async def close(self):
        await self._session.close()

    async def get_markets(self) -> proto.GetMarketsResponse:
        async with self._session.get(f"{self._endpoint}/market/markets") as res:
            return await map_response(res, proto.GetMarketsResponse())

    async def get_quotes(
        self,
        *,
        in_token: str = "",
        out_token: str = "",
        in_amount: float = 0,
        slippage: float = 0,
        limit: int = 10,
        projects: List[proto.Project] = [],
    ) -> proto.GetQuotesResponse:
        projects_str = (
            "projects=&".join(str(project.value) for project in projects)
            if len(projects) > 0
            else ""
        )
        async with self._session.get(
            f"{self._endpoint}/market/quote?inToken={in_token}&outToken={out_token}&inAmount={in_amount}&slippage={slippage}&limit={limit}&projects={projects_str}"
        ) as res:
            return await map_response(res, proto.GetQuotesResponse())

    async def post_route_trade_swap(
        self,
        *,
        project: proto.Project = proto.Project.P_RAYDIUM,
        owner_address: str = "",
        steps: List["proto.RouteStep"] = [],
    ) -> proto.TradeSwapResponse:
        request = proto.RouteTradeSwapRequest()
        request.project = project
        request.owner_address = owner_address
        if steps is not None:
            request.steps = steps

        async with self._session.post(
            f"{self._endpoint}/trade/route-swap", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def get_orderbook(
        self,
        *,
        market: str = "",
        limit: int = 0,
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint}/market/orderbooks/{market}?limit={limit}&project={project.name}"
        ) as res:
            return await map_response(res, proto.GetOrderbookResponse())

    async def get_tickers(
        self,
        *,
        market: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetTickersResponse:
        async with self._session.get(
            f"{self._endpoint}/market/tickers/{market}?project={project.name}"
        ) as res:
            return await map_response(res, proto.GetTickersResponse())

    async def get_orders(
        self,
        *,
        market: str = "",
        status: proto.OrderStatus = proto.OrderStatus.OS_UNKNOWN,
        side: proto.Side = proto.Side.S_UNKNOWN,
        types: List[proto.OrderType] = [],
        from_: Optional[datetime.datetime] = None,
        limit: int = 0,
        direction: proto.Direction = proto.Direction.D_ASCENDING,
        address: str = "",
        open_orders_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetOrdersResponse:
        raise NotImplementedError()

    async def get_open_orders(
        self,
        *,
        market: str = "",
        side: proto.Side = proto.Side.S_UNKNOWN,
        types: List[proto.OrderType] = [],
        from_: Optional[datetime.datetime] = None,
        limit: int = 0,
        direction: proto.Direction = proto.Direction.D_ASCENDING,
        address: str = "",
        open_orders_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetOpenOrdersResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/orders/{market}"
            f"?address={address}"
            f"&openOrdersAddress={open_orders_address}"
            f"&side={side}"
            "&types=OT_LIMIT"
            f"&direction={direction.name}"
            f"&project={project.name}"
        ) as res:
            return await map_response(res, proto.GetOpenOrdersResponse())

    async def get_order_by_i_d(
        self,
        *,
        order_i_d: str = "",
        market: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetOrderByIDResponse:
        # TODO
        raise NotImplementedError()

    async def get_unsettled(
        self,
        *,
        market: str = "",
        owner_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.GetUnsettledResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/unsettled/{market}?ownerAddress={owner_address}&project={project.name}"
        ) as res:
            return await map_response(res, proto.GetUnsettledResponse())

    async def get_account_balance(
        self, owner_address: str = ""
    ) -> proto.GetAccountBalanceResponse:
        async with self._session.get(
            f"{self._endpoint}/account/balance?ownerAddress={owner_address}"
        ) as res:
            return await map_response(res, proto.GetAccountBalanceResponse())

    async def get_pools(
        self, projects: List["proto.Project"] = []
    ) -> proto.GetPoolsResponse:
        params = (
            "?" + "projects=&".join(str(project.value) for project in projects)
            if len(projects) > 0
            else ""
        )
        async with self._session.get(
            f"{self._endpoint}/market/pools{params}"
        ) as res:
            return await map_response(res, proto.GetPoolsResponse())

    async def get_price(self, tokens: List[str] = []) -> proto.GetPriceResponse:
        params = "?" + "tokens=&".join(tokens) if len(tokens) > 0 else ""
        async with self._session.get(
            f"{self._endpoint}/market/price{params}"
        ) as res:
            return await map_response(res, proto.GetPriceResponse())

    async def get_recent_block_hash(self) -> proto.GetRecentBlockHashResponse:
        async with self._session.get(
            f"{self._endpoint}/system/blockhash"
        ) as res:
            return await map_response(res, proto.GetRecentBlockHashResponse())

    async def post_trade_swap(
        self,
        project: proto.Project = proto.Project.P_ALL,
        owner_address: str = "",
        in_token: str = "",
        out_token: str = "",
        in_amount: float = 0,
        slippage: float = 0,
    ) -> proto.TradeSwapResponse:
        request = proto.TradeSwapRequest(
            project,
            owner_address,
            in_token,
            out_token,
            in_amount,
            slippage,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/swap", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def post_order(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: proto.Side = proto.Side.S_UNKNOWN,
        type: List["proto.OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
        project: proto.Project = proto.Project.P_UNKNOWN,
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
            project,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/place", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_cancel_order(
        self,
        *,
        order_i_d: str = "",
        side: proto.Side = proto.Side.S_UNKNOWN,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostCancelOrderResponse:
        request = proto.PostCancelOrderRequest(
            order_i_d,
            side,
            market_address,
            owner_address,
            open_orders_address,
            project,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/cancel", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_by_client_order_i_d(
        self,
        *,
        client_order_i_d: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostCancelOrderResponse:
        request = proto.PostCancelByClientOrderIDRequest(
            client_order_i_d,
            market_address,
            owner_address,
            open_orders_address,
            project,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/cancelbyid", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_all(
        self,
        *,
        market: str = "",
        owner_address: str = "",
        open_orders_addresses: List[str] = [],
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostCancelAllResponse:
        request = proto.PostCancelAllRequest(
            market, owner_address, open_orders_addresses, project
        )
        async with self._session.post(
            f"{self._endpoint}/trade/cancelall", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelAllResponse())

    async def post_settle(
        self,
        *,
        owner_address: str = "",
        market: str = "",
        base_token_wallet: str = "",
        quote_token_wallet: str = "",
        open_orders_address: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostSettleResponse:
        request = proto.PostSettleRequest(
            owner_address,
            market,
            base_token_wallet,
            quote_token_wallet,
            open_orders_address,
            project,
        )
        async with self._session.post(
            f"{self._endpoint}/trade/settle", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSettleResponse())

    async def post_submit(
        self,
        *,
        transaction: Optional[proto.TransactionMessage] = None,
        skip_pre_flight: bool = False,
    ) -> proto.PostSubmitResponse:
        if transaction is None:
            raise ValueError("transaction cannot be omitted")

        request = proto.PostSubmitRequest(transaction, skip_pre_flight)
        async with self._session.post(
            f"{self._endpoint}/trade/submit", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

    async def post_replace_by_client_order_i_d(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: proto.Side = proto.Side.S_UNKNOWN,
        type: List["proto.OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
        project: proto.Project = proto.Project.P_UNKNOWN,
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
            project,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/replacebyclientid", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_replace_order(
        self,
        *,
        owner_address: str = "",
        payer_address: str = "",
        market: str = "",
        side: "proto.Side" = proto.Side.S_UNKNOWN,
        type: List["proto.OrderType"] = [],
        amount: float = 0,
        price: float = 0,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
        order_i_d: str = "",
        project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostOrderResponse:
        request = proto.PostReplaceOrderRequest(
            owner_address,
            payer_address,
            market,
            side,
            type,
            amount,
            price,
            open_orders_address,
            client_order_i_d,
            order_i_d,
            project,
        )

        async with self._session.post(
            f"{self._endpoint}/trade/replace", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def _unary_stream(
        self,
        route: str,
        # pyre-ignore[11]: type is too hard to find
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> AsyncGenerator["T", None]:
        raise NotImplementedError(
            "streaming is not implemented in HTTP provider"
        )

        # useless line to turn function into a generator
        yield response_type()


def http() -> Provider:
    return HttpProvider()


def http_testnet() -> Provider:
    return HttpProvider(endpoint=constants.TESTNET_API_HTTP)


def http_devnet() -> Provider:
    return HttpProvider(endpoint=constants.DEVNET_API_HTTP)


def http_local() -> Provider:
    return HttpProvider(endpoint=constants.LOCAL_API_HTTP)
