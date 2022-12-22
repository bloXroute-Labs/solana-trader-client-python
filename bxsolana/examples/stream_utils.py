import bxsolana
from bxsolana_trader_proto import api as proto


async def do_stream(api: bxsolana.Provider, run_slow=False):
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
            pools=["58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"],
            include_failed=True,
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break
