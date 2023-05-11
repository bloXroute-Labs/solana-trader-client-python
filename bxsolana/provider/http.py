import datetime
import os
from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING, List, Any

import aiohttp
from bxsolana_trader_proto.common import OrderType

from solders import keypair as kp

from bxsolana_trader_proto import api as proto
from .. import transaction
from . import constants
from .base import Provider
from .http_error import map_response
from bxsolana_trader_proto.common import (
    PerpPositionSide,
    PostOnlyParams,
    PerpOrderType,
    PerpContract,
    PerpCollateralType,
    PerpCollateralToken,
)

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class HttpProvider(Provider):
    _endpoint: str
    _session: aiohttp.ClientSession
    _private_key: Optional[kp.Keypair]

    # noinspection PyMissingConstructor
    def __init__(
            self,
            endpoint: str = constants.MAINNET_API_HTTP,
            auth_header: Optional[str] = None,
            private_key: Optional[str] = None,
    ):
        self._endpoint = f"{endpoint}/api/v1"
        self._endpointV2 = f"{endpoint}/api/v2"

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

    def private_key(self) -> Optional[kp.Keypair]:
        return self._private_key

    async def close(self):
        await self._session.close()

    # Beginning of V2
    async def get_drift_markets(
            self,
            request: proto.GetDriftMarketsRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetDriftMarketsResponse:
        async with self._session.get(
                f"{self._endpointV2}/drift/markets={request.metadata}"
        ) as res:
            return await map_response(res, proto.GetDriftMarketsResponse())

    async def post_drift_enable_margin_trading(
            self,
            request: proto.PostDriftEnableMarginTradingRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostDriftEnableMarginTradingResponse:
        async with self._session.post(
                f"{self._endpointV2}/drift/enable-margin", json=request.to_dict()
        ) as res:
            return await map_response(
                res, proto.PostDriftEnableMarginTradingResponse()
            )

    async def post_drift_margin_order(
            self,
            request: proto.PostDriftMarginOrderRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostDriftMarginOrderResponse:
        request = proto.PostDriftMarginOrderRequest()
        async with self._session.post(
                f"{self._endpointV2}/drift/margin-place", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostDriftMarginOrderResponse())

    async def get_drift_margin_orderbook(
            self,
            request: proto.GetDriftMarginOrderbookRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetDriftMarginOrderbookResponse:
        async with self._session.get(
                f"{self._endpointV2}/drift/margin-orderbooks/{request.market}?limit=/{request.limit}&metadata={request.metadata}"
        ) as res:
            return await map_response(
                res, proto.GetDriftMarginOrderbookResponse()
            )

    # End of V2

    async def get_markets(
            self,
            request: proto.GetMarketsRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None) -> proto.GetMarketsResponse:
        async with self._session.get(f"{self._endpoint}/market/markets") as res:
            return await map_response(res, proto.GetMarketsResponse())

    async def get_quotes(
            self,
            request: proto.GetQuotesRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetQuotesResponse:
        projects_str = serialize_projects(request.projects)
        async with self._session.get(
                f"{self._endpoint}/market/quote?inToken={request.in_token}&outToken={request.out_token}&inAmount={request.in_amount}&slippage={request.slippage}&limit={request.limit}&{projects_str}"
        ) as res:
            return await map_response(res, proto.GetQuotesResponse())

    async def post_route_trade_swap(
            self,
            *,
            request: proto.RouteTradeSwapRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.TradeSwapResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/route-swap", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def get_orderbook(
            self,
            *,
            request: proto.GetOrderbookRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOrderbookResponse:
        async with self._session.get(
                f"{self._endpoint}/market/orderbooks/{request.market}?limit={request.limit}&project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetOrderbookResponse())

    async def get_market_depth(
            self,
            *,
            request: proto.GetMarketDepthRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetMarketDepthResponse:
        async with self._session.get(
                f"{self._endpoint}/market/depth/{request.market}?limit={request.limit}&project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetMarketDepthResponse())

    async def get_tickers(
            self,
            *,
            request: proto.GetTickersRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetTickersResponse:
        async with self._session.get(
                f"{self._endpoint}/market/tickers/{request.market}?project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetTickersResponse())

    async def get_orders(
            self,
            *,
            request: proto.GetOrdersRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOrdersResponse:
        raise NotImplementedError()

    async def get_open_orders(
            self,
            *,
            request: proto.GetOpenOrdersRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOpenOrdersResponse:
        async with self._session.get(
                f"{self._endpoint}/trade/orders/{request.market}"
                f"?address={request.address}"
                f"&openOrdersAddress={request.open_orders_address}"
                f"&side={request.side}"
                "&types=OT_LIMIT"
                f"&direction={request.direction.name}"
                f"&project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetOpenOrdersResponse())

    async def get_order_by_id(
            self,
            *,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOrderByIdResponse:
        # TODO
        raise NotImplementedError()

    async def get_unsettled(
            self,
            *,
            request: proto.GetUnsettledRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetUnsettledResponse:
        async with self._session.get(
                f"{self._endpoint}/trade/unsettled/{request.market}?ownerAddress={request.owner_address}&"
                f"project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetUnsettledResponse())

    async def get_account_balance(
            self,
            *,
            request: proto.GetAccountBalanceRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetAccountBalanceResponse:
        async with self._session.get(
                f"{self._endpoint}/account/balance?ownerAddress={request.owner_address}"
        ) as res:
            return await map_response(res, proto.GetAccountBalanceResponse())

    async def get_token_accounts(
            self,
            *,
            request: proto.GetTokenAccountsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetTokenAccountsResponse:
        async with self._session.get(
                f"{self._endpoint}/account/token-accounts?ownerAddress={request.owner_address}"
        ) as res:
            return await map_response(res, proto.GetTokenAccountsResponse())

    async def get_pools(
            self,
            *,
            request: proto.GetPoolsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetPoolsResponse:
        params = "?" + serialize_projects(request.projects)

        async with self._session.get(
                f"{self._endpoint}/market/pools{params}"
        ) as res:
            return await map_response(res, proto.GetPoolsResponse())

    async def get_price(self,
                        *,
                        request: proto.GetPoolsRequest,
                        timeout: Optional[float] = None,
                        deadline: Optional[proto.Deadline] = None,
                        metadata: Optional[proto.MetadataLike] = None) -> proto.GetPriceResponse:
        params = "?" + serialize_list("tokens", request.tokens)
        async with self._session.get(
                f"{self._endpoint}/market/price{params}"
        ) as res:
            return await map_response(res, proto.GetPriceResponse())

    async def get_recent_block_hash(self,
                                    *,
                                    request: proto.GetRecentBlockHashRequest,
                                    timeout: Optional[float] = None,
                                    deadline: Optional[proto.Deadline] = None,
                                    metadata: Optional[proto.MetadataLike] = None) -> proto.GetRecentBlockHashResponse:
        async with self._session.get(
                f"{self._endpoint}/system/blockhash"
        ) as res:
            return await map_response(res, proto.GetRecentBlockHashResponse())

    async def get_perp_orderbook(
            self,
            *,
            request: proto.GetPerpOrderbookRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetPerpOrderbookResponse:
        async with self._session.get(
                f"{self._endpoint}/market/perp/orderbook/{request.contract}?limit={request.limit}&project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetPerpOrderbookResponse())

    async def post_settle_pnl(
            self,
            *,
            owner_address: str = "",
            settlee_account_address: str = "",
            contract: PerpContract = PerpContract.ALL,
            project: proto.Project = proto.Project.P_DRIFT,
    ) -> proto.PostSettlePnlResponse:
        request = proto.PostSettlePnlRequest()
        request.contract = contract
        request.project = project
        request.owner_address = owner_address
        request.settlee_account_address = settlee_account_address

        async with self._session.post(
                f"{self._endpoint}/trade/perp/settle-pnl", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSettlePnlResponse())

    async def post_settle_pn_ls(
            self,
            *,
            owner_address: str = "",
            settlee_account_addresses: List[str] = [],
            contract: PerpContract = PerpContract.ALL,
            project: proto.Project = proto.Project.P_DRIFT,
    ) -> proto.PostSettlePnLsResponse:
        request = proto.PostSettlePnLsRequest()
        request.contract = contract
        request.project = project
        request.owner_address = owner_address
        request.settlee_account_addresses = settlee_account_addresses

        async with self._session.post(
                    f"{self._endpoint}/trade/perp/settle-pnls", json=request.to_dict()
            ) as res:
                return await map_response(res, proto.PostSettlePnLsResponse())

    async def post_liquidate_perp(
            self,
            *,
            owner_address: str = "",
            settlee_account_address: str = "",
            amount: float = 0,
            contract: PerpContract = PerpContract.ALL,
            project: proto.Project = proto.Project.P_DRIFT,
    ) -> proto.PostLiquidatePerpResponse:
        request = proto.PostLiquidatePerpRequest()
        request.amount = amount
        request.contract = contract
        request.project = project
        request.owner_address = owner_address
        request.settlee_account_address = settlee_account_address

        async with self._session.post(
                f"{self._endpoint}/trade/perp/liquidate", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostLiquidatePerpResponse())

    async def get_assets(
            self,
            *,
            request: proto.GetAssetsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetAssetsResponse:
        async with self._session.get(
                f"{self._endpoint}/trade/perp/assets?ownerAddress={request.owner_address}&accountAddress={request.account_address}"
                f"&project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetAssetsResponse())

    async def get_perp_contracts(
            self,
            *,
            request: proto.GetPerpContractsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetPerpContractsResponse:
        async with self._session.get(
                f"{self._endpoint}/market/perp/contracts?project={request.project.name}"
        ) as res:
            return await map_response(res, proto.GetPerpContractsResponse())

    async def post_perp_order(
            self,
            *,
            request: proto.PostPerpOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostPerpOrderResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/perp/order", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostPerpOrderResponse())

    async def get_open_perp_order(
            self,
            *,
            request: proto.GetOpenPerpOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOpenPerpOrderResponse:
        async with self._session.get(
                f"{self._endpoint}/trade/perp/open-order-by-id?ownerAddress={request.owner_address}&accountAddress={request.account_address}"
                f"&project={request.project.name}&contract={request.contract.name}&clientOrderID={request.client_order_id}&orderID={request.order_id}"
        ) as res:
            return await map_response(res, proto.GetOpenPerpOrderResponse())

    async def get_open_perp_orders(
            self,
            *,
            request: proto.GetOpenPerpOrdersRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetOpenPerpOrdersResponse:
        params = ""
        for i in range(len(request.contracts)):
            params += "&contracts=" + str(request.contracts[i].name)

        async with self._session.get(
                f"{self._endpoint}/trade/perp/open-orders?ownerAddress={request.owner_address}&accountAddress={request.account_address}"
                f"&project={request.project.name}{params}"
        ) as res:
            return await map_response(res, proto.GetOpenPerpOrdersResponse())

    async def post_cancel_perp_order(
            self,
            *,
            request: proto.PostCancelPerpOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostCancelPerpOrderResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/perp/cancelbyid", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelPerpOrderResponse())

    async def post_cancel_perp_orders(
            self,
            *,
            request: proto.PostCancelPerpOrdersRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostCancelPerpOrdersResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/perp/cancel", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelPerpOrdersResponse())

    async def post_close_perp_positions(
            self,
            *,
            request: proto.PostClosePerpPositionsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostClosePerpPositionsResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/perp/close", json=request.to_dict()
        ) as res:
            return await map_response(
                res, proto.PostClosePerpPositionsResponse()
            )

    async def post_create_user(
            self,
            *,
            request: proto.PostCreateUserRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostCreateUserResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/user", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCreateUserResponse())

    async def get_user(
            self,
            *,
            request: proto.GetUserRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetUserResponse:
        async with self._session.get(
                f"{self._endpoint}/trade/user?ownerAddress={request.owner_address}&project={request.project.name}&accountAddress={request.account_address}"
        ) as res:
            return await map_response(res, proto.GetUserResponse())

    async def post_manage_collateral(
            self,
            *,
            request: proto.PostManageCollateralRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostManageCollateralResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/perp/managecollateral",
                json=request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostManageCollateralResponse())

    async def get_perp_positions(
            self,
            *,
            request: proto.GetPerpPositionsRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.GetPerpPositionsResponse:
        params = ""
        for i in range(len(request.contracts)):
            params += "&contracts=" + str(request.contracts[i].name)

        async with self._session.get(
                f"{self._endpoint}/trade/perp/positions?ownerAddress={request.owner_address}"
                f"&accountAddress={request.account_address}"
                f"&project={request.project.name}{params}"
        ) as res:
            return await map_response(res, proto.GetPerpPositionsResponse())

    async def post_trade_swap(
            self,
            *,
            request: proto.TradeSwapRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.TradeSwapResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/swap", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def post_order(
            self,
            *,
            request: proto.PostOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostOrderResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/place", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_cancel_order(
            self,
            *,
            request: proto.PostCancelOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional[proto.Deadline] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostCancelOrderResponse:
        async with self._session.post(
                f"{self._endpoint}/trade/cancel", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_by_client_order_id(
            self,
            *,
            client_order_i_d: int = 0,
            market_address: str = "",
            owner_address: str = "",
            open_orders_address: str = "",
            project: proto.Project = proto.Project.P_UNKNOWN,
    ) -> proto.PostCancelOrderResponse:
        request = proto.PostCancelByClientOrderIdRequest(
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
            request: proto.PostSubmitRequest,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostSubmitResponse:
        if transaction is None:
            raise ValueError("transaction cannot be omitted")

        request = proto.PostSubmitRequest(request.transaction, request.skip_pre_flight)
        async with self._session.post(
                f"{self._endpoint}/trade/submit", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

    async def post_submit_batch(
            self,
            *,
            request: proto.PostSubmitBatchRequest,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostSubmitBatchResponse:
        request = proto.PostSubmitBatchRequest(request.entries, request.submit_strategy)
        async with self._session.post(
                f"{self._endpoint}/trade/submit-batch", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitBatchResponse())

    async def post_replace_by_client_order_id(
            self,
            request: proto.PostOrderRequest,
            *,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostOrderResponse:

        async with self._session.post(
                f"{self._endpoint}/trade/replacebyclientid", json=request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_replace_order(
            self,
            *,
            request: proto.PostReplaceOrderRequest,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional[proto.MetadataLike] = None
    ) -> proto.PostOrderResponse:
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


def serialize_list(key: str, values: List[Any]) -> str:
    parts = []
    for i, v in enumerate(values):
        parts.append(f"{key}={v}")
        if i != len(values) - 1:
            parts.append("&")
    return "".join(parts)


def serialize_projects(projects: List[proto.Project]) -> str:
    return serialize_list("projects", [project.name for project in projects])


def http() -> Provider:
    return HttpProvider()


def http_testnet() -> Provider:
    return HttpProvider(endpoint=constants.TESTNET_API_HTTP)


def http_devnet() -> Provider:
    return HttpProvider(endpoint=constants.DEVNET_API_HTTP)


def http_local() -> Provider:
    return HttpProvider(endpoint=constants.LOCAL_API_HTTP)
