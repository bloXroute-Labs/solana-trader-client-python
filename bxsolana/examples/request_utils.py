from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import OrderType

from .. import provider


async def do_requests(
    api: provider.Provider,
    public_key: str,
    open_orders: str,
    order_id: str,
    usdc_wallet: str,
    sol_usdc_market: str,
):
    print("fetching market depth")
    print(
        (
            await api.get_market_depth(
                limit=1, market="SOLUSDC", project=proto.Project.P_OPENBOOK
            )
        ).to_json()
    )

    # markets API
    print("fetching all markets")
    print((await api.get_markets()).to_json())

    print("fetching SOL/USDC orderbook")
    print(
        (
            await api.get_orderbook(
                market="SOLUSDC", project=proto.Project.P_OPENBOOK
            )
        ).to_json()
    )

    print("fetching SOL/USDC ticker")
    print(
        (
            await api.get_tickers(
                market="SOLUSDC", project=proto.Project.P_OPENBOOK
            )
        ).to_json()
    )

    print("fetching all tickers")
    print((await api.get_tickers(project=proto.Project.P_OPENBOOK)).to_json())

    print("fetching prices")
    print(
        (
            await api.get_price(
                tokens=[
                    "So11111111111111111111111111111111111111112",
                    "USDC",
                    "SOL",
                    "USDT",
                ]
            )
        ).to_json()
    )

    print("fetching pools")
    print((await api.get_pools(projects=[proto.Project.P_RAYDIUM])).to_json())

    print("fetching quotes")
    print(
        (
            await api.get_quotes(
                in_token="USDC",
                out_token="SOL",
                in_amount=0.01,
                slippage=10,
                limit=1,
                projects=[proto.Project.P_RAYDIUM],
            )
        ).to_json()
    )

    # trade API
    print("fetching open orders for account")
    print(
        (
            await api.get_open_orders(
                market="SOLUSDC",
                address=public_key,
                project=proto.Project.P_OPENBOOK,
            )
        ).to_json()
    )

    print("fetching unsettled amounts")
    print(
        (
            await api.get_unsettled(
                market="SOLUSDC",
                owner_address=public_key,
                project=proto.Project.P_OPENBOOK,
            )
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
                type=[OrderType.OT_LIMIT],
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

    print("generate replace by client order id")
    print(
        (
            await api.post_replace_by_client_order_i_d(
                owner_address=public_key,
                payer_address=public_key,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[OrderType.OT_LIMIT],
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

    print("generate replace by order id")
    print(
        (
            await api.post_replace_order(
                owner_address=public_key,
                payer_address=public_key,
                market="SOLUSDC",
                side=proto.Side.S_ASK,
                type=[OrderType.OT_LIMIT],
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

    print("generate trade swap")
    print(
        (
            await api.post_trade_swap(
                project=proto.Project.P_RAYDIUM,
                owner_address=public_key,
                in_token="SOL",
                in_amount=0.01,
                out_token="USDC",
                slippage=0.01,
            )
        )
    )

    print("generate route swap")
    step = proto.RouteStep(
        in_token="USDC",
        in_amount=0.01,
        out_token="SOL",
        out_amount=0.01,
        out_amount_min=0.01,
        project=proto.StepProject(label="Raydium"),
    )
    print(
        (
            await api.post_route_trade_swap(
                project=proto.Project.P_RAYDIUM,
                owner_address=public_key,
                steps=[step],
            )
        ).to_json()
    )

    #     DRIFT
    print("get Drift orderbook")
    print(
        (
            await api.get_perp_orderbook(
                market="SOL-PERP", project=proto.Project.P_DRIFT
            )
        ).to_json()
    )
