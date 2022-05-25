import asyncio

import bxserum
from bxserum import provider


async def main():
    await http()
    # await ws()
    # await grpc()


async def http():
    p = provider.HttpProvider("127.0.0.1", 9000)
    api = await bxserum.serum(p)

    # either `try`/`finally` or `async with` work with each type of provider
    try:
        await do_requests(api)
    finally:
        await p.close()


async def ws():
    async with provider.WsProvider("127.0.0.1", 9001) as api:
        await do_requests(api)
        await do_stream(api)


async def grpc():
    p = provider.GrpcProvider("127.0.0.1", 9002)
    api = await bxserum.serum(p)

    try:
        await do_requests(api)
        await do_stream(api)
    finally:
        await p.close()


async def do_requests(api: bxserum.Api):
    # markets API
    print("fetching all markets")
    print(await api.get_markets())

    print("fetching SOL/USDC orderbook")
    print(await api.get_orderbook(market="SOLUSDC"))

    print("fetching SOL/USDC ticker")
    print(await api.get_tickers(market="SOLUSDC"))

    print("fetching all tickers")
    print(await api.get_tickers())

    # print("fetching SOL/USDC ord")
    # print(await api.get_orders(market="SOLUSDC", address="AFT8VayE7qr8MoQsW3wHsDS83HhEvhGWdbNSHRKeUDfQ"))
    # print(await api.get_trades(market="SOLUSDC"))


async def do_stream(api: bxserum.Api):
    pass

    #print("checking stream...")
    #async for response in api.get_orderbook_stream(market="SOLUSDC"):
    #    print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
