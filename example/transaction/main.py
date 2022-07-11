import asyncio
import os
import random

import async_timeout

from bxserum import proto, provider
from bxserum.transaction import signing

public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
open_orders = os.getenv("OPEN_ORDERS")
base_token_wallet = os.getenv("BASE_TOKEN_WALLET")
quote_token_wallet = os.getenv("QUOTE_TOKEN_WALLET")

stream_expect_timeout = 60

market_addr = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"  # SOL/USDC
order_side = proto.Side.S_ASK
order_type = proto.OrderType.OT_LIMIT
order_price = 170200
order_amount = 0.1


async def main():
    await ws()
    await grpc()


async def ws():
    print("*** WS Test ***\n")
    async with provider.ws() as api:
        async with provider.ws() as api2:  # TODO use same provider when WS streams are separated
            await order_lifecycle(api, api2)


async def grpc():
    print("*** GRPC Test ***\n")
    async with provider.grpc() as api:
        await order_lifecycle(api, api)


async def order_lifecycle(p1: provider.Provider, p2: provider.Provider):
    oss = p2.get_order_status_stream(market=market_addr, owner_address=public_key)
    task = asyncio.create_task(oss.__anext__())

    await asyncio.sleep(10)

    # Place Order => `Open`
    client_order_id = await place_order(p1)
    try:
        async with async_timeout.timeout(stream_expect_timeout):
            response = await task
            if response.order_info.order_status == proto.OrderStatus.OS_OPEN:
                print("order went to orderbook (`OPEN`) successfully")
            else:
                print(
                    "order should be `OPEN` but is "
                    + response.order_info.order_status.__str__()
                )
    except asyncio.TimeoutError:
        raise Exception("no updates after placing order")
    print()

    await asyncio.sleep(10)

    # Cancel Order => `Cancelled`
    await cancel_order(p1, client_order_id)
    try:
        async with async_timeout.timeout(stream_expect_timeout):
            response = await oss.__anext__()
            if response.order_info.order_status == proto.OrderStatus.OS_CANCELLED:
                print("order cancelled (`CANCELLED`) successfully")
            else:
                print(
                    "order should be `CANCELLED` but is "
                    + response.order_info.order_status.__str__()
                )
    except asyncio.TimeoutError:
        raise Exception("no updates after cancelling order")
    print()

    # Settle Funds
    await settle_funds(p1)
    print()


async def place_order(p: provider.Provider) -> int:
    print("starting place order")

    client_order_id = random.randint(0, 1000000)
    post_order_response = await p.post_order(
        owner_address=public_key,
        payer_address=public_key,
        market=market_addr,
        side=order_side,
        type=[order_type],
        amount=order_amount,
        price=order_price,
        open_orders_address=open_orders,
        client_order_i_d=client_order_id,
    )
    print("place order transaction created successfully")

    signed_tx = signing.sign_tx(post_order_response.transaction)

    post_submit_response = await p.post_submit(
        transaction=signed_tx, skip_pre_flight=True
    )
    print(
        f"placing order with clientOrderID {client_order_id.__str__()}, response signature: {post_submit_response.signature}"
    )

    return client_order_id


async def cancel_order(p: provider.Provider, client_order_id: int):
    print("starting cancel order")

    cancel_order_response = await p.post_cancel_by_client_order_i_d(
        client_order_i_d=client_order_id,
        market_address=market_addr,
        owner_address=public_key,
        open_orders_address=open_orders,
    )
    print("cancel order transaction created successfully")

    signed_tx = signing.sign_tx(cancel_order_response.transaction)

    post_submit_response = await p.post_submit(
        transaction=signed_tx, skip_pre_flight=True
    )
    print(
        f"cancelling order with clientOrderID {client_order_id.__str__()}, response signature: {post_submit_response.signature}"
    )


async def settle_funds(p: provider.Provider):
    print("starting settle funds")

    post_settle_response = await p.post_settle(
        owner_address=public_key,
        market=market_addr,
        base_token_wallet=base_token_wallet,
        quote_token_wallet=quote_token_wallet,
        open_orders_address=open_orders,
    )
    print("settle transaction created successfully")

    signed_settle_tx = signing.sign_tx(post_settle_response.transaction)

    post_submit_response = await p.post_submit(
        transaction=signed_settle_tx, skip_pre_flight=True
    )
    print("settling funds, response signature: " + post_submit_response.signature)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
