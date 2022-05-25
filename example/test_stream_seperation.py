from typing import AsyncGenerator

import asyncio
from typing import AsyncGenerator

from bxserum.provider import WsProvider


async def listen_to_stream(gen: AsyncGenerator):
    async for item in gen:
        print("here 3")
        print(item)

async def print_num(int):
    try:
        for i in range(5):
            await asyncio.sleep(1)
            print(int)
    except asyncio.TimeoutError:
        return

async def main():
    ws = WsProvider(host="127.0.0.1", port=9001)
    await ws.connect()
    print("here")
    ob_stream1 = ws.get_orderbook_stream(market="SOLUSDC")
    #ob_stream2 = ws.get_orderbook_stream(market="SOLUSDT")

    task1 = asyncio.create_task(listen_to_stream(ob_stream1))
    #task2 = asyncio.create_task(listen_to_stream(ob_stream2))

    await task1
    #await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())