import asyncio
import os
import random
import time
import typing
from bxserum.transaction import signing
import async_timeout

from bxserum import provider, proto

public_key=os.getenv("PUBLIC_KEY")
private_key=os.getenv("PRIVATE_KEY")
open_orders=os.getenv("OPEN_ORDERS")

market="SOL/USDC"
stream_expect_timeout = 30

marketAddr = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"
orderSide   = proto.Side.S_ASK
orderType   = proto.OrderType.OT_LIMIT
orderPrice  = 170200
orderAmount = 0.1

baseTokenWallet = "F75gCEckFAyeeCWA9FQMkmLCmke7ehvBnZeVZ3QgvJR7"
quoteTokenWallet = "4raJjCwLLqw8TciQXYruDEF4YhDkGwoEnwnAdwJSjcgv"


async def main():
    await ws()
    #await grpc()

async def ws():
    async with provider.ws() as api:
        await order_lifecycle(api)

async def grpc():
    async with provider.grpc() as api:
        await order_lifecycle(api)

async def order_lifecycle(p: provider.Provider):
    oss = p.get_order_status_stream(market=market, owner_address=public_key)

    await asyncio.sleep(10)

    client_order_id = await place_order(p)
    try:
        async with async_timeout.timeout(stream_expect_timeout):
            response = await oss.__anext__()
            if response.order_info.order_status == proto.OrderStatus.OS_OPEN:
                print("order went to orderbook (`OPEN`) successfully")
            else:
                print("order should be `OPEN` but is " + response.order_info.order_status.__str__())
    except asyncio.TimeoutError:
        raise Exception("no updates after placing order")

    await asyncio.sleep(10)

    await cancel_order(p, client_order_id)
    try:
        async with async_timeout.timeout(stream_expect_timeout):
            response = await oss.__anext__()
            if response.order_info.order_status == proto.OrderStatus.OS_CANCELLED:
                print("order cancelled (`CANCELLED`) successfully")
            else:
                print("order should be `CANCELLED` but is " + response.order_info.order_status.__str__())
    except asyncio.TimeoutError:
        raise Exception("no updates after cancelling order")

    await settle_funds(p)

async def place_order(p: provider.Provider) -> int:
    print("starting place order")
    client_order_id = random.randint(0, 1000000)

    post_order_response = await p.post_order(owner_address=public_key, payer_address=public_key, market=marketAddr, side=orderSide,
                       type=[orderType], amount=orderAmount, price=orderPrice, open_orders_address=open_orders,
                       client_order_i_d=client_order_id)
    print("unsigned place order transaction " + post_order_response.transaction.__str__())

    signed_tx = signing.sign_tx(post_order_response.transaction)

    post_submit_response = await p.post_submit(transaction=signed_tx, skip_pre_flight=True)
    print("placed order " + post_submit_response.signature + " with clientOrderID " + client_order_id.__str__())

    return client_order_id

async def cancel_order(p: provider.Provider, client_order_id: int):
    print("starting cancel order")
    cancel_order_response = await p.post_cancel_by_client_order_i_d(client_order_i_d=client_order_id, market_address=marketAddr,
                                            owner_address=public_key, open_orders_address=open_orders)

    signed_cancel_tx = signing.sign_tx(cancel_order_response.transaction)
    await p.post_submit(transaction=signed_cancel_tx, skip_pre_flight=True)

    print("cancelled order for clientID " + client_order_id.__str__())

async def settle_funds(p: provider.Provider):
    print("starting settle funds")
    post_settle_response = await p.post_settle(owner_address=public_key, market=marketAddr, base_token_wallet=baseTokenWallet, quote_token_wallet=quoteTokenWallet, open_orders_address=open_orders)
    print("settle transaction created successfully")

    signed_settle_tx = signing.sign_tx(post_settle_response.transaction)

    post_submit_response = await p.post_submit(transaction=signed_settle_tx, skip_pre_flight=True)
    print("response signature for settle received: " + post_submit_response.signature)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
