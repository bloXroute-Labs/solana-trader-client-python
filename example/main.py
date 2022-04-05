import asyncio

from grpclib import client

from bxserum import proto


async def main():
    async with client.Channel("127.0.0.1", 7002) as channel:
        print("checking request...")
        service = proto.ApiStub(channel)
        result = await service.get_orderbook(market="ETHUSDT")
        print(result)

        print("checking stream...")
        async for response in service.get_orderbook_updates(market="ETHUSDC"):
            print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
