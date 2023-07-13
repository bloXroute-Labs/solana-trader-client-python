from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import PerpPositionSide
from bxsolana_trader_proto.common import PerpOrderType
from bxsolana_trader_proto.common import PerpContract
from bxsolana_trader_proto.common import PerpCollateralType
from bxsolana_trader_proto.common import PerpCollateralToken
from bxsolana_trader_proto.common import PostOnlyParams

from .. import provider


async def do_requests(
    api: provider.Provider,
    public_key: str,
    open_orders: str,
    order_id: str,
    usdc_wallet: str,
    sol_usdc_market: str,
):
    print("fetching market depth")
    print(
        (
            await api.get_market_depth_v2(
                get_market_depth_request_v2=proto.GetMarketDepthRequestV2(
                    limit=1, market="SOLUSDC"
                )
            )
        ).to_json()
    )

    # markets API
    print("fetching all markets")
    print(
        (
            await api.get_markets_v2(
                get_markets_request_v2=proto.GetMarketsRequestV2()
            )
        ).to_json()
    )

    print("fetching SOL/USDC orderbook")
    print(
        (
            await api.get_orderbook_v2(
                get_orderbook_request_v2=proto.GetOrderbookRequestV2(
                    market="SOLUSDC"
                )
            )
        ).to_json()
    )

    print("fetching SOL/USDC ticker")
    print(
        (
            await api.get_tickers_v2(
                get_tickers_request_v2=proto.GetTickersRequestV2(
                    market="SOLUSDC"
                )
            )
        ).to_json()
    )

    print("fetching all tickers")
    print(
        (
            await api.get_tickers_v2(
                get_tickers_request_v2=proto.GetTickersRequestV2()
            )
        ).to_json()
    )

    print("fetching prices")

    print(
        (
            await api.get_price(
                get_price_request=proto.GetPriceRequest(
                    tokens=[
                        "So11111111111111111111111111111111111111112",
                        "SOL",
                        "USDT",
                    ]
                )
            )
        ).to_json()
    )

    print("fetching Raydium prices")

    print(
        (
            await api.get_raydium_prices(
                get_raydium_prices_request=proto.GetRaydiumPricesRequest(
                    tokens=[
                        "So11111111111111111111111111111111111111112",
                        "SOL",
                        "USDT",
                    ]
                )
            )
        ).to_json()
    )

    print("fetching Jupiter prices")

    print(
        (
            await api.get_jupiter_prices(
                get_jupiter_prices_request=proto.GetJupiterPricesRequest(
                    tokens=[
                        "So11111111111111111111111111111111111111112",
                        "SOL",
                        "USDT",
                    ]
                )
            )
        ).to_json()
    )

    print("fetching pools")
    print(
        (
            await api.get_pools(
                get_pools_request=proto.GetPoolsRequest(
                    projects=[proto.Project.P_RAYDIUM]
                )
            )
        ).to_json()
    )

    print("fetching Raydium pools")
    print(
        (
            await api.get_raydium_pools(
                get_raydium_pools_request=proto.GetRaydiumPoolsRequest()
            )
        ).to_json()
    )

    print("fetching quotes")
    print(
        (
            await api.get_quotes(
                get_quotes_request=proto.GetQuotesRequest(
                    in_token="USDT",
                    out_token="SOL",
                    in_amount=0.01,
                    slippage=10,
                    limit=1,
                    projects=[proto.Project.P_RAYDIUM],
                )
            )
        ).to_json()
    )

    print("fetching Raydium quotes")
    print(
        (
            await api.get_raydium_quotes(
                get_raydium_quotes_request=proto.GetRaydiumQuotesRequest(
                    in_token="USDT",
                    out_token="SOL",
                    in_amount=0.01,
                    slippage=10,
                    limit=1,
                )
            )
        ).to_json()
    )

    print("fetching Jupiter quotes")
    print(
        (
            await api.get_jupiter_quotes(
                get_jupiter_quotes_request=proto.GetJupiterQuotesRequest(
                    in_token="USDT",
                    out_token="SOL",
                    in_amount=0.01,
                    slippage=10,
                    limit=1,
                )
            )
        ).to_json()
    )

    # trade API
    print("fetching open orders for account")
    print(
        (
            await api.get_open_orders_v2(
                get_open_orders_request_v2=proto.GetOpenOrdersRequestV2(
                    order_id="",
                    client_order_id=0,
                    market="SOLUSDC",
                    address=public_key,
                    limit=0,
                )
            )
        ).to_json()
    )

    print("fetching unsettled amounts")
    print(
        (
            await api.get_unsettled_v2(
                get_unsettled_request_v2=proto.GetUnsettledRequestV2(
                    market="SOLUSDC",
                    owner_address=public_key,
                )
            )
        ).to_json()
    )

    print("fetching account balance amounts")
    print(
        (
            await api.get_account_balance(
                get_account_balance_request=proto.GetAccountBalanceRequest(
                    owner_address=public_key
                )
            )
        ).to_json()
    )

    print("fetching token accounts and balances")
    print(
        (
            await api.get_token_accounts(
                get_token_accounts_request=proto.GetTokenAccountsRequest(
                    owner_address=public_key
                )
            )
        ).to_json()
    )

    print(
        "generating unsigned order (no sign or submission) to sell 0.1 SOL for"
        " USDC at 150_000 USD/SOL"
    )
    print(
        (
            await api.post_order_v2(
                post_order_request_v2=proto.PostOrderRequestV2(
                    owner_address=public_key,
                    payer_address=public_key,
                    market="SOLUSDC",
                    side=proto.Side.S_ASK,
                    amount=0.1,
                    price=150_000,
                    # optional, but much faster if known
                    open_orders_address=open_orders,
                    # optional, for identification
                    client_order_id=0,
                )
            )
        ).to_json()
    )
    if order_id != "":
        print("generate cancel order")
        print(
            (
                await api.post_cancel_order_v2(
                    post_cancel_order_request_v2=proto.PostCancelOrderRequestV2(
                        order_id=order_id,
                        side=proto.Side.S_ASK,
                        market_address="SOLUSDC",
                        owner_address=public_key,
                        open_orders_address=open_orders,
                        client_order_id=0,
                    )
                )
            ).to_json()
        )

    print("generate cancel order by client ID")
    print(
        await api.post_cancel_order_v2(
            post_cancel_order_request_v2=proto.PostCancelOrderRequestV2(
                client_order_id=123,
                market_address=sol_usdc_market,
                owner_address=public_key,
                open_orders_address=open_orders,
            )
        )
    )

    print("generate settle order")
    print(
        await api.post_settle_v2(
            post_settle_request_v2=proto.PostSettleRequestV2(
                owner_address=public_key,
                market="SOLUSDC",
                base_token_wallet=public_key,
                quote_token_wallet=usdc_wallet,
                open_orders_address=open_orders,
            )
        )
    )

    print("generate replace by client order id")
    print(
        (
            await api.post_replace_order_v2(
                post_replace_order_request_v2=proto.PostReplaceOrderRequestV2(
                    owner_address=public_key,
                    payer_address=public_key,
                    market="SOLUSDC",
                    side=proto.Side.S_ASK,
                    amount=0.1,
                    price=150_000,
                    # optional, but much faster if known
                    open_orders_address=open_orders,
                    # optional, for identification
                    client_order_id=123,
                )
            )
        ).to_json()
    )
    if order_id != "":
        print("generate replace by order id")
        print(
            (
                await api.post_replace_order_v2(
                    post_replace_order_request_v2=proto.PostReplaceOrderRequestV2(
                        owner_address=public_key,
                        payer_address=public_key,
                        market="SOLUSDC",
                        side=proto.Side.S_ASK,
                        amount=0.1,
                        price=150_000,
                        # optional, but much faster if known
                        open_orders_address=open_orders,
                        # optional, for identification
                        client_order_id=0,
                        order_id=order_id,
                    )
                )
            ).to_json()
        )

    print("generate trade swap")
    print(
        (
            await api.post_trade_swap(
                trade_swap_request=proto.TradeSwapRequest(
                    project=proto.Project.P_RAYDIUM,
                    owner_address=public_key,
                    in_token="SOL",
                    in_amount=0.01,
                    out_token="USDT",
                    slippage=0.01,
                )
            )
        )
    )

    print("generate raydium swap")
    print(
        (
            await api.post_raydium_swap(
                post_raydium_swap_request=proto.PostRaydiumSwapRequest(
                    owner_address=public_key,
                    in_token="SOL",
                    in_amount=0.01,
                    out_token="USDT",
                    slippage=0.01,
                )
            )
        )
    )

    print("generate jupiter swap")
    print(
        (
            await api.post_jupiter_swap(
                post_jupiter_swap_request=proto.PostJupiterSwapRequest(
                    owner_address=public_key,
                    in_token="SOL",
                    in_amount=0.01,
                    out_token="USDT",
                    slippage=0.01,
                )
            )
        )
    )

    print("generate route swap")
    step = proto.RouteStep(
        in_token="USDT",
        in_amount=0.01,
        out_token="SOL",
        out_amount=0.01,
        out_amount_min=0.01,
        project=proto.StepProject(label="Raydium"),
    )
    print(
        (
            await api.post_route_trade_swap(
                route_trade_swap_request=proto.RouteTradeSwapRequest(
                    project=proto.Project.P_RAYDIUM,
                    owner_address=public_key,
                    slippage=0.1,
                    steps=[step],
                )
            )
        ).to_json()
    )

    print("generate raydium route swap")
    step = proto.RaydiumRouteStep(
        in_token="USDT",
        in_amount=0.01,
        out_token="SOL",
        out_amount=0.01,
        out_amount_min=0.01,
    )
    print(
        (
            await api.post_raydium_route_swap(
                post_raydium_route_swap_request=proto.PostRaydiumRouteSwapRequest(
                    owner_address=public_key,
                    slippage=0.1,
                    steps=[step],
                )
            )
        ).to_json()
    )

    # DRIFT
    print("post Drift close perp positions")
    print(
        (
            await api.post_close_drift_perp_positions(
                post_close_drift_perp_positions_request=proto.PostCloseDriftPerpPositionsRequest(
                    owner_address=public_key,
                    contracts=["SOL_PERP"],
                )
            )
        ).to_json()
    )

    print("post Drift create user")
    print(
        (
            await api.post_create_drift_user(
                post_create_drift_user_request=proto.PostCreateDriftUserRequest(
                    action="CREATE",
                    owner_address=(
                        "BgJ8uyf9yhLJaUVESRrqffzwVyQgRi9YvWmpEFaH14kx"
                    ),
                )
            )
        ).to_json()
    )

    print("post Drift deposit collateral")
    print(
        (
            await api.post_drift_manage_collateral(
                post_drift_manage_collateral_request=proto.PostDriftManageCollateralRequest(
                    account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    amount=0.1,
                    token="USDC",
                    type="DEPOSIT",
                )
            )
        ).to_json()
    )

    print("post Drift settle pnl")
    print(
        (
            await api.post_drift_settle_pnl(
                post_drift_settle_pnl_request=proto.PostDriftSettlePnlRequest(
                    owner_address=public_key,
                    settlee_account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    contract="SOL_PERP",
                )
            )
        ).to_json()
    )

    print("post Drift settle pnls")
    print(
        (
            await api.post_drift_settle_pn_ls(
                post_drift_settle_pn_ls_request=proto.PostDriftSettlePnLsRequest(
                    owner_address=public_key,
                    settlee_account_addresses=[
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ],
                    contract="SOL_PERP",
                )
            )
        ).to_json()
    )

    print("post Drift liquidate perp")
    print(
        (
            await api.post_liquidate_drift_perp(
                post_liquidate_drift_perp_request=proto.PostLiquidateDriftPerpRequest(
                    owner_address=public_key,
                    settlee_account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    contract="SOL_PERP",
                    amount=1,
                )
            )
        ).to_json()
    )

    print("get Drift perp orderbook")
    print(
        (
            await api.get_drift_perp_orderbook(
                get_drift_perp_orderbook_request=proto.GetDriftPerpOrderbookRequest(
                    contract="SOL_PERP",
                )
            )
        ).to_json()
    )

    print("get Drift user")
    print(
        (
            await api.get_drift_user(
                get_drift_user_request=proto.GetDriftUserRequest(
                    owner_address=public_key
                )
            )
        ).to_json()
    )

    print("get Drift assets")
    print(
        (
            await api.get_drift_assets(
                get_drift_assets_request=proto.GetDriftAssetsRequest(
                    owner_address=public_key,
                )
            )
        ).to_json()
    )

    print("get Drift perp contracts")
    print(
        (
            await api.get_drift_perp_contracts(
                get_drift_perp_contracts_request=proto.GetDriftPerpContractsRequest()
            )
        ).to_json()
    )

    print("post Drift get perp open order")
    print(
        (
            await api.get_drift_open_perp_order(
                get_drift_open_perp_order_request=proto.GetDriftOpenPerpOrderRequest(
                    owner_address=public_key, client_order_id=12, order_id=1
                )
            )
        ).to_json()
    )

    print("post Drift get open margin order")
    print(
        (
            await api.get_drift_open_margin_order(
                get_drift_open_margin_order_request=proto.GetDriftOpenMarginOrderRequest(
                    owner_address=public_key,
                    client_order_id=13,
                    order_id=8,
                )
            )
        ).to_json()
    )

    print("post Drift get open perp positions")
    print(
        (
            await api.get_drift_perp_positions(
                get_drift_perp_positions_request=proto.GetDriftPerpPositionsRequest(
                    owner_address=public_key, contracts=["SOL_PERP"]
                )
            )
        ).to_json()
    )

    print("post Drift get perp open orders")
    print(
        (
            await api.get_drift_open_perp_orders(
                get_drift_open_perp_orders_request=proto.GetDriftOpenPerpOrdersRequest(
                    owner_address=public_key, contracts=["SOL_PERP"]
                )
            )
        ).to_json()
    )

    print("post Drift cancel perp order")
    print(
        (
            await api.post_drift_cancel_perp_order(
                post_drift_cancel_perp_order_request=proto.PostDriftCancelPerpOrderRequest(
                    owner_address=public_key, contract="SOL_PERP"
                )
            )
        ).to_json()
    )

    print("post Drift modify order")
    print(
        (
            await api.post_modify_drift_order(
                post_modify_drift_order_request=proto.PostModifyDriftOrderRequest(
                    owner_address=public_key,
                    new_position_side="long",
                    order_id=1,
                )
            )
        ).to_json()
    )
    print("post Drift get open margin orders")
    print(
        (
            await api.get_drift_open_margin_orders(
                get_drift_open_margin_orders_request=proto.GetDriftOpenMarginOrdersRequest(
                    owner_address=public_key, markets=["SOL"]
                )
            )
        ).to_json()
    )

    print("post Drift cancel margin orders")
    print(
        (
            await api.post_cancel_drift_margin_order(
                post_cancel_drift_margin_order_request=proto.PostCancelDriftMarginOrderRequest(
                    owner_address=public_key
                )
            )
        ).to_json()
    )

    print("post Drift margin trading flag")
    print(
        (
            await api.post_drift_enable_margin_trading(
                post_drift_enable_margin_trading_request=proto.PostDriftEnableMarginTradingRequest(
                    owner_address=public_key, enable_margin=True
                )
            )
        ).to_json()
    )

    print("post Drift Margin order")
    print(
        (
            await api.post_drift_margin_order(
                post_drift_margin_order_request=proto.PostDriftMarginOrderRequest(
                    owner_address=public_key,
                    market="SOL",
                    position_side="LONG",
                    slippage=10,
                    type="MARKET",  # or Limit
                    amount=10,
                    client_order_id=12,
                    post_only=PostOnlyParams.PO_NONE,
                )
            )
        ).to_json()
    )

    print("get Drift markets")
    print(
        (
            await api.get_drift_markets(
                get_drift_markets_request=proto.GetDriftMarketsRequest(
                    metadata=True
                )
            )
        ).to_json()
    )

    print("get Drift margin orderbook")
    print(
        (
            await api.get_drift_margin_orderbook(
                get_drift_margin_orderbook_request=proto.GetDriftMarginOrderbookRequest(
                    market="SOL", limit=2, metadata=True
                )
            )
        ).to_json()
    )

    print("get user")
    print(
        (
            await api.get_user(
                get_user_request=proto.GetUserRequest(
                    project=proto.Project.P_DRIFT, owner_address=public_key
                )
            )
        ).to_json()
    )

    print("get Drift perp orderbook")
    print(
        (
            await api.get_perp_orderbook(
                get_perp_orderbook_request=proto.GetPerpOrderbookRequest(
                    contract=PerpContract.SOL_PERP,
                    project=proto.Project.P_DRIFT,
                )
            )
        ).to_json()
    )

    print("get Drift market depth")
    print(
        (
            await api.get_drift_market_depth(
                get_drift_market_depth_request=proto.GetDriftMarketDepthRequest(
                    contract="SOL_PERP", limit=3
                )
            )
        ).to_json()
    )

    print("post perp order")
    print(
        (
            await api.post_perp_order(
                post_perp_order_request=proto.PostPerpOrderRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    contract=PerpContract.SOL_PERP,
                    position_side=PerpPositionSide.PS_LONG,
                    slippage=0,
                    type=PerpOrderType.POT_LIMIT,
                    amount=0,
                    price=12000,
                    client_order_id=12,
                )
            )
        ).to_json()
    )

    print("get perp contracts")
    print(
        (
            await api.get_perp_contracts(
                get_perp_contracts_request=proto.GetPerpContractsRequest(
                    project=proto.Project.P_DRIFT,
                )
            )
        ).to_json()
    )

    print("get perp assets")
    print(
        (
            await api.get_assets(
                get_assets_request=proto.GetAssetsRequest(
                    owner_address=public_key,
                    project=proto.Project.P_DRIFT,
                )
            )
        ).to_json()
    )

    print("get open perp order")
    print(
        (
            await api.get_open_perp_order(
                get_open_perp_order_request=proto.GetOpenPerpOrderRequest(
                    owner_address=public_key,
                    project=proto.Project.P_DRIFT,
                    client_order_id=12,
                )
            )
        ).to_json()
    )

    print("get open perp orders")
    print(
        (
            await api.get_open_perp_orders(
                get_open_perp_orders_request=proto.GetOpenPerpOrdersRequest(
                    owner_address=public_key,
                    project=proto.Project.P_DRIFT,
                    contracts=[PerpContract.SOL_PERP, PerpContract.BTC_PERP],
                )
            )
        ).to_json()
    )

    print("post liquidate perp")
    print(
        (
            await api.post_liquidate_perp(
                post_liquidate_perp_request=proto.PostLiquidatePerpRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    settlee_account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    contract=PerpContract.SOL_PERP,
                    amount=1,
                )
            )
        ).to_json()
    )

    print("post settle pnl")
    print(
        (
            await api.post_settle_pnl(
                post_settle_pnl_request=proto.PostSettlePnlRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    settlee_account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    contract=PerpContract.SOL_PERP,
                )
            )
        ).to_json()
    )

    print("post settle pnls")
    print(
        (
            await api.post_settle_pn_ls(
                post_settle_pn_ls_request=proto.PostSettlePnLsRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    settlee_account_addresses=[
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ],
                    contract=PerpContract.SOL_PERP,
                )
            )
        ).to_json()
    )

    print("post cancel perp order")
    print(
        (
            await api.post_cancel_perp_order(
                post_cancel_perp_order_request=proto.PostCancelPerpOrderRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    client_order_id=12,
                    order_id=0,
                    contract=PerpContract.SOL_PERP,
                )
            )
        ).to_json()
    )

    print("post close perp positions")
    print(
        (
            await api.post_close_perp_positions(
                post_close_perp_positions_request=proto.PostClosePerpPositionsRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    contracts=[PerpContract.SOL_PERP],
                )
            )
        ).to_json()
    )

    print("post cancel perp orders")
    print(
        (
            await api.post_cancel_perp_orders(
                post_cancel_perp_orders_request=proto.PostCancelPerpOrdersRequest(
                    project=proto.Project.P_DRIFT,
                    contract=PerpContract.SOL_PERP,
                    owner_address=public_key,
                )
            )
        ).to_json()
    )

    print("post create user")
    print(
        (
            await api.post_create_user(
                post_create_user_request=proto.PostCreateUserRequest(
                    project=proto.Project.P_DRIFT,
                    action="CREATE",
                    owner_address=(
                        "BgJ8uyf9yhLJaUVESRrqffzwVyQgRi9YvWmpEFaH14kx"
                    ),
                )
            )
        ).to_json()
    )

    print("post deposit collateral")
    print(
        (
            await api.post_manage_collateral(
                post_manage_collateral_request=proto.PostManageCollateralRequest(
                    project=proto.Project.P_DRIFT,
                    account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    amount=0.1,
                    token=PerpCollateralToken.PCTK_USDC,
                    type=PerpCollateralType.PCT_DEPOSIT,
                )
            )
        ).to_json()
    )

    print("post withdraw collateral")
    print(
        (
            await api.post_manage_collateral(
                post_manage_collateral_request=proto.PostManageCollateralRequest(
                    project=proto.Project.P_DRIFT,
                    account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    amount=0.1,
                    token=PerpCollateralToken.PCTK_SOL,
                    type=PerpCollateralType.PCT_WITHDRAWAL,
                )
            )
        ).to_json()
    )

    print("post transfer collateral")
    print(
        (
            await api.post_manage_collateral(
                post_manage_collateral_request=proto.PostManageCollateralRequest(
                    project=proto.Project.P_DRIFT,
                    account_address=(
                        "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                    ),
                    amount=0.1,
                    token=PerpCollateralToken.PCTK_SOL,
                    type=PerpCollateralType.PCT_TRANSFER,
                    to_account_address=(
                        "AbnwAQGrYnvktT4ihhX5np8RbgtfXJfPwpgMJnCFa4MT"
                    ),
                )
            )
        ).to_json()
    )

    print("get perp positions")
    print(
        (
            await api.get_perp_positions(
                get_perp_positions_request=proto.GetPerpPositionsRequest(
                    project=proto.Project.P_DRIFT,
                    owner_address=public_key,
                    contracts=[PerpContract.SOL_PERP],
                )
            )
        ).to_json()
    )
