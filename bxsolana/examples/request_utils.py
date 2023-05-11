from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import OrderType
from bxsolana_trader_proto.common import PerpPositionSide
from bxsolana_trader_proto.common import PerpOrderType
from bxsolana_trader_proto.common import PerpContract
from bxsolana_trader_proto.common import PerpCollateralType
from bxsolana_trader_proto.common import PerpCollateralToken
from bxsolana_trader_proto.common import PostOnlyParams

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
    return
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

    print("fetching token accounts and balances")
    print((await api.get_token_accounts(owner_address=public_key)).to_json())

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
    if order_id != "":
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
    if order_id != "":
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

    # DRIFT
    print("post Drift margin trading flag")
    print(
        (
            await api.post_drift_enable_margin_trading(
                owner_address=public_key, enable_margin=True
            )
        ).to_json()
    )

    print("post Drift Margin order")
    print(
        (
            await api.post_drift_margin_order(
                owner_address=public_key,
                market="SOL",
                position_side="LONG",
                slippage=10,
                type="MARKET",  # or Limit
                amount=10,
                client_order_i_d=12,
                post_only=PostOnlyParams.PO_NONE,
            )
        ).to_json()
    )

    print("get Drift markets")
    print((await api.get_drift_markets(metadata=True)).to_json())

    print("get Drift margin orderbook")
    print(
        (
            await api.get_drift_margin_orderbook(
                market="SOL", limit=2, metadata=True
            )
        ).to_json()
    )

    print("get user")
    print(
        (
            await api.get_user(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
            )
        ).to_json()
    )

    print("get Drift orderbook")
    print(
        (
            await api.get_perp_orderbook(
                contract=PerpContract.SOL_PERP, project=proto.Project.P_DRIFT
            )
        ).to_json()
    )

    print("post perp order")
    print(
        (
            await api.post_perp_order(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                payer_address=public_key,
                contract=PerpContract.SOL_PERP,
                position_side=PerpPositionSide.PS_LONG,
                slippage=0,
                type=PerpOrderType.POT_LIMIT,
                amount=0,
                price=12000,
                client_order_i_d=12,
            )
        ).to_json()
    )

    print("get perp contracts")
    print(
        (
            await api.get_perp_contracts(
                project=proto.Project.P_DRIFT,
            )
        ).to_json()
    )

    print("get perp assets")
    print(
        (
            await api.get_assets(
                owner_address=public_key,
                project=proto.Project.P_DRIFT,
            )
        ).to_json()
    )

    print("get open perp order")
    print(
        (
            await api.get_open_perp_order(
                owner_address=public_key,
                project=proto.Project.P_DRIFT,
                contract=PerpContract.SOL_PERP,
                client_order_i_d=12,
            )
        ).to_json()
    )

    print("get open perp orders")
    print(
        (
            await api.get_open_perp_orders(
                owner_address=public_key,
                project=proto.Project.P_DRIFT,
                contracts=[PerpContract.SOL_PERP, PerpContract.BTC_PERP],
            )
        ).to_json()
    )

    print("post liquidate perp")
    print(
        (
            await api.post_liquidate_perp(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                settlee_account_address=(
                    "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                ),
                contract=PerpContract.SOL_PERP,
                amount=1,
            )
        ).to_json()
    )

    print("post settle pnl")
    print(
        (
            await api.post_settle_p_n_l(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                settlee_account_address=(
                    "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                ),
                contract=PerpContract.SOL_PERP,
            )
        ).to_json()
    )

    print("post settle pnls")
    print(
        (
            await api.post_settle_p_n_ls(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                settlee_account_addresses=[
                    "9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS"
                ],
                contract=PerpContract.SOL_PERP,
            )
        ).to_json()
    )

    print("post cancel perp order")
    print(
        (
            await api.post_cancel_perp_order(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                client_order_i_d=12,
                order_i_d=0,
                contract=PerpContract.SOL_PERP,
            )
        ).to_json()
    )

    print("post close perp orders")
    print(
        (
            await api.post_close_perp_positions(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                contracts=[PerpContract.SOL_PERP],
            )
        ).to_json()
    )

    print("post cancel perp orders")
    print(
        (
            await api.post_cancel_perp_orders(
                project=proto.Project.P_DRIFT,
                contract=PerpContract.SOL_PERP,
                owner_address=public_key,
            )
        ).to_json()
    )

    print("post create user")
    print(
        (
            await api.post_create_user(
                project=proto.Project.P_DRIFT,
                owner_address="BgJ8uyf9yhLJaUVESRrqffzwVyQgRi9YvWmpEFaH14kx",
            )
        ).to_json()
    )

    print("post deposit collateral")
    print(
        (
            await api.post_manage_collateral(
                project=proto.Project.P_DRIFT,
                account_address="9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS",
                amount=0.1,
                token=PerpCollateralToken.PCTK_USDC,
                type=PerpCollateralType.PCT_DEPOSIT,
            )
        ).to_json()
    )

    print("post withdraw collateral")
    print(
        (
            await api.post_manage_collateral(
                project=proto.Project.P_DRIFT,
                account_address="9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS",
                amount=0.1,
                token=PerpCollateralToken.PCTK_SOL,
                type=PerpCollateralType.PCT_WITHDRAWAL,
            )
        ).to_json()
    )

    print("post transfer collateral")
    print(
        (
            await api.post_manage_collateral(
                project=proto.Project.P_DRIFT,
                account_address="9UnwdvTf5EfGeLyLrF4GZDUs7LKRUeJQzW7qsDVGQ8sS",
                amount=0.1,
                token=PerpCollateralToken.PCTK_SOL,
                type=PerpCollateralType.PCT_TRANSFER,
                to_account_address=(
                    "AbnwAQGrYnvktT4ihhX5np8RbgtfXJfPwpgMJnCFa4MT"
                ),
            )
        ).to_json()
    )

    print("get perp positions")
    print(
        (
            await api.get_perp_positions(
                project=proto.Project.P_DRIFT,
                owner_address=public_key,
                contracts=[PerpContract.SOL_PERP],
            )
        ).to_json()
    )
