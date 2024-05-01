from bxsolana_trader_proto import api as proto

from .. import provider


async def do_requests(
    api: provider.Provider,
    public_key: str,
    open_orders: str,
    order_id: str,
    usdc_wallet: str,
    sol_usdc_market: str,
):
    print("fetching Raydium pool reserve")
    print(
        (
            await api.get_raydium_pool_reserve(
                get_raydium_pool_reserve_request=proto.GetRaydiumPoolReserveRequest(
                    pairs_or_addresses=[
                        "HZ1znC9XBasm9AMDhGocd9EHSyH8Pyj1EUdiPb4WnZjo",
                        "D8wAxwpH2aKaEGBKfeGdnQbCc2s54NrRvTDXCK98VAeT",
                        "DdpuaJgjB2RptGMnfnCZVmC4vkKsMV6ytRa2gggQtCWt",
                    ]
                )
            )
        ).to_json()
    )

    # prints too much info, that's why it's commented
    # print("fetching Raydium pools")
    # print(
    #     (
    #         await api.get_raydium_pools(
    #             get_raydium_pools_request=proto.GetRaydiumPoolsRequest()
    #         )
    #     ).to_json()
    # )

    print("getting transaction")
    print(
        (
            await api.get_transaction(
                get_transaction_request=proto.GetTransactionRequest(
                    signature="2s48MnhH54GfJbRwwiEK7iWKoEh3uNbS2zDEVBPNu7DaCjPXe3bfqo6RuCg9NgHRFDn3L28sMVfEh65xevf4o5W3"
                )
            )
        ).to_json()
    )

    print("getting ratelimit")
    print(
        (
            await api.get_rate_limit(
                get_rate_limit_request=proto.GetRateLimitRequest()
            )
        ).to_json()
    )

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

    print("fetching priority fee")
    print(
        (
            await api.get_priority_fee(
                get_priority_fee_request=proto.GetPriorityFeeRequest(
                    project=proto.Project.P_RAYDIUM
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
                        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
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
                        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
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
                        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
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
                    in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    out_token="So11111111111111111111111111111111111111112",
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
                    in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    out_token="So11111111111111111111111111111111111111112",
                    in_amount=0.01,
                    slippage=10,
                )
            )
        ).to_json()
    )

    print("fetching Jupiter quotes")
    print(
        (
            await api.get_jupiter_quotes(
                get_jupiter_quotes_request=proto.GetJupiterQuotesRequest(
                    in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    out_token="So11111111111111111111111111111111111111112",
                    in_amount=0.01,
                    slippage=10,
                    fast_mode=True,
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
                    side="ASK",
                    amount=0.1,
                    price=150_000,
                    type="limit",
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
                        side="ASK",
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
                    side="ASK",
                    type="limit",
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
                        side="ASK",
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
                    in_token="So11111111111111111111111111111111111111112",
                    in_amount=0.01,
                    out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
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
                    in_token="So11111111111111111111111111111111111111112",
                    in_amount=0.01,
                    out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
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
                    in_token="So11111111111111111111111111111111111111112",
                    in_amount=0.01,
                    out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    slippage=0.01,
                    fast_mode=True,
                )
            )
        )
    )

    print("generate route swap")
    step = proto.RouteStep(
        in_token="So11111111111111111111111111111111111111112",
        in_amount=0.01,
        out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_amount=0.007505,
        out_amount_min=0.0074,
        project=proto.StepProject(
            label="Raydium", id="58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"
        ),
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
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        in_amount=0.01,
        out_token="So11111111111111111111111111111111111111112",
        out_amount=0.01,
        out_amount_min=0.01,
        project=proto.StepProject(
            label="Raydium", id="58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"
        ),
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
