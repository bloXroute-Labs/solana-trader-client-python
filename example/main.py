import asyncio

import bxserum
from bxserum import provider


async def main():
    p = provider.GrpcProvider("127.0.0.1", 7002)
    api = bxserum.serum(p)

    try:
        print("checking request...")
        print(await api.get_orderbook(market="ETHUSDT"))

        print("checking stream...")
        async for response in api.get_orderbook_stream(market="ETHUSDC"):
            print(response)
    finally:
        p.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
