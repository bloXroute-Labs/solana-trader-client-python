import os
from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING, List, Any

import aiohttp

from solders import keypair as kp

from bxsolana_trader_proto import api as proto
from grpclib.metadata import Deadline
from grpclib.metadata import _MetadataLike as MetadataLike
from .. import transaction
from . import constants
from .base import Provider
from .http_error import map_response

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import T


class HttpProvider(Provider):
    _endpoint: str
    _endpoint_v2: str
    _session: aiohttp.ClientSession
    _private_key: Optional[kp.Keypair]

    # noinspection PyMissingConstructor
    def __init__(
        self,
        endpoint: str = constants.MAINNET_API_NY_HTTP,
        auth_header: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self._endpoint = f"{endpoint}/api/v1"
        self._endpoint_v2 = f"{endpoint}/api/v2"

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

    async def get_raydium_pools(
        self,
        get_raydium_pools_request: proto.GetRaydiumPoolsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumPoolsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/pools"
            f"?pairOrAddress={get_raydium_pools_request.pair_or_address}"
        ) as res:
            return await map_response(res, proto.GetRaydiumPoolsResponse())

    async def get_raydium_quotes(
        self,
        get_raydium_quotes_request: proto.GetRaydiumQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/quotes?inToken={get_raydium_quotes_request.in_token}&"
            f"outToken={get_raydium_quotes_request.out_token}&inAmount={get_raydium_quotes_request.in_amount}&"
            f"slippage={get_raydium_quotes_request.slippage}"
        ) as res:
            return await map_response(res, proto.GetRaydiumQuotesResponse())

    async def get_jupiter_quotes(
        self,
        get_jupiter_quotes_request: proto.GetJupiterQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetJupiterQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/jupiter/quotes?inToken={get_jupiter_quotes_request.in_token}&"
            f"outToken={get_jupiter_quotes_request.out_token}&inAmount={get_jupiter_quotes_request.in_amount}&"
            f"slippage={get_jupiter_quotes_request.slippage}&limit={get_jupiter_quotes_request.limit}"
        ) as res:
            return await map_response(res, proto.GetJupiterQuotesResponse())

    async def get_raydium_prices(
        self,
        get_raydium_prices_request: proto.GetRaydiumPricesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumPricesResponse:
        params = "?" + serialize_list(
            "tokens", get_raydium_prices_request.tokens
        )
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/prices{params}"
        ) as res:
            return await map_response(res, proto.GetRaydiumPricesResponse())

    async def get_jupiter_prices(
        self,
        get_jupiter_prices_request: proto.GetJupiterPricesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetJupiterPricesResponse:
        params = "?" + serialize_list(
            "tokens", get_jupiter_prices_request.tokens
        )
        async with self._session.get(
            f"{self._endpoint_v2}/jupiter/prices{params}"
        ) as res:
            return await map_response(res, proto.GetJupiterPricesResponse())

    async def post_jupiter_swap(
        self,
        post_jupiter_swap_request: proto.PostJupiterSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostJupiterSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/jupiter/swap",
            json=post_jupiter_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostJupiterSwapResponse())

    async def post_raydium_swap(
        self,
        post_raydium_swap_request: proto.PostRaydiumSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/swap",
            json=post_raydium_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumSwapResponse())

    async def post_jupiter_route_swap(
        self,
        post_jupiter_route_swap_request: proto.PostJupiterRouteSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostJupiterRouteSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/jupiter/route-swap",
            json=post_jupiter_route_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostJupiterRouteSwapResponse())

    async def post_raydium_route_swap(
        self,
        post_raydium_route_swap_request: proto.PostRaydiumRouteSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumRouteSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/route-swap",
            json=post_raydium_route_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumRouteSwapResponse())

    # Beginning of Drift V2
    async def post_close_drift_perp_positions(
        self,
        post_close_drift_perp_positions_request: proto.PostCloseDriftPerpPositionsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCloseDriftPerpPositionsResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/close",
            json=post_close_drift_perp_positions_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostCloseDriftPerpPositionsResponse()
            )

    async def post_create_drift_user(
        self,
        post_create_drift_user_request: proto.PostCreateDriftUserRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCreateDriftUserResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/user",
            json=post_create_drift_user_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostCreateDriftUserResponse())

    async def post_drift_manage_collateral(
        self,
        post_drift_manage_collateral_request: proto.PostDriftManageCollateralRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftManageCollateralResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/manage-collateral",
            json=post_drift_manage_collateral_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostDriftManageCollateralResponse()
            )

    async def post_drift_settle_pnl(
        self,
        post_drift_settle_pnl_request: proto.PostDriftSettlePnlRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftSettlePnlResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/settle-pnl",
            json=post_drift_settle_pnl_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostDriftSettlePnlResponse())

    async def post_drift_settle_pn_ls(
        self,
        post_drift_settle_pn_ls_request: proto.PostDriftSettlePnLsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftSettlePnLsResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/settle-pnls",
            json=post_drift_settle_pn_ls_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostDriftSettlePnLsResponse())

    async def post_liquidate_drift_perp(
        self,
        post_liquidate_drift_perp_request: proto.PostLiquidateDriftPerpRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostLiquidateDriftPerpResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/liquidate",
            json=post_liquidate_drift_perp_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostLiquidateDriftPerpResponse()
            )

    async def get_drift_perp_orderbook(
        self,
        get_drift_perp_orderbook_request: proto.GetDriftPerpOrderbookRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftPerpOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/orderbook/{get_drift_perp_orderbook_request.contract}"
            f"?limit={get_drift_perp_orderbook_request.limit}"
        ) as res:
            return await map_response(
                res, proto.GetDriftPerpOrderbookResponse()
            )

    async def get_drift_user(
        self,
        get_drift_user_request: proto.GetDriftUserRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftUserResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/user?ownerAddress={get_drift_user_request.owner_address}"
            f"&accountAddress={get_drift_user_request.account_address}"
        ) as res:
            return await map_response(res, proto.GetDriftUserResponse())

    async def get_drift_assets(
        self,
        get_drift_assets_request: proto.GetDriftAssetsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftAssetsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/assets?ownerAddress={get_drift_assets_request.owner_address}"
            f"&accountAddress={get_drift_assets_request.account_address}"
        ) as res:
            return await map_response(res, proto.GetDriftAssetsResponse())

    async def get_drift_perp_contracts(
        self,
        get_drift_perp_contracts_request: proto.GetDriftPerpContractsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftPerpContractsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/contracts"
        ) as res:
            return await map_response(
                res, proto.GetDriftPerpContractsResponse()
            )

    async def get_drift_open_perp_order(
        self,
        get_drift_open_perp_order_request: proto.GetDriftOpenPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftOpenPerpOrderResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/open-order?ownerAddress={get_drift_open_perp_order_request.owner_address}"
            f"&accountAddress={get_drift_open_perp_order_request.account_address}"
            f"&clientOrderID={get_drift_open_perp_order_request.client_order_id}"
            f"&orderID={get_drift_open_perp_order_request.order_id}"
        ) as res:
            return await map_response(
                res, proto.GetDriftOpenPerpOrderResponse()
            )

    async def get_drift_open_margin_order(
        self,
        get_drift_open_margin_order_request: proto.GetDriftOpenMarginOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftOpenMarginOrderResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/margin/open-order?ownerAddress={get_drift_open_margin_order_request.owner_address}"
            f"&accountAddress={get_drift_open_margin_order_request.account_address}"
            f"&clientOrderID={get_drift_open_margin_order_request.client_order_id}"
            f"&orderID={get_drift_open_margin_order_request.order_id}"
        ) as res:
            return await map_response(
                res, proto.GetDriftOpenMarginOrderResponse()
            )

    async def get_drift_perp_positions(
        self,
        get_drift_perp_positions_request: proto.GetDriftPerpPositionsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftPerpPositionsResponse:
        params = ""
        for i in range(len(get_drift_perp_positions_request.contracts)):
            params += "&contracts=" + str(
                get_drift_perp_positions_request.contracts[i]
            )

        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/positions?ownerAddress={get_drift_perp_positions_request.owner_address}"
            f"&accountAddress={get_drift_perp_positions_request.account_address}{params}"
        ) as res:
            return await map_response(
                res, proto.GetDriftOpenPerpOrdersResponse()
            )

    async def get_drift_open_perp_orders(
        self,
        get_drift_open_perp_orders_request: proto.GetDriftOpenPerpOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftOpenPerpOrdersResponse:
        params = ""
        for i in range(len(get_drift_open_perp_orders_request.contracts)):
            params += "&contracts=" + str(
                get_drift_open_perp_orders_request.contracts[i]
            )

        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/open-orders?ownerAddress={get_drift_open_perp_orders_request.owner_address}"
            f"&accountAddress={get_drift_open_perp_orders_request.account_address}{params}"
        ) as res:
            return await map_response(
                res, proto.GetDriftOpenPerpOrdersResponse()
            )

    async def post_drift_cancel_perp_order(
        self,
        post_drift_cancel_perp_order_request: proto.PostDriftCancelPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftCancelPerpOrderResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/cancel",
            json=post_drift_cancel_perp_order_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostCancelDriftMarginOrderResponse()
            )

    async def post_cancel_drift_margin_order(
        self,
        post_cancel_drift_margin_order_request: proto.PostCancelDriftMarginOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelDriftMarginOrderResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/margin/cancel",
            json=post_cancel_drift_margin_order_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostCancelDriftMarginOrderResponse()
            )

    async def get_drift_open_margin_orders(
        self,
        get_drift_open_margin_orders_request: proto.GetDriftOpenMarginOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftOpenMarginOrdersResponse:
        params = ""
        for i in range(len(get_drift_open_margin_orders_request.markets)):
            params += "&markets=" + str(
                get_drift_open_margin_orders_request.markets[i]
            )

        async with self._session.get(
            f"{self._endpoint_v2}/drift/margin/open-orders?ownerAddress={get_drift_open_margin_orders_request.owner_address}"
            f"&accountAddress={get_drift_open_margin_orders_request.account_address}{params}"
        ) as res:
            return await map_response(
                res, proto.GetDriftOpenMarginOrdersResponse()
            )

    async def post_modify_drift_order(
        self,
        post_modify_drift_order_request: proto.PostModifyDriftOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostModifyDriftOrderResponse:
        request_dict = post_modify_drift_order_request.to_dict()
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")
        async with self._session.post(
            f"{self._endpoint_v2}/drift/modify-order",
            json=request_dict,
        ) as res:
            return await map_response(res, proto.PostModifyDriftOrderResponse())

    async def get_drift_markets(
        self,
        get_drift_markets_request: proto.GetDriftMarketsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftMarketsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/markets?metadata={get_drift_markets_request.metadata}"
        ) as res:
            return await map_response(res, proto.GetDriftMarketsResponse())

    async def post_drift_enable_margin_trading(
        self,
        post_drift_enable_margin_trading_request: proto.PostDriftEnableMarginTradingRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftEnableMarginTradingResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/drift/margin-enable",
            json=post_drift_enable_margin_trading_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostDriftEnableMarginTradingResponse()
            )

    async def post_drift_margin_order(
        self,
        post_drift_margin_order_request: proto.PostDriftMarginOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftMarginOrderResponse:
        request_dict = post_drift_margin_order_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")

        async with self._session.post(
            f"{self._endpoint_v2}/drift/margin/place", json=request_dict
        ) as res:
            return await map_response(res, proto.PostDriftMarginOrderResponse())

    async def get_drift_margin_orderbook(
        self,
        get_drift_margin_orderbook_request: proto.GetDriftMarginOrderbookRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftMarginOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/margin/orderbooks/{get_drift_margin_orderbook_request.market}?"
            f"limit={get_drift_margin_orderbook_request.limit}&metadata={get_drift_margin_orderbook_request.metadata}"
        ) as res:
            return await map_response(
                res, proto.GetDriftMarginOrderbookResponse()
            )

    async def get_drift_market_depth(
        self,
        get_drift_market_depth_request: proto.GetDriftMarketDepthRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetDriftMarketDepthResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/drift/perp/market-depth/{get_drift_market_depth_request.contract}?"
            f"limit={get_drift_market_depth_request.limit}"
        ) as res:
            return await map_response(res, proto.GetDriftMarketDepthResponse())

    # Openbook V2

    async def get_markets_v2(
        self,
        get_markets_request_v2: proto.GetMarketsRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetMarketsResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/markets"
        ) as res:
            return await map_response(res, proto.GetMarketsResponseV2())

    async def get_orderbook_v2(
        self,
        get_orderbook_request_v2: proto.GetOrderbookRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOrderbookResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/orderbooks/{get_orderbook_request_v2.market}?"
            f"limit={get_orderbook_request_v2.limit}"
        ) as res:
            return await map_response(res, proto.GetOrderbookResponseV2())

    async def get_market_depth_v2(
        self,
        get_market_depth_request_v2: proto.GetMarketDepthRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetMarketDepthResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/depth/{get_market_depth_request_v2.market}?limit={get_market_depth_request_v2.limit}"
        ) as res:
            return await map_response(res, proto.GetMarketDepthResponseV2())

    async def get_tickers_v2(
        self,
        get_tickers_request_v2: proto.GetTickersRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetTickersResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/tickers/{get_tickers_request_v2.market}"
        ) as res:
            return await map_response(res, proto.GetTickersResponseV2())

    async def get_open_orders_v2(
        self,
        get_open_orders_request_v2: proto.GetOpenOrdersRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOpenOrdersResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/open-orders/{get_open_orders_request_v2.market}"
            f"?address={get_open_orders_request_v2.address}"
            f"&openOrdersAddress={get_open_orders_request_v2.open_orders_address}"
            f"&orderID={get_open_orders_request_v2.order_id}"
            f"&clientOrderID={get_open_orders_request_v2.client_order_id}"
        ) as res:
            return await map_response(res, proto.GetOpenOrdersResponseV2())

    async def get_unsettled_v2(
        self,
        get_unsettled_request_v2: proto.GetUnsettledRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetUnsettledResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/openbook/unsettled/{get_unsettled_request_v2.market}?"
            f"ownerAddress={get_unsettled_request_v2.owner_address}&"
        ) as res:
            return await map_response(res, proto.GetUnsettledResponse())

    async def post_order_v2(
        self,
        post_order_request_v2: proto.PostOrderRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostOrderResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/openbook/place",
            json=post_order_request_v2.to_dict(),
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_cancel_order_v2(
        self,
        post_cancel_order_request_v2: proto.PostCancelOrderRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelOrderResponseV2:
        request_dict = post_cancel_order_request_v2.to_dict()
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")
        async with self._session.post(
            f"{self._endpoint_v2}/openbook/cancel",
            json=request_dict,
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponseV2())

    async def post_settle_v2(
        self,
        post_settle_request_v2: proto.PostSettleRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSettleResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/openbook/settle",
            json=post_settle_request_v2.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSettleResponse())

    async def post_replace_order_v2(
        self,
        post_replace_order_request_v2: proto.PostReplaceOrderRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostOrderResponse:
        request_dict = post_replace_order_request_v2.to_dict()
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")

        async with self._session.post(
            f"{self._endpoint_v2}/openbook/replace",
            json=request_dict,
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    # End of Openbook V2

    # End of V2

    async def get_markets(
        self,
        get_markets_request: proto.GetMarketsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetMarketsResponse:
        async with self._session.get(f"{self._endpoint}/market/markets") as res:
            return await map_response(res, proto.GetMarketsResponse())

    async def get_quotes(
        self,
        get_quotes_request: proto.GetQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetQuotesResponse:
        projects_str = serialize_projects(get_quotes_request.projects)
        async with self._session.get(
            f"{self._endpoint}/market/quote?inToken={get_quotes_request.in_token}&"
            f"outToken={get_quotes_request.out_token}&inAmount={get_quotes_request.in_amount}&"
            f"slippage={get_quotes_request.slippage}&limit={get_quotes_request.limit}&{projects_str}"
        ) as res:
            return await map_response(res, proto.GetQuotesResponse())

    async def post_route_trade_swap(
        self,
        route_trade_swap_request: proto.RouteTradeSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.TradeSwapResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/route-swap",
            json=route_trade_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def get_orderbook(
        self,
        get_orderbook_request: proto.GetOrderbookRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint}/market/orderbooks/{get_orderbook_request.market}?"
            f"limit={get_orderbook_request.limit}&project={get_orderbook_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetOrderbookResponse())

    async def get_market_depth(
        self,
        get_market_depth_request: proto.GetMarketDepthRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetMarketDepthResponse:
        async with self._session.get(
            f"{self._endpoint}/market/depth/{get_market_depth_request.market}?limit={get_market_depth_request.limit}"
            f"&project={get_market_depth_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetMarketDepthResponse())

    async def get_tickers(
        self,
        get_tickers_request: proto.GetTickersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetTickersResponse:
        async with self._session.get(
            f"{self._endpoint}/market/tickers/{get_tickers_request.market}?project={get_tickers_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetTickersResponse())

    async def get_orders(
        self,
        get_orders_request: proto.GetOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOrdersResponse:
        raise NotImplementedError()

    async def get_open_orders(
        self,
        get_open_orders_request: proto.GetOpenOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOpenOrdersResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/orders/{get_open_orders_request.market}"
            f"?address={get_open_orders_request.address}"
            f"&openOrdersAddress={get_open_orders_request.open_orders_address}"
            "&types=OT_LIMIT"
            f"&project={get_open_orders_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetOpenOrdersResponse())

    async def get_order_by_id(
        self,
        get_order_by_id_request: proto.GetOrderByIdRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOrderByIdResponse:
        # TODO
        raise NotImplementedError()

    async def get_unsettled(
        self,
        get_unsettled_request: proto.GetUnsettledRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetUnsettledResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/unsettled/{get_unsettled_request.market}?"
            f"ownerAddress={get_unsettled_request.owner_address}&"
            f"project={get_unsettled_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetUnsettledResponse())

    async def get_account_balance(
        self,
        get_account_balance_request: proto.GetAccountBalanceRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetAccountBalanceResponse:
        async with self._session.get(
            f"{self._endpoint}/account/balance?ownerAddress={get_account_balance_request.owner_address}"
        ) as res:
            return await map_response(res, proto.GetAccountBalanceResponse())

    async def get_token_accounts(
        self,
        get_token_accounts_request: proto.GetTokenAccountsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetTokenAccountsResponse:
        async with self._session.get(
            f"{self._endpoint}/account/token-accounts?ownerAddress={get_token_accounts_request.owner_address}"
        ) as res:
            return await map_response(res, proto.GetTokenAccountsResponse())

    async def get_pools(
        self,
        get_pools_request: proto.GetPoolsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPoolsResponse:
        params = "?" + serialize_projects(get_pools_request.projects)

        async with self._session.get(
            f"{self._endpoint}/market/pools{params}"
        ) as res:
            return await map_response(res, proto.GetPoolsResponse())

    async def get_price(
        self,
        get_price_request: proto.GetPriceRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPriceResponse:
        params = "?" + serialize_list("tokens", get_price_request.tokens)
        async with self._session.get(
            f"{self._endpoint}/market/price{params}"
        ) as res:
            return await map_response(res, proto.GetPriceResponse())

    async def get_recent_block_hash(
        self,
        get_recent_block_hash_request: proto.GetRecentBlockHashRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRecentBlockHashResponse:
        async with self._session.get(
            f"{self._endpoint}/system/blockhash"
        ) as res:
            return await map_response(res, proto.GetRecentBlockHashResponse())

    async def get_perp_orderbook(
        self,
        get_perp_orderbook_request: proto.GetPerpOrderbookRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPerpOrderbookResponse:
        async with self._session.get(
            f"{self._endpoint}/market/perp/orderbook/{get_perp_orderbook_request.contract}?"
            f"limit={get_perp_orderbook_request.limit}&project={get_perp_orderbook_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetPerpOrderbookResponse())

    async def post_settle_pnl(
        self,
        post_settle_pnl_request: proto.PostSettlePnlRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSettlePnlResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/settle-pnl",
            json=post_settle_pnl_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSettlePnlResponse())

    async def post_settle_pn_ls(
        self,
        post_settle_pn_ls_request: proto.PostSettlePnLsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSettlePnLsResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/settle-pnls",
            json=post_settle_pn_ls_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSettlePnLsResponse())

    async def post_liquidate_perp(
        self,
        post_liquidate_perp_request: proto.PostLiquidatePerpRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostLiquidatePerpResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/liquidate",
            json=post_liquidate_perp_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostLiquidatePerpResponse())

    async def get_assets(
        self,
        get_assets_request: proto.GetAssetsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetAssetsResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/perp/assets?ownerAddress={get_assets_request.owner_address}&"
            f"accountAddress={get_assets_request.account_address}"
            f"&project={get_assets_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetAssetsResponse())

    async def get_perp_contracts(
        self,
        get_perp_contracts_request: proto.GetPerpContractsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPerpContractsResponse:
        async with self._session.get(
            f"{self._endpoint}/market/perp/contracts?project={get_perp_contracts_request.project.name}"
        ) as res:
            return await map_response(res, proto.GetPerpContractsResponse())

    async def post_perp_order(
        self,
        post_perp_order_request: proto.PostPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostPerpOrderResponse:
        request_dict = post_perp_order_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")

        async with self._session.post(
            f"{self._endpoint}/trade/perp/order", json=request_dict
        ) as res:
            return await map_response(res, proto.PostPerpOrderResponse())

    async def post_drift_perp_order(
        self,
        post_drift_perp_order_request: proto.PostDriftPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostDriftPerpOrderResponse:
        request_dict = post_drift_perp_order_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")

        async with self._session.post(
            f"{self._endpoint_v2}/drift/perp/place", json=request_dict
        ) as res:
            return await map_response(res, proto.PostDriftPerpOrderResponse())

    async def get_open_perp_order(
        self,
        get_open_perp_order_request: proto.GetOpenPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOpenPerpOrderResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/perp/open-order-by-id?ownerAddress={get_open_perp_order_request.owner_address}"
            f"&accountAddress={get_open_perp_order_request.account_address}"
            f"&project={get_open_perp_order_request.project.name}"
            f"&clientOrderID={get_open_perp_order_request.client_order_id}&orderID={get_open_perp_order_request.order_id}"
        ) as res:
            return await map_response(res, proto.GetOpenPerpOrderResponse())

    async def get_open_perp_orders(
        self,
        get_open_perp_orders_request: proto.GetOpenPerpOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetOpenPerpOrdersResponse:
        params = ""
        for i in range(len(get_open_perp_orders_request.contracts)):
            params += "&contracts=" + str(
                get_open_perp_orders_request.contracts[i].name
            )

        async with self._session.get(
            f"{self._endpoint}/trade/perp/open-orders?ownerAddress={get_open_perp_orders_request.owner_address}"
            f"&accountAddress={get_open_perp_orders_request.account_address}"
            f"&project={get_open_perp_orders_request.project.name}{params}"
        ) as res:
            return await map_response(res, proto.GetOpenPerpOrdersResponse())

    async def post_cancel_perp_order(
        self,
        post_cancel_perp_order_request: proto.PostCancelPerpOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelPerpOrderResponse:
        request_dict = post_cancel_perp_order_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")

        async with self._session.post(
            f"{self._endpoint}/trade/perp/cancelbyid", json=request_dict
        ) as res:
            return await map_response(res, proto.PostCancelPerpOrderResponse())

    async def post_cancel_perp_orders(
        self,
        post_cancel_perp_orders_request: proto.PostCancelPerpOrdersRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelPerpOrdersResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/cancel",
            json=post_cancel_perp_orders_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostCancelPerpOrdersResponse())

    async def post_close_perp_positions(
        self,
        post_close_perp_positions_request: proto.PostClosePerpPositionsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostClosePerpPositionsResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/close",
            json=post_close_perp_positions_request.to_dict(),
        ) as res:
            return await map_response(
                res, proto.PostClosePerpPositionsResponse()
            )

    async def post_create_user(
        self,
        post_create_user_request: proto.PostCreateUserRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCreateUserResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/user",
            json=post_create_user_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostCreateUserResponse())

    async def get_user(
        self,
        get_user_request: proto.GetUserRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetUserResponse:
        async with self._session.get(
            f"{self._endpoint}/trade/user?ownerAddress={get_user_request.owner_address}"
            f"&project={get_user_request.project.name}&accountAddress={get_user_request.account_address}"
        ) as res:
            return await map_response(res, proto.GetUserResponse())

    async def post_manage_collateral(
        self,
        post_manage_collateral_request: proto.PostManageCollateralRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostManageCollateralResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/perp/managecollateral",
            json=post_manage_collateral_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostManageCollateralResponse())

    async def get_perp_positions(
        self,
        get_perp_positions_request: proto.GetPerpPositionsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPerpPositionsResponse:
        params = ""
        for i in range(len(get_perp_positions_request.contracts)):
            params += "&contracts=" + str(
                get_perp_positions_request.contracts[i].name
            )

        async with self._session.get(
            f"{self._endpoint}/trade/perp/positions?ownerAddress={get_perp_positions_request.owner_address}"
            f"&accountAddress={get_perp_positions_request.account_address}"
            f"&project={get_perp_positions_request.project.name}{params}"
        ) as res:
            return await map_response(res, proto.GetPerpPositionsResponse())

    async def post_trade_swap(
        self,
        trade_swap_request: proto.TradeSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.TradeSwapResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/swap", json=trade_swap_request.to_dict()
        ) as res:
            return await map_response(res, proto.TradeSwapResponse())

    async def post_order(
        self,
        post_order_request: proto.PostOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostOrderResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/place", json=post_order_request.to_dict()
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_cancel_order(
        self,
        post_cancel_order_request: proto.PostCancelOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelOrderResponse:
        request_dict = post_cancel_order_request.to_dict()
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")
        async with self._session.post(
            f"{self._endpoint}/trade/cancel",
            json=request_dict,
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_by_client_order_id(
        self,
        post_cancel_by_client_order_id_request: proto.PostCancelByClientOrderIdRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelOrderResponse:
        request_dict = post_cancel_by_client_order_id_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")
        async with self._session.post(
            f"{self._endpoint}/trade/cancelbyid", json=request_dict
        ) as res:
            return await map_response(res, proto.PostCancelOrderResponse())

    async def post_cancel_all(
        self,
        post_cancel_all_request: proto.PostCancelAllRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostCancelAllResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/cancelall",
            json=post_cancel_all_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostCancelAllResponse())

    async def post_settle(
        self,
        post_settle_request: proto.PostSettleRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSettleResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/settle", json=post_settle_request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSettleResponse())

    async def post_submit(
        self,
        post_submit_request: proto.PostSubmitRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitResponse:
        if transaction is None:
            raise ValueError("transaction cannot be omitted")

        async with self._session.post(
            f"{self._endpoint}/trade/submit", json=post_submit_request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

    async def post_submit_batch(
        self,
        post_submit_batch_request: proto.PostSubmitBatchRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitBatchResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/submit-batch",
            json=post_submit_batch_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSubmitBatchResponse())

    async def post_replace_by_client_order_id(
        self,
        post_order_request: proto.PostOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostOrderResponse:
        request_dict = post_order_request.to_dict()
        if "clientOrderId" in request_dict:
            request_dict["clientOrderID"] = request_dict.pop("clientOrderId")
        async with self._session.post(
            f"{self._endpoint}/trade/replacebyclientid", json=request_dict
        ) as res:
            return await map_response(res, proto.PostOrderResponse())

    async def post_replace_order(
        self,
        post_replace_order_request: proto.PostReplaceOrderRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostOrderResponse:
        request_dict = post_replace_order_request.to_dict()
        if "orderId" in request_dict:
            request_dict["orderID"] = request_dict.pop("orderId")

        async with self._session.post(
            f"{self._endpoint}/trade/replace",
            json=request_dict,
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
        metadata: Optional["MetadataLike"] = None,
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
