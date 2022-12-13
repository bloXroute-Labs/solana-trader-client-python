import bxsolana
from bxsolana_trader_proto import api as proto

async def do_stream(api: bxsolana.Provider,
                    run_slow_streams: False):
    item_count = 0

    if run_slow_streams:
        print("streaming orderbook updates...")
        async for response in api.get_orderbooks_stream(markets=["SOLUSDC"], project=proto.Project.P_OPENBOOK):
            print(response.to_json())
            item_count += 1
            if item_count == 5:
                item_count = 0
                break

    if run_slow_streams:
        print("streaming ticker updates...")
        async for response in api.get_tickers_stream(market="SOLUSDC", project=proto.Project.P_OPENBOOK):
            print(response.to_json())
            item_count += 1
            if item_count == 5:
                item_count = 0
                break

    if run_slow_streams:
        print("streaming trade updates...")
        async for response in api.get_trades_stream(market="SOLUSDC", project=proto.Project.P_OPENBOOK):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break