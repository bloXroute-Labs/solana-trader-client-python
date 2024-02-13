from bxsolana_trader_proto import api as proto
from .. import provider


async def do_stream(api: provider.Provider, run_slow: bool = False):
    item_count = 0

    if run_slow:
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
            get_tickers_request=proto.GetTickersRequest(
                market="SOLUSDC", project=proto.Project.P_OPENBOOK
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
                projects=[proto.Project.P_RAYDIUM]
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
                    "SOL",
                    "USDT",
                ],
            )
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming raydium new pool updates...")
        async for response in api.get_new_raydium_pools_stream(
            get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest()
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming bundle requests stream updates...")
        async for response in api.get_bundle_results_stream(
            get_bundle_results_stream_request=proto.GetBundleResultsStreamRequest()
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
