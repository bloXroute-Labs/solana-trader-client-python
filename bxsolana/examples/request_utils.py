from bxsolana_trader_proto import api as proto

from .. import provider


async def do_requests(
    api: provider.Provider,
    pumpny_api: provider.Provider,
    public_key: str,
):
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
