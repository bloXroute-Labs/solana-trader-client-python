from asyncio.log import logger
import base64
from collections.abc import Callable, Awaitable
from pprint import pprint

from solders.hash import Hash

from bxsolana import provider
from bxsolana_trader_proto import api as proto

import os

from bxsolana.transaction import create_trader_api_tip_tx_signed, load_private_key_from_env

from solders import pubkey as pk # pyre-ignore[21]: module is too hard to find
from solders import instruction as inst # pyre-ignore[21]: module is too hard to find
from solders import transaction as solders_tx  # pyre-ignore[21]: module is too hard to find
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction
from solders import message as msg # pyre-ignore[21]: module is too hard to find
import base64



class Endpoint:
    func: Callable[[provider.Provider], Awaitable[bool]]
    requires_additional_env_vars: bool

    def __init__(self, func: Callable[[provider.Provider], Awaitable[bool]], requires_additional_env_vars: bool):
        self.func = func
        self.requires_additional_env_vars = requires_additional_env_vars


class EnvironmentVariables:
    private_key: str
    public_key: str
    open_orders_address: str
    payer: str

    def __init__(self, private_key, public_key, open_orders_address, payer):
        self.private_key = private_key
        self.public_key = public_key
        self.open_orders_address = open_orders_address
        self.payer = payer


def initializeEnvironmentVariables() -> EnvironmentVariables:
    if not os.getenv("AUTH_HEADER"):
        logger.critical("Must specify bloXroute authorization header!")
        raise SystemExit("AUTH_HEADER environment variable is required!")

    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        logger.error("PRIVATE_KEY environment variable not set. Cannot run examples requiring transaction submission.")

    public_key = os.getenv("PUBLIC_KEY")
    if not public_key:
        logger.warning("PUBLIC_KEY environment variable not set. Will skip place/cancel/settle examples.")

    open_orders_address = os.getenv("OPEN_ORDERS")
    if not open_orders_address:
        logger.error("OPEN_ORDERS environment variable not set. Requests may be slower.")

    payer = os.getenv("PAYER")
    if not payer:
        if public_key:
            logger.warning("PAYER environment variable not set. Defaulting to PUBLIC_KEY as payer.")
            payer = public_key
        else:
            payer = ""
            logger.error("PAYER and PUBLIC_KEY environment variables are both unset. PAYER cannot be defaulted.")

    return EnvironmentVariables(
        private_key=private_key or "",
        public_key=public_key or "",
        open_orders_address=open_orders_address or "",
        payer=payer
    )


UserEnvironment = initializeEnvironmentVariables()


async def get_markets(p: provider.Provider) -> bool:
    resp = await p.get_markets_v2(proto.GetMarketsRequestV2())
    pprint(resp)

    return True if resp.markets is not None else False


async def get_pools(p: provider.Provider) -> bool:
    resp = await p.get_pools(proto.GetPoolsRequest(projects=[proto.Project.P_RAYDIUM]))
    pprint(resp)
    return True if resp is not None else False


async def get_tickers(p: provider.Provider) -> bool:
    resp = await p.get_tickers_v2(proto.GetTickersRequestV2(market="SOLUSDC"))
    pprint(resp)

    return True if resp.tickers is not None else False


async def get_raydium_clmm_pools(p: provider.Provider) -> bool:
    resp = await p.get_raydium_clmm_pools(proto.GetRaydiumClmmPoolsRequest())
    pprint(resp)

    return True if resp.pools is not None else False


async def get_orderbook(p: provider.Provider) -> bool:
    resp = await p.get_orderbook_v2(proto.GetOrderbookRequestV2("SOL-USDC"))
    pprint(resp)

    return True if resp.market is not None else False


async def get_raydium_pool_reserves(p: provider.Provider) -> bool:
    resp = await p.get_raydium_pool_reserve(proto.GetRaydiumPoolReserveRequest(
        pairs_or_addresses=["HZ1znC9XBasm9AMDhGocd9EHSyH8Pyj1EUdiPb4WnZjo",
                            "D8wAxwpH2aKaEGBKfeGdnQbCc2s54NrRvTDXCK98VAeT"]))
    pprint(resp)

    return True if resp.pools is not None else False


async def get_market_depth(p: provider.Provider) -> bool:
    resp = await p.get_market_depth_v2(proto.GetMarketDepthRequestV2(market="SOLUSDC"))
    pprint(resp)

    return True if resp.market is not None else False


async def get_open_orders(p: provider.Provider) -> bool:
    resp = await p.get_open_orders_v2(
        proto.GetOpenOrdersRequestV2(market="SOLUSDC", address="FFqDwRq8B4hhFKRqx7N1M6Dg6vU699hVqeynDeYJdPj5"))
    pprint(resp)

    return True if resp.orders is not None else False


async def get_transaction(p: provider.Provider) -> bool:
    resp = await p.get_transaction(
        proto.GetTransactionRequest(
            signature="2s48MnhH54GfJbRwwiEK7iWKoEh3uNbS2zDEVBPNu7DaCjPXe3bfqo6RuCg9NgHRFDn3L28sMVfEh65xevf4o5W3"))
    pprint(resp)

    return True if resp.slot is not None else False


async def get_recent_blockhash(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())
    pprint(resp)

    return True if resp.block_hash is not None else False


async def get_recent_blockhash_offset(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2(offset=1))
    pprint(resp)

    return True if resp.block_hash is not None else False


async def get_rate_limit(p: provider.Provider) -> bool:
    resp = await p.get_rate_limit(proto.GetRateLimitRequest())
    pprint(resp)

    return True if resp.limit is not None else False


async def get_raydium_pools(p: provider.Provider) -> bool:
    resp = await p.get_raydium_pools(proto.GetRaydiumPoolsRequest())
    pprint(resp)

    return True if resp.pools is not None else False


async def get_price(p: provider.Provider) -> bool:
    resp = await p.get_price(proto.GetPriceRequest(tokens=["So11111111111111111111111111111111111111112",
                                                           "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"]))
    pprint(resp)

    return True if resp.token_prices is not None else False


async def get_raydium_prices(p: provider.Provider) -> bool:
    resp = await p.get_raydium_prices(
        proto.GetRaydiumPricesRequest(tokens=["So11111111111111111111111111111111111111112",
                                              "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"]))
    pprint(resp)

    return True if resp.token_prices is not None else False


async def get_jupiter_prices(p: provider.Provider) -> bool:
    resp = await p.get_jupiter_prices(
        proto.GetJupiterPricesRequest(tokens=["So11111111111111111111111111111111111111112",
                                              "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"]))
    pprint(resp)

    return True if resp.token_prices is not None else False


async def get_unsettled(p: provider.Provider) -> bool:
    resp = await p.get_unsettled_v2(
        proto.GetUnsettledRequestV2(market="SOLUSDC", owner_address="HxFLKUAmAMLz1jtT3hbvCMELwH5H9tpM2QugP8sKyfhc"))
    pprint(resp)

    return True if resp.market is not None else False


async def get_account_balance(p: provider.Provider) -> bool:
    if UserEnvironment.public_key != "":
        resp = await p.get_account_balance_v2(
            proto.GetAccountBalanceRequest(owner_address=UserEnvironment.public_key))
        pprint(resp)

    else:
        resp = await p.get_account_balance_v2(
            proto.GetAccountBalanceRequest(owner_address="HxFLKUAmAMLz1jtT3hbvCMELwH5H9tpM2QugP8sKyfhc"))
        pprint(resp)

    return True if resp.tokens is not None else False


async def get_quotes(p: provider.Provider) -> bool:
    resp = await p.get_quotes(proto.GetQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                                     out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                                     in_amount=0.01,
                                                     slippage=5,
                                                     limit=5))

    pprint(resp)

    return True if resp.quotes is not None else False


async def get_raydium_quotes(p: provider.Provider) -> bool:
    resp = await p.get_raydium_quotes(
        proto.GetRaydiumQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                      out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                      in_amount=0.01,
                                      slippage=5))

    pprint(resp)

    return True if resp.routes is not None else False


async def get_raydium_cpmm_quotes(p: provider.Provider) -> bool:
    resp = await p.get_raydium_cpmm_quotes(
        proto.GetRaydiumCpmmQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                          out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                          in_amount=0.01,
                                          slippage=5))

    pprint(resp)

    return True if resp.out_token is not None else False


async def get_raydium_clmm_quotes(p: provider.Provider) -> bool:
    resp = await p.get_raydium_clmm_quotes(
        proto.GetRaydiumClmmQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                          out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                          in_amount=0.01,
                                          slippage=5))

    pprint(resp)

    return True if resp.out_token is not None else False


async def get_jupiter_quotes(p: provider.Provider) -> bool:
    resp = await p.get_jupiter_quotes(
        proto.GetJupiterQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                      out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                      in_amount=0.01,
                                      slippage=5))

    pprint(resp)

    return True if resp.out_token is not None else False


async def get_pump_fun_quotes(p: provider.Provider) -> bool:
    p = provider.http_pump_ny()

    resp = await p.get_pump_fun_quotes(
        proto.GetPumpFunQuotesRequest(quote_type="buy",
                                      bonding_curve_address="Dga6eouREJ4kLHMqWWtccGGPsGebexuBYrcepBVd494q",
                                      mint_address="9QG5NHnfqQCyZ9SKhz7BzfjPseTFWaApmAtBTziXLanY",
                                      amount=0.01, slippage=5))

    pprint(resp)

    return True if resp.out_amount is not None else False

async def get_leader_schedule(p: provider.Provider) -> bool:
    resp = await p.get_leader_schedule(proto.GetLeaderScheduleRequest(max_slots=0))

    pprint(resp)

    # return True if resp
    return True

async def get_priority_fee(p: provider.Provider) -> bool:
    resp = await p.get_priority_fee(proto.GetPriorityFeeRequest())
    pprint(resp)

    return True if resp.fee_at_percentile is not None else False


async def get_token_accounts(p: provider.Provider) -> bool:
    resp = await p.get_token_accounts(proto.GetTokenAccountsRequest(owner_address=UserEnvironment.public_key))
    pprint(resp)

    return True if resp.accounts is not None else False


async def orderbook_stream(p: provider.Provider) -> bool:
    print("streaming orderbook updates...")

    async for resp in p.get_orderbooks_stream(
            get_orderbooks_request=proto.GetOrderbooksRequest(
                markets=["SOLUSDC"], project=proto.Project.P_OPENBOOK
            )
    ):
        pprint(resp)
        await p.close()

        return True if resp.orderbook is not None else False
    return False


async def market_depth_stream(p: provider.Provider) -> bool:
    print("streaming market depth updates...")

    async for resp in p.get_market_depths_stream(
            get_market_depths_request=proto.GetMarketDepthsRequest(
                markets=["SOLUSDC"], limit=5, project=proto.Project.P_OPENBOOK
            ),
            timeout=10,
    ):
        pprint(resp)
        await p.close()

        return True if resp.data is not None else False
    return False


async def get_tickers_stream(p: provider.Provider) -> bool:
    print("streaming ticker updates...")

    async for resp in p.get_tickers_stream(timeout=10,
                                           get_tickers_stream_request=proto.GetTickersStreamRequest(
                                               markets=[
                                                   "BONK/SOL",
                                                   "wSOL/RAY",
                                                   "BONK/RAY",
                                                   "RAY/USDC",
                                                   "SOL/USDC",
                                                   "SOL/USDC",
                                                   "RAY/USDC",
                                                   "USDT/USDC",
                                               ],
                                               project=proto.Project.P_OPENBOOK,
                                           )
                                           ):
        pprint(resp)
        await p.close()

        return True if resp.ticker is not None else False
    return False


async def get_prices_stream(p: provider.Provider) -> bool:
    print("streaming price streams...")
    async for resp in p.get_prices_stream(
            get_prices_stream_request=proto.GetPricesStreamRequest(
                projects=[proto.Project.P_RAYDIUM],
                tokens=[
                    "So11111111111111111111111111111111111111112",
                    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                ],
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.price is not None else False
    return False


async def get_swaps_stream(p: provider.Provider) -> bool:
    print("streaming swap events...")
    async for resp in p.get_swaps_stream(
            get_swaps_stream_request=proto.GetSwapsStreamRequest(
                projects=[proto.Project.P_RAYDIUM],
                # RAY-SOL , ETH-SOL, SOL-USDC, SOL-USDT
                pools=[
                    "AVs9TA4nWDzfPJE9gGVNJMVhcQy3V9PGazuz33BfG2RA",
                    "9Hm8QX7ZhE9uB8L2arChmmagZZBtBmnzBbpfxzkQp85D",
                    "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2",
                    "7XawhbbxtsRcQA8KTkHT9f9nc6d69UwqCDh6U5EEbEmX",
                ],
                include_failed=True,
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.swap is not None else False
    return False


async def get_trades_stream(p: provider.Provider) -> bool:
    print("streaming trade updates...")
    async for resp in p.get_trades_stream(
            get_trades_request=proto.GetTradesRequest(
                market="SOLUSDC", project=proto.Project.P_OPENBOOK
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.trades is not None else False
    return False


async def get_new_raydium_pools_stream(p: provider.Provider) -> bool:
    print("streaming raydium new pool updates without cpmm pools...")
    async for resp in p.get_new_raydium_pools_stream(
            get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest()
    ):
        pprint(resp)

        await p.close()
        return True if resp.pool is not None else False
    return False


async def get_new_raydium_pools_stream_cpmm(p: provider.Provider) -> bool:
    print("streaming raydium new pool updates without cpmm pools...")
    async for resp in p.get_new_raydium_pools_stream(
            get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest(
                include_cpmm=True
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.pool is not None else False
    return False


async def get_recent_blockhash_stream(p: provider.Provider) -> bool:
    print("streaming raydium new pool updates without cpmm pools...")
    async for resp in p.get_recent_block_hash_stream(
            get_recent_block_hash_request=proto.GetRecentBlockHashRequest(
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.block_hash is not None else False
    return False


async def get_pool_reserve_stream(p: provider.Provider) -> bool:
    print("streaming pool reserves...")
    async for resp in p.get_pool_reserves_stream(
            get_pool_reserves_stream_request=proto.GetPoolReservesStreamRequest(
                projects=[proto.Project.P_RAYDIUM],
                pools=[
                    "GHGxSHVHsUNcGuf94rqFDsnhzGg3qbN1dD1z6DHZDfeQ",
                    "HZ1znC9XBasm9AMDhGocd9EHSyH8Pyj1EUdiPb4WnZjo",
                    "D8wAxwpH2aKaEGBKfeGdnQbCc2s54NrRvTDXCK98VAeT",
                    "DdpuaJgjB2RptGMnfnCZVmC4vkKsMV6ytRa2gggQtCWt",
                ],
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.reserves is not None else False
    return False


async def get_block_stream(p: provider.Provider) -> bool:
    print("streaming pool reserves...")
    async for resp in p.get_block_stream(get_block_stream_request=proto.GetBlockStreamRequest()):
        pprint(resp)

        await p.close()
        return True if resp.block is not None else False
    return False


async def get_priority_fee_stream(p: provider.Provider) -> bool:
    print("streaming priority fee updates...")
    async for resp in p.get_priority_fee_stream(
            get_priority_fee_request=proto.GetPriorityFeeRequest()
    ):
        pprint(resp)
        await p.close()

        return True if resp.fee_at_percentile is not None else False
    return False


async def get_bundle_tip_stream(p: provider.Provider) -> bool:
    print("streaming bundle tip updates...")
    async for resp in p.get_bundle_tip_stream(
            get_bundle_tip_request=proto.GetBundleTipRequest()
    ):
        pprint(resp)
        await p.close()

        return True if resp.timestamp is not None else False
    return False

async def get_priority_fee_by_program_stream(p: provider.Provider) -> bool:
    print("streaming priority fee by program updates...")
    async for resp in p.get_priority_fee_by_program_stream(
            get_priority_fee_by_program_request=proto.GetPriorityFeeByProgramRequest(
                programs=[
                    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
                    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
                    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C"
                ]
            )
    ):
        pprint(resp)
        await p.close()

        return True if resp.data is not None else False
    return False

async def call_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit trade swap (using batch submit)...")

    response = await p.submit_post_trade_swap(project=proto.Project.P_RAYDIUM,
                                              owner_address=UserEnvironment.public_key,
                                              in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                              out_token="So11111111111111111111111111111111111111112",
                                              in_amount=0.01,
                                              slippage=0.5,
                                              compute_limit=200000,
                                              compute_price=100000,
                                              tip=1000000,
                                              submit_strategy=proto.SubmitStrategy.P_ABORT_ON_FIRST_ERROR,
                                              skip_pre_flight=True)

    print("signature for trade swap tx", response.transactions[0].signature)

    return True if response.transactions[0].signature else False


async def call_route_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit route trade swap (using batch submit)...")

    response = await p.submit_post_route_trade_swap(project=proto.Project.P_RAYDIUM,
                                                    owner_address=UserEnvironment.public_key,
                                                    slippage=0.5,
                                                    compute_price=100000,
                                                    compute_limit=200000,
                                                    tip=1000000,
                                                    steps=[proto.RouteStep(
                                                        in_token="So11111111111111111111111111111111111111112",
                                                        out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                                        in_amount=0.01,
                                                        out_amount_min=0.007505,
                                                        out_amount=0.0074,
                                                        project=proto.StepProject(label="Raydium",
                                                                                  id="58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"))])

    print("signature for route trade swap tx", response.transactions[0].signature)

    return True if response.transactions[0].signature else False


async def call_raydium_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit raydium trade swap...")

    response = await p.submit_raydium_swap(
        owner_address=UserEnvironment.public_key,
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_token="So11111111111111111111111111111111111111112",
        slippage=0.5,
        in_amount=0.01,
        compute_price=100000,
        compute_limit=200000,
        tip=1000000,
    )

    print("signature for raydium swap tx", response)

    return True if response != "" else False


async def call_raydium_cpmm_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit raydium cpmm trade swap...")

    response = await p.submit_raydium_swap_cpmm(
        owner_address=UserEnvironment.public_key,
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_token="So11111111111111111111111111111111111111112",
        slippage=0.5,
        in_amount=0.01,
        compute_price=100000,
        compute_limit=200000,
        tip=1000000,
    )

    print("signature for raydium cpmm swap tx", response)

    return True if response != "" else False


async def call_raydium_clmm_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit raydium clmm trade swap...")

    response = await p.submit_raydium_swap_clmm(
        owner_address=UserEnvironment.public_key,
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_token="So11111111111111111111111111111111111111112",
        slippage=0.5,
        in_amount=0.01,
        compute_price=100000,
        compute_limit=200000,
        tip=1000000,
    )

    print("signature for raydium clmm swap tx", response)

    return True if response != "" else False


async def call_jupiter_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit jupiter trade swap...")

    response = await p.submit_jupiter_swap(
        owner_address=UserEnvironment.public_key,
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_token="So11111111111111111111111111111111111111112",
        slippage=0.5,
        in_amount=0.01,
        compute_price=160000,
        compute_limit=200000,
        tip=1100000,
    )

    print("signature for jupiter swap tx", response)

    return True if response != "" else False

async def call_pump_fun_trade_swap(p: provider.Provider) -> bool:
    print("calling pump fun trade swap...")

    await p.close()

    p = provider.http_pump_ny()
    await p.connect()

    response = await p.submit_pump_fun_swap(
        owner_address=UserEnvironment.public_key,
        bonding_curve_address="3q1sBYJLF1bKSghg94MWsWb75NXwm2tJymT2f7VXJkju",
        token_address="5vzEtnMtjYWcKTuhXyoA8tn572SnAsZHH6mJ9rtApump",
        token_amount=10,
        sol_threshold=0.0001,
        is_buy=True,
        compute_price=160000,
        compute_limit=200000,
        tip=1100000,
    )

    print("signature for pump fun swap tx", response)

    return True if response != "" else False

async def create_personal_tx_and_submit(p: provider.Provider) -> bool:
    print("creating own transaction and submitting to trader api... ")

    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())

    tx = create_trader_api_tip_tx_signed(
        tip_amount=1100000,
        sender_address=load_private_key_from_env(),
        blockhash=Hash.from_string(resp.block_hash)
    )

    response = await p.post_submit(proto.PostSubmitRequest(
        transaction=tx,
        skip_pre_flight=True)
    )


    print("signature for custom user tx", response)

    return True if response != "" else False


async def call_submit_snipe(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())
    blockhash = Hash.from_string(resp.block_hash)
    
    fee_payer = Keypair()
    small_tip = 100_000
    staked_tip_threshold = 1_000_000
    tip_wallet = Pubkey.from_string("HWEoBxYs7ssKuudEjzjmpfJVX7Dvi7wescFsVx2L5yoY")
    jito_tip_wallet = Pubkey.from_string("96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5")

    # First transaction: transfer to both jito and bloxroute
    tx1_instructions = [
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=jito_tip_wallet,
            lamports=small_tip
        )),
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=tip_wallet, 
            lamports=small_tip
        ))
    ]

    tx1_message = MessageV0.try_compile(
        payer=fee_payer.pubkey(),
        instructions=tx1_instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    tx1 = VersionedTransaction(tx1_message, [fee_payer])
    signature1 = fee_payer.sign_message(msg.to_bytes_versioned(tx1.message))
    tx1 = VersionedTransaction.populate(tx1.message, [signature1])

    # Second transaction: staked transfer to bloxroute
    tx2_instructions = [
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=tip_wallet,
            lamports=staked_tip_threshold
        ))
    ]
    
    tx2_message = MessageV0.try_compile(
        payer=fee_payer.pubkey(),
        instructions=tx2_instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    tx2 = VersionedTransaction(tx2_message, [fee_payer])
    signature2 = fee_payer.sign_message(msg.to_bytes_versioned(tx2.message))
    tx2 = VersionedTransaction.populate(tx2.message, [signature2])

    transactions = [
        proto.TransactionMessage(
            content=base64.b64encode(bytes(tx1)).decode(),
            is_cleanup=False
        ),
        proto.TransactionMessage(
            content=base64.b64encode(bytes(tx2)).decode(),
            is_cleanup=False
        )
    ]

    result = await p.submit_snipe(transactions, use_staked_rpcs=True)
    print("Snipe Signatures:", result)
    return len(result) > 0