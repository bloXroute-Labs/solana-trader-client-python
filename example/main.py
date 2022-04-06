import asyncio

import bxserum
from bxserum import provider


async def main():
    await http()


async def http():
    p = provider.HttpProvider("127.0.0.1", 7000)
    api = bxserum.serum(p)

    await do_things(api)


async def grpc():
    p = provider.GrpcProvider("127.0.0.1", 7002)
    api = bxserum.serum(p)

    try:
        await do_things(api)
    finally:
        p.close()


async def do_things(api: bxserum.Api):
    print("checking request...")
    print(await api.get_orderbook(market="ETHUSDT"))

    print("checking stream...")
    async for response in api.get_orderbook_stream(market="ETHUSDT"):
        print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
