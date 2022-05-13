import asyncio

import bxserum
from bxserum import provider


async def main():
    await http()
    await ws()
    await grpc()


async def http():
    p = provider.HttpProvider("127.0.0.1", 9000)
    api = await bxserum.serum(p)

    try:
        await do(api)
    finally:
        await p.close()


async def ws():
    async with provider.WsProvider("127.0.0.1", 9001) as api:
        await do(api)

async def grpc():
    p = provider.GrpcProvider("127.0.0.1", 9002)
    api = await bxserum.serum(p)

    try:
        await do(api)
    finally:
        await p.close()


async def do(api: bxserum.Api):
    print("checking request...")
    print(await api.get_orderbook(market="SOLUSDC"))
    print(await api.get_orders(market="SOLUSDC", address="AFT8VayE7qr8MoQsW3wHsDS83HhEvhGWdbNSHRKeUDfQ"))
    print(await api.get_trades(market="SOLUSDC"))

    #print("checking stream...")
    #async for response in api.get_orderbook_stream(market="SOLUSDC"):
    #    print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
