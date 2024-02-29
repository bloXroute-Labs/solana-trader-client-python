import asyncio

from bxsolana_trader_proto import api as proto
from .. import provider


async def do_stream(api: provider.Provider, run_slow: bool = False):
    item_count = 0
    await process_new_pools(api)
    #
    # if run_slow:
    #     print("streaming raydium new pool updates...")
    #     async for new_pool in api.get_new_raydium_pools_stream(
    #         get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest()
    #     ):
    #         print("new pool info : ", new_pool.to_json())
    #
    #         print("subscribing to swap events for the pool")
    #         async for swap_event in api.get_swaps_stream(
    #             get_swaps_stream_request=proto.GetSwapsStreamRequest(
    #                 projects=[proto.Project.P_RAYDIUM],
    #                 pools=[new_pool.pool.pool_address],
    #                 include_failed=True,
    #             )
    #         ):
    #             print(
    #                 "swap event for pool",
    #                 new_pool.pool.pool_address,
    #                 "swap event :",
    #                 swap_event.to_json(),
    #             )
    #             item_count += 1
    #             if item_count == 1:
    #                 item_count = 0


async def process_new_pools(api):
    async for new_pool in api.get_new_raydium_pools_stream(
            get_new_raydium_pools_request=proto.GetNewRaydiumPoolsRequest()
    ):
        print("new pool info : ", new_pool.to_json())
        print("subscribing to swap events for the pool")

        # Start the swap events processing in a separate task
        asyncio.create_task(process_swap_events(api, new_pool))


async def process_swap_events(api, new_pool):
    async for swap_event in api.get_swaps_stream(
            get_swaps_stream_request=proto.GetSwapsStreamRequest(
                projects=[proto.Project.P_RAYDIUM],
                pools=[new_pool.pool.pool_address],
                include_failed=True,
            )
    ):
        print(
            "swap event for pool",
            new_pool.pool.pool_address,
            "swap event :",
            swap_event.to_json(),
        )
