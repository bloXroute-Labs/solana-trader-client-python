import asyncio

import bxserum
from bxserum import provider, proto

# sample public key for trades API
PUBLIC_KEY = "AFT8VayE7qr8MoQsW3wHsDS83HhEvhGWdbNSHRKeUDfQ"
USDC_WALLET = "3wYEfi36o9fEzq4L36JN4rcwf3uDmQMcKexoQ8kwSrUR"


async def main():
    await http()
    await ws()
    await grpc()


async def http():
    # private keys are loaded from environment variable `PRIVATE_KEY` by default
    # alternatively, can specify the key manually in base58 str if loaded from other source
    # p = provider.HttpProvider("127.0.0.1", 9000, private_key="...")

    p = provider.http()
    api = await bxserum.serum(p)

    # either `try`/`finally` or `async with` work with each type of provider
    try:
        await do_requests(api)
    except Exception as e:
        print(e)
    finally:
        await p.close()


async def ws():
    async with provider.ws() as api:
        await do_requests(api)
        await do_stream(api)


async def grpc():
    p = provider.grpc()
    api = await bxserum.serum(p)

    try:
        await do_requests(api)
        await do_stream(api)
    finally:
        await p.close()


async def do_requests(api: bxserum.Provider):
    # markets API
    print("fetching all markets")
    print((await api.get_markets()).to_json())

    print("fetching SOL/USDC orderbook")
    print((await api.get_orderbook(market="SOLUSDC")).to_json())

    print("fetching SOL/USDC ticker")
    print((await api.get_tickers(market="SOLUSDC")).to_json())

    print("fetching all tickers")
    print((await api.get_tickers()).to_json())

    # trade API
    print("fetching open orders for account")
    print((await api.get_open_orders(market="SOLUSDC", address=PUBLIC_KEY)).to_json())

    print("fetching unsettled amounts")
    print((await api.get_unsettled(market="SOLUSDC", owner=PUBLIC_KEY)).to_json())

    print("fetching account balance amounts")
    print((await api.get_account_balance(owner_address=PUBLIC_KEY)).to_json())

    print(
        "generating unsigned order (no sign or submission) to sell 0.1 SOL for USDC at "
        "150_000 USD/SOL"
    )
    print(
        (
            await api.post_order(
                owner_address=PUBLIC_KEY,
                payer_address=PUBLIC_KEY,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[proto.OrderType.OT_LIMIT],
                amount=0.1,
                price=150_000,
                # optional, but much faster if known
                open_orders_address="5yyh4mzzycmjfR6arY736d1mB6vNSLiUaFWfepKLf8kZ",
                # optional, for identification
                client_order_i_d=0,
            )
        ).to_json()
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
            # optional, but much faster if known
            open_orders_address="5yyh4mzzycmjfR6arY736d1mB6vNSLiUaFWfepKLf8kZ",
            # optional, for identification
            client_order_id=0,
        )
    )

    print("generate cancel order")
    print(
        (
            await api.post_cancel_order(
                order_i_d="",
                side=proto.Side.S_ASK,
                market_address="SOLUSDC",
                owner_address=PUBLIC_KEY,
                open_orders_address="",  # optional
            )
        ).to_json()
    )

    print("submit cancel order")
    print(
        await api.submit_cancel_order(
            order_i_d="",
            side=proto.Side.S_ASK,
            market_address="SOLUSDC",
            owner_address=PUBLIC_KEY,
            open_orders_address="",  # optional
        )
    )

    print("generate cancel order by client ID")
    print(
        await api.post_cancel_by_client_order_i_d(
            client_order_i_d=123,
            market_address="9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT",
            owner_address=PUBLIC_KEY,
            open_orders_address="",  # optional
        )
    )

    print("submit cancel order by client ID")
    print(
        await api.submit_cancel_by_client_order_i_d(
            client_order_i_d=123,
            market_address="9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT",
            owner_address=PUBLIC_KEY,
            open_orders_address="",  # optional
        )
    )

    print("generate settle order")
    print(
        await api.post_settle(
            owner_address=PUBLIC_KEY,
            market="SOLUSDC",
            base_token_wallet=PUBLIC_KEY,
            quote_token_wallet=USDC_WALLET,
            open_orders_address="",  # optional
        )
    )

    print("submit settle order")
    print(
        await api.submit_settle(
            owner_address=PUBLIC_KEY,
            market="SOLUSDC",
            base_token_wallet=PUBLIC_KEY,
            quote_token_wallet=USDC_WALLET,
            open_orders_address="",  # optional
        )
    )


# websockets / GRPC only
async def do_stream(api: bxserum.Provider):
    item_count = 0

    print("streaming orderbook updates...")
    async for response in api.get_orderbooks_stream(market="SOLUSDC"):
        print(response.to_json())
        item_count += 1
        if item_count == 5:
            item_count = 0
            break

    print("streaming filtered orderbook updates...")
    async for response in api.get_filtered_orderbooks_stream(markets=["SOL/USDC"]):
        print(response.to_json())
        item_count += 1
        if item_count == 5:
            item_count = 0
            break

    print("streaming ticker updates...")
    async for response in api.get_tickers_stream(market="SOLUSDC"):
        print(response.to_json())
        item_count += 1
        if item_count == 5:
            item_count = 0
            break

    print("streaming trade updates...")
    async for response in api.get_trades_stream(market="SOLUSDC"):
        print(response.to_json())
        item_count += 1
        if item_count == 5:
            item_count = 0
            break


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
