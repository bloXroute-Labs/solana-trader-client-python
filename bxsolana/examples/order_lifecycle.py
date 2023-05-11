import asyncio
import async_timeout

from bxsolana import provider
from bxsolana_trader_proto import api as proto
from .order_utils import cancel_order, place_order, settle_funds

crank_timeout = 60


async def order_lifecycle(
    p1: provider.Provider,
    p2: provider.Provider,
    owner_addr,
    payer_addr,
    market_addr,
    order_side,
    order_type,
    order_amount,
    order_price,
    open_orders_addr,
    base_token_wallet,
    quote_token_wallet,
):
    print("order lifecycle test\n")

    oss = p2.get_order_status_stream(
        get_order_status_stream_request=proto.GetOrderStatusStreamRequest(
            market=market_addr, owner_address=owner_addr
        )
    )

    # pyre-ignore[6]:
    task = asyncio.create_task(oss.__anext__())
    await asyncio.sleep(10)

    # Place Order => `Open`
    client_order_id = await place_order(
        p1,
        owner_addr,
        payer_addr,
        market_addr,
        order_side,
        order_type,
        order_amount,
        order_price,
        open_orders_addr,
    )
    try:
        print(f"waiting {crank_timeout}s for place order to be cranked")
        async with async_timeout.timeout(crank_timeout):
            response = await task
            if response.order_info.order_status == proto.OrderStatus.OS_OPEN:
                print("order went to orderbook (`OPEN`) successfully")
            else:
                print(
                    "order should be `OPEN` but is "
                    + response.order_info.order_status.__str__()  # noqa: W503
                )
    except asyncio.TimeoutError:
        raise Exception("no updates after placing order")
    print()

    await asyncio.sleep(10)

    # Cancel Order => `Cancelled`
    await cancel_order(
        p1, client_order_id, market_addr, owner_addr, open_orders_addr
    )
    try:
        print(f"waiting {crank_timeout}s for cancel order to be cranked")
        async with async_timeout.timeout(crank_timeout):
            response = await oss.__anext__()
            if (
                response.order_info.order_status
                == proto.OrderStatus.OS_CANCELLED  # noqa: W503
            ):
                print("order cancelled (`CANCELLED`) successfully")
            else:
                print(
                    "order should be `CANCELLED` but is "
                    + response.order_info.order_status.__str__()  # noqa: W503
                )
    except asyncio.TimeoutError:
        raise Exception("no updates after cancelling order")
    print()

    # Settle Funds
    await settle_funds(
        p1,
        owner_addr,
        market_addr,
        base_token_wallet,
        quote_token_wallet,
        open_orders_addr,
    )
    print()
