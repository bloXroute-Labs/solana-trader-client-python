import random
import time

from bxsolana_trader_proto import api as proto

from bxsolana import provider
from bxsolana.transaction import signing

crank_timeout = 60


async def place_order(
    p: provider.Provider,
    owner_addr,
    payer_addr,
    market_addr,
    order_side,
    order_type,
    order_amount,
    order_price,
    open_orders_addr,
) -> int:
    print("starting place order")

    client_order_id = random.randint(0, 1000000)
    post_order_response = await p.post_order(
        post_order_request=proto.PostOrderRequest(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market_addr,
            side=order_side,
            type=[order_type],
            amount=order_amount,
            price=order_price,
            open_orders_address=open_orders_addr,
            client_order_id=client_order_id,
        )
    )
    print("place order transaction created successfully")

    signed_tx = signing.sign_tx(post_order_response.transaction.content)

    post_submit_response = await p.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(content=signed_tx),
            skip_pre_flight=True,
        )
    )

    print(
        f"placing order with clientOrderID {client_order_id.__str__()},"
        f" response signature: {post_submit_response.signature}"
    )

    return client_order_id


async def place_order_with_tip(
    p: provider.Provider,
    owner_addr,
    payer_addr,
    market_addr,
    order_side,
    order_type,
    order_amount,
    order_price,
    open_orders_addr,
) -> int:
    print("starting place order")

    client_order_id = random.randint(0, 1000000)
    post_order_response = await p.post_order(
        post_order_request=proto.PostOrderRequest(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market_addr,
            side=order_side,
            type=[order_type],
            amount=order_amount,
            price=order_price,
            open_orders_address=open_orders_addr,
            client_order_id=client_order_id,
            tip=1030,
        )
    )
    print("place order transaction created successfully")

    signed_tx = signing.sign_tx(post_order_response.transaction.content)

    post_submit_response = await p.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(content=signed_tx),
            skip_pre_flight=True,
            front_running_protection=True,
            use_staked_rp_cs=True,
        )
    )

    print(
        f"placing order with clientOrderID {client_order_id.__str__()},"
        f" response signature: {post_submit_response.signature}"
    )

    return client_order_id


async def cancel_order(
    p: provider.Provider,
    client_order_id: int,
    market_addr: str,
    owner_addr: str,
    open_orders_addr: str,
):
    print("starting cancel order")

    cancel_order_response = await p.post_cancel_by_client_order_id(
        post_cancel_by_client_order_id_request=proto.PostCancelByClientOrderIdRequest(
            client_order_id=client_order_id,
            market_address=market_addr,
            owner_address=owner_addr,
            open_orders_address=open_orders_addr,
        )
    )
    print("cancel order transaction created successfully")

    signed_tx = signing.sign_tx(cancel_order_response.transaction.content)

    post_submit_response = await p.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(content=signed_tx),
            skip_pre_flight=True,
        )
    )
    print(
        f"cancelling order with clientOrderID {client_order_id.__str__()},"
        f" response signature: {post_submit_response.signature}"
    )


async def settle_funds(
    p: provider.Provider,
    owner_addr: str,
    market_addr: str,
    base_token_wallet: str,
    quote_token_wallet: str,
    open_orders_addr: str,
):
    print("starting settle funds")

    post_settle_response = await p.post_settle(
        post_settle_request=proto.PostSettleRequest(
            owner_address=owner_addr,
            market=market_addr,
            base_token_wallet=base_token_wallet,
            quote_token_wallet=quote_token_wallet,
            open_orders_address=open_orders_addr,
        )
    )
    print("settle transaction created successfully")

    signed_settle_tx = signing.sign_tx(post_settle_response.transaction.content)

    post_submit_response = await p.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(content=signed_settle_tx),
            skip_pre_flight=True,
        )
    )

    print(
        "settling funds, response signature: " + post_submit_response.signature
    )


async def cancel_all_orders(
    p: provider.Provider,
    owner_addr,
    payer_addr,
    order_side,
    order_type,
    order_amount,
    order_price,
    open_orders_addr,
    market_addr,
):
    print("cancel all test\n")

    print("placing order #1")
    client_order_id_1 = await place_order(
        p,
        owner_addr,
        payer_addr,
        market_addr,
        order_side,
        order_type,
        order_amount,
        order_price,
        open_orders_addr,
    )
    print()

    print("placing order #2")
    client_order_id_2 = await place_order(
        p,
        owner_addr,
        payer_addr,
        market_addr,
        order_side,
        order_type,
        order_amount,
        order_price,
        open_orders_addr,
    )
    print()

    print(f"waiting {crank_timeout}s for place orders to be cranked")
    time.sleep(crank_timeout)

    o = await p.get_open_orders(
        get_open_orders_request=proto.GetOpenOrdersRequest(
            market=market_addr, address=owner_addr
        )
    )
    found1 = False
    found2 = False

    for order in o.orders:
        if order.client_order_id == str(client_order_id_1):
            found1 = True
        elif order.client_order_id == str(client_order_id_2):
            found2 = True

    if not found1 or not found2:
        raise Exception("one/both orders not found in orderbook")
    print("2 orders placed successfully\n")

    await cancel_all(p, owner_addr, open_orders_addr, market_addr)

    print(f"\nwaiting {crank_timeout}s for cancel order(s) to be cranked")
    time.sleep(crank_timeout)

    o = await p.get_open_orders(
        get_open_orders_request=proto.GetOpenOrdersRequest(
            market=market_addr, address=owner_addr
        )
    )
    if len(o.orders) != 0:
        print(f"{len(o.orders)} orders in orderbook not cancelled")
    else:
        print("orders in orderbook cancelled")
    print()


async def cancel_all(
    p: provider.Provider, owner_addr, open_orders_addr, market_addr
):
    print("starting cancel all")

    open_orders_addresses = [""]
    if open_orders_addresses is None:
        open_orders_addresses.append(open_orders_addr)

    cancel_all_response = await p.post_cancel_all(
        post_cancel_all_request=proto.PostCancelAllRequest(
            market=market_addr,
            owner_address=owner_addr,
            open_orders_addresses=open_orders_addresses,
        )
    )
    print("cancel all transaction created successfully")

    signatures = []
    for transaction in cancel_all_response.transactions:
        signed_tx = signing.sign_tx(transaction.content)
        post_submit_response = await p.post_submit(
            post_submit_request=proto.PostSubmitRequest(
                transaction=proto.TransactionMessage(content=signed_tx),
                skip_pre_flight=True,
            )
        )
        signatures.append(post_submit_response.signature)

    signatures_string = ", ".join(signatures)
    print(f"cancelling all orders, response signature(s): {signatures_string}")


async def replace_order_by_client_order_id(
    p: provider.Provider,
    owner_addr,
    payer_addr,
    market_addr,
    order_side,
    order_type,
    order_amount,
    order_price,
    open_orders_addr,
) -> int:
    print("starting replace order by client order ID")

    client_order_id = random.randint(0, 1000000)
    post_order_response = await p.post_replace_by_client_order_id(
        post_order_request=proto.PostOrderRequest(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market_addr,
            side=order_side,
            type=[order_type],
            amount=order_amount,
            price=order_price,
            open_orders_address=open_orders_addr,
            client_order_id=client_order_id,
        )
    )
    print("replace order transaction created successfully")

    signed_tx = signing.sign_tx(post_order_response.transaction.content)

    post_submit_response = await p.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(content=signed_tx),
            skip_pre_flight=True,
        )
    )
    print(
        f"replacing order with clientOrderID {client_order_id.__str__()},"
        f" response signature: {post_submit_response.signature}"
    )

    return client_order_id
