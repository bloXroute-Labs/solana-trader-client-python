from bxsolana_trader_proto import api as proto

from .. import provider


async def do_stream(api: provider.Provider, run_slow: bool = False):
    item_count = 0

    if run_slow:
        print("streaming orderbook updates...")
        async for response in api.get_orderbooks_stream(
            markets=["SOLUSDC"], project=proto.Project.P_OPENBOOK
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 5:
                item_count = 0
                break

    if run_slow:
        print("streaming ticker updates...")
        async for response in api.get_tickers_stream(
            market="SOLUSDC", project=proto.Project.P_OPENBOOK
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 5:
                item_count = 0
                break

    if run_slow:
        print("streaming trade updates...")
        async for response in api.get_trades_stream(
            market="SOLUSDC", project=proto.Project.P_OPENBOOK
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming swap events...")
        async for response in api.get_swaps_stream(
            projects=[proto.Project.P_RAYDIUM],
            # RAY-SOL
            pools=["AVs9TA4nWDzfPJE9gGVNJMVhcQy3V9PGazuz33BfG2RA"],
            include_failed=True,
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming pool reserves...")
        async for response in api.get_pool_reserves_stream(
            projects=[proto.Project.P_RAYDIUM]
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming price streams...")
        async for response in api.get_prices_stream(
            projects=[proto.Project.P_RAYDIUM],
            tokens=[
                "So11111111111111111111111111111111111111112",
                "USDC",
                "SOL",
                "USDT",
            ],
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break
