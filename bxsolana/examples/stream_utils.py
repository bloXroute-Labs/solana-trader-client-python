from bxsolana_trader_proto import api as proto
from .. import provider


async def do_stream(api: provider.Provider, run_slow: bool = False):
    item_count = 0
    print("streaming market depth updates...")
    async for response in api.get_market_depths_stream(
        get_market_depths_request=proto.GetMarketDepthsRequest(
            markets=["SOLUSDC"], limit=10, project=proto.Project.P_OPENBOOK
        )
    ):
        print(response.to_json())
        item_count += 1
        if item_count == 1:
            item_count = 0
            break

    print("streaming orderbook updates...")
    async for response in api.get_orderbooks_stream(
        get_orderbooks_request=proto.GetOrderbooksRequest(
            markets=["SOLUSDC"], project=proto.Project.P_OPENBOOK
        )
    ):
        print(response.to_json())
        item_count += 1
        if item_count == 1:
            item_count = 0
            break

    if run_slow:
        print("streaming ticker updates...")
        async for response in api.get_tickers_stream(
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
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming trade updates...")
        async for response in api.get_trades_stream(
            get_trades_request=proto.GetTradesRequest(
                market="SOLUSDC", project=proto.Project.P_OPENBOOK
            )
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming swap events...")
        async for response in api.get_swaps_stream(
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
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming pool reserves...")
        async for response in api.get_pool_reserves_stream(
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
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming price streams...")
        async for response in api.get_prices_stream(
            get_prices_stream_request=proto.GetPricesStreamRequest(
                projects=[proto.Project.P_RAYDIUM],
                tokens=[
                    "So11111111111111111111111111111111111111112",
                    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                ],
            )
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        if run_slow:
            print("streaming raydium new pool updates without cpmm pools...")
            async for response in api.get_new_raydium_pools_stream(
                get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest()
            ):
                print(response.to_json())
                item_count += 1
                if item_count == 1:
                    item_count = 0
                    break

    if run_slow:
        print("streaming raydium new pool updates with cpmm pools...")
        async for response in api.get_new_raydium_pools_stream(
            get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest(
                include_cpmm=True
            )
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming priority fee updates...")
        async for response in api.get_priority_fee_stream(
            get_priority_fee_request=proto.GetPriorityFeeRequest()
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming bundle tip updates...")
        async for response in api.get_bundle_tip_stream(
            get_bundle_tip_request=proto.GetBundleTipRequest()
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break
