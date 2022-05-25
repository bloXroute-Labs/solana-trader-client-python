import asyncio

import bxserum
from bxserum import provider, proto

# sample public key for trades API
PUBLIC_KEY = "AFT8VayE7qr8MoQsW3wHsDS83HhEvhGWdbNSHRKeUDfQ"


async def main():
    await http()
    # await ws()
    # await grpc()


async def http():
    # private keys are loaded from environment variable `PRIVATE_KEY` by default
    # alternatively, can specify the key manually in base58 str if loaded from other source
    # p = provider.HttpProvider("127.0.0.1", 9000, private_key="...")

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


async def do_requests(api: bxserum.Provider):
    # markets API
    # print("fetching all markets")
    # print(await api.get_markets())
    #
    # print("fetching SOL/USDC orderbook")
    # print(await api.get_orderbook(market="SOLUSDC"))
    #
    # print("fetching SOL/USDC ticker")
    # print(await api.get_tickers(market="SOLUSDC"))
    #
    # print("fetching all tickers")
    # print(await api.get_tickers())

    # trade API
    print("fetching open orders for account")
    print(await api.get_open_orders(market="SOLUSDC", address=PUBLIC_KEY))

    # TODO
    # print("fetching order by id")
    # print(await api.get_order_by_i_d(market="SOLUSDC", address=PUBLIC_KEY))

    print("fetching unsettled amounts")
    print(await api.get_unsettled(market="SOLUSDC", owner=PUBLIC_KEY))

    print("generating unsigned order to sell 0.1 SOL for USDC at 150_000 USD/SOL")
    print(
        await api.post_order(
            owner_address=PUBLIC_KEY,
            payer_address=PUBLIC_KEY,
            market="SOLUSDC",
            side=proto.Side.S_ASK,
            type=[proto.OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            open_orders_address="",  # optional
            client_order_i_d=0,  # optional
        )
    )

    print(
        "submitting order (generate + sign) to sell 0.1 SOL for USDC at 150_000 USD/SOL"
    )
    print(
        await api.submit_order(
            owner_address=PUBLIC_KEY,
            payer_address=PUBLIC_KEY,
            market="SOLUSDC",
            side=proto.Side.S_ASK,
            types=[proto.OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            open_orders_address="",  # optional
            client_order_id=0,  # optional
        )
    )

    print("generate cancel order")
    print(
        await api.post_cancel_order(
            order_i_d="",
            side=proto.Side.S_ASK,
            market="SOLUSDC",
            owner=PUBLIC_KEY,
            open_orders="",  # optional
        )
    )

    print("submit cancel order")
    # TODO
    # print(
    #     await api.post_cancel_order(
    #         order_i_d="",
    #         side=proto.Side.S_ASK,
    #         market="SOLUSDC",
    #         owner=PUBLIC_KEY,
    #         open_orders="",  # optional
    #     )
    # )

    print("generate cancel order by client ID")
    print(
        await api.post_cancel_order_by_client_i_d(
            client_i_d=123,
            market="SOLUSDC",
            owner=PUBLIC_KEY,
            open_orders="",  # optional
        )
    )

    print("submit cancel order by client ID")
    # TODO
    # print(
    #     await api.post_cancel_order(
    #         order_i_d="",
    #         side=proto.Side.S_ASK,
    #         market="SOLUSDC",
    #         owner=PUBLIC_KEY,
    #         open_orders="",  # optional
    #     )
    # )


async def do_stream(api: bxserum.Api):
    pass

    # print("checking stream...")
    # async for response in api.get_orderbook_stream(market="SOLUSDC"):
    #    print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
