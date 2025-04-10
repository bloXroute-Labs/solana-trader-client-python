from bxsolana_trader_proto import api as proto

from .. import provider


async def do_requests(
    api: provider.Provider,
    pumpny_api: provider.Provider,
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

    print("fetching Raydium CLMM pools")
    print(
        (
            await api.get_raydium_clmm_pools(
                get_raydium_clmm_pools_request=proto.GetRaydiumClmmPoolsRequest()
            )
        ).to_json()
    )

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

    print("fetching priority fee by program")
    print(
        (
            await api.get_priority_fee_by_program(
                get_priority_fee_by_program_request=proto.GetPriorityFeeByProgramRequest(
                    programs=[
                        "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
	                    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C",
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

    print("fetching PumpFun quotes")
    print(
        (
            await pumpny_api.get_pump_fun_quotes(
                get_pump_fun_quotes_request=proto.GetPumpFunQuotesRequest(
                    bonding_curve_address=(
                        "Dga6eouREJ4kLHMqWWtccGGPsGebexuBYrcepBVd494q"
                    ),
                    mint_address="9QG5NHnfqQCyZ9SKhz7BzfjPseTFWaApmAtBTziXLanY",
                    amount=0.01,
                    quote_type="buy",
                )
            )
        ).to_json()
    )

    print("fetching Raydium CLMM quotes")
    print(
        (
            await api.get_raydium_clmm_quotes(
                get_raydium_clmm_quotes_request=proto.GetRaydiumClmmQuotesRequest(
                    in_token="USDC",
                    out_token="SOL",
                    in_amount=32,
                    slippage=10,
                )
            )
        ).to_json()
    )

    print("fetching Raydium CPMM quotes")
    print(
        (
            await api.get_raydium_cpmm_quotes(
                get_raydium_cpmm_quotes_request=proto.GetRaydiumCpmmQuotesRequest(
                    in_token="USDC",
                    out_token="SOL",
                    in_amount=32,
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

    print("generate raydium CLMM swap")
    print(
        (
            await api.post_raydium_clmm_swap(
                post_raydium_swap_request=proto.PostRaydiumSwapRequest(
                    owner_address=public_key,
                    in_token="SOL",
                    in_amount=1,
                    out_token="USDC",
                    slippage=10,
                )
            )
        )
    )

    print("generate raydium CPMM swap")
    print(
        (
            await api.post_raydium_cpmm_swap(
                post_raydium_cpmm_swap_request=proto.PostRaydiumCpmmSwapRequest(
                    owner_address=public_key,
                    in_token="SOL",
                    in_amount=1,
                    out_token="USDC",
                    slippage=10,
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

    print("generate pump_fun swap")
    print(
        (
            await pumpny_api.post_pump_fun_swap(
                post_pump_fun_swap_request=proto.PostPumpFunSwapRequest(
                    user_address=public_key,
                    bonding_curve_address=(
                        "7BcRpqUC7AF5Xsc3QEpCb8xmoi2X1LpwjUBNThbjWvyo"
                    ),
                    token_address=(
                        "BAHY8ocERNc5j6LqkYav1Prr8GBGsHvBV5X3dWPhsgXw"
                    ),
                    token_amount=10,
                    sol_threshold=0.0001,
                    is_buy=True,
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
                )
            )
        )
    )

    print("generate route swap")
    step = proto.RaydiumRouteStep(
        in_token="So11111111111111111111111111111111111111112",
        in_amount=0.01,
        out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_amount=0.007505,
        out_amount_min=0.0074,
        project=proto.StepProject(
            label="Raydium", id="58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"
        ),
    )

    print("generate raydium CLMM route swap")
    print(
        (
            await api.post_raydium_clmm_route_swap(
                post_raydium_route_swap_request=proto.PostRaydiumRouteSwapRequest(
                    owner_address=public_key,
                    slippage=10,
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

    print("fetching Recent Block Hash")
    print(
        (
            await api.get_recent_block_hash(
                get_recent_block_hash_request=proto.GetRecentBlockHashRequest()
            )
        ).to_json()
    )

    print("fetching Recent Block Hash V2 without offset")
    print(
        (
            await api.get_recent_block_hash_v2(
                get_recent_block_hash_request_v2=proto.GetRecentBlockHashRequestV2()
            )
        ).to_json()
    )

    print("fetching Recent Block Hash V2 with offset")
    print(
        (
            await api.get_recent_block_hash_v2(
                get_recent_block_hash_request_v2=proto.GetRecentBlockHashRequestV2(
                    offset=1
                )
            )
        ).to_json()
    )
