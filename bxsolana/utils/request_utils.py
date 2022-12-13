import bxsolana
from bxsolana_trader_proto import api as proto

from bxsolana.utils.constants import SOL_USDC_MARKET, PUBLIC_KEY, OPEN_ORDERS, ORDER_ID, USDC_WALLET


async def do_requests(api: bxsolana.Provider,
                      public_key: PUBLIC_KEY,
                      open_orders: OPEN_ORDERS,
                      order_id: ORDER_ID,
                      usdc_wallet: USDC_WALLET,
                      sol_usdc_market: SOL_USDC_MARKET):
    # markets API
    print("fetching all markets")
    print((await api.get_markets()).to_json())

    print("fetching SOL/USDC orderbook")
    print((await api.get_orderbook(market="SOLUSDC", project=proto.Project.P_OPENBOOK)).to_json())

    print("fetching SOL/USDC ticker")
    print((await api.get_tickers(market="SOLUSDC", project=proto.Project.P_OPENBOOK)).to_json())

    print("fetching all tickers")
    print((await api.get_tickers(project=proto.Project.P_OPENBOOK)).to_json())

    # trade API
    print("fetching open orders for account")
    print(
        (
            await api.get_open_orders(market="SOLUSDC", address=public_key, project=proto.Project.P_OPENBOOK)
        ).to_json()
    )

    print("fetching unsettled amounts")
    print(
        (
            await api.get_unsettled(market="SOLUSDC", owner_address=public_key, project=proto.Project.P_OPENBOOK)
        ).to_json()
    )

    print("fetching account balance amounts")
    print((await api.get_account_balance(owner_address=public_key)).to_json())

    print(
        "generating unsigned order (no sign or submission) to sell 0.1 SOL for"
        " USDC at 150_000 USD/SOL"
    )
    print(
        (
            await api.post_order(
                owner_address=public_key,
                payer_address=public_key,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[proto.OrderType.OT_LIMIT],
                amount=0.1,
                price=150_000,
                project=proto.Project.P_OPENBOOK,
                # optional, but much faster if known
                open_orders_address=open_orders,
                # optional, for identification
                client_order_i_d=0,
            )
        ).to_json()
    )

    print("generate cancel order")
    print(
        (
            await api.post_cancel_order(
                order_i_d=order_id,
                side=proto.Side.S_ASK,
                market_address="SOLUSDC",
                project=proto.Project.P_OPENBOOK,
                owner_address=public_key,
                open_orders_address=open_orders,
            )
        ).to_json()
    )

    print("generate cancel order by client ID")
    print(
        await api.post_cancel_by_client_order_i_d(
            client_order_i_d=123,
            market_address=sol_usdc_market,
            owner_address=public_key,
            project=proto.Project.P_OPENBOOK,
            open_orders_address=open_orders,
        )
    )

    print("generate settle order")
    print(
        await api.post_settle(
            owner_address=public_key,
            market="SOLUSDC",
            base_token_wallet=public_key,
            quote_token_wallet=usdc_wallet,
            project=proto.Project.P_OPENBOOK,
            open_orders_address=open_orders,
        )
    )

    print(
        (
            await api.post_replace_by_client_order_i_d(
                owner_address=public_key,
                payer_address=public_key,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[proto.OrderType.OT_LIMIT],
                amount=0.1,
                price=150_000,
                project=proto.Project.P_OPENBOOK,
                # optional, but much faster if known
                open_orders_address=open_orders,
                # optional, for identification
                client_order_i_d=123,
            )
        ).to_json()
    )

    print(
        (
            await api.post_replace_order(
                owner_address=public_key,
                payer_address=public_key,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[proto.OrderType.OT_LIMIT],
                amount=0.1,
                price=150_000,
                project=proto.Project.P_OPENBOOK,
                # optional, but much faster if known
                open_orders_address=open_orders,
                # optional, for identification
                client_order_i_d=0,
                order_i_d=order_id,
            )
        ).to_json()
    )