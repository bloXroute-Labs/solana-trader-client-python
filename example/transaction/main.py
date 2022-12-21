import asyncio
import os

from bxsolana_trader_proto import api as proto
from bxsolana import provider
from bxsolana import examples

# TODO: Add some logic here to indicate to user if missing needed environment variables for tests
public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
open_orders = os.getenv("OPEN_ORDERS")
base_token_wallet = os.getenv("BASE_TOKEN_WALLET")
quote_token_wallet = os.getenv("QUOTE_TOKEN_WALLET")

market_addr = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"  # SOL/USDC
order_side = proto.Side.S_ASK
order_type = proto.OrderType.OT_LIMIT
order_price = 170200
order_amount = 0.1


async def main():
    await ws()
    await grpc()
    await http()


async def ws():
    print("\n*** WS Test ***\n")
    async with provider.ws() as api:
        async with provider.ws() as api2:  # TODO use same provider when WS streams are separated
            await examples.order_lifecycle(
                p1=api,
                p2=api2,
                owner_addr=public_key,
                payer_addr=public_key,
                market_addr=market_addr,
                order_side=order_side,
                order_type=order_type,
                order_amount=order_amount,
                order_price=order_price,
                open_orders_addr=open_orders,
                base_token_wallet=base_token_wallet,
                quote_token_wallet=quote_token_wallet,
            )

            await examples.cancel_all_orders(
                api,
                owner_addr=public_key,
                payer_addr=public_key,
                order_side=order_side,
                order_type=order_type,
                order_amount=order_amount,
                order_price=order_price,
                open_orders_addr=open_orders,
                market_addr=market_addr,
            )

            await examples.replace_order_by_client_order_i_d(
                api,
                owner_addr=public_key,
                payer_addr=public_key,
                market_addr=market_addr,
                order_side=order_side,
                order_type=order_type,
                order_amount=order_amount,
                order_price=order_price,
                open_orders_addr=open_orders,
            )


async def grpc():
    print("\n*** GRPC Test ***\n")
    async with provider.grpc() as api:
        await examples.order_lifecycle(
            p1=api,
            p2=api,
            owner_addr=public_key,
            payer_addr=public_key,
            market_addr=market_addr,
            order_side=order_side,
            order_type=order_type,
            order_amount=order_amount,
            order_price=order_price,
            open_orders_addr=open_orders,
            base_token_wallet=base_token_wallet,
            quote_token_wallet=quote_token_wallet,
        )

        await examples.cancel_all_orders(
            api,
            owner_addr=public_key,
            payer_addr=public_key,
            order_side=order_side,
            order_type=order_type,
            order_amount=order_amount,
            order_price=order_price,
            open_orders_addr=open_orders,
            market_addr=market_addr,
        )

        await examples.replace_order_by_client_order_i_d(
            api,
            owner_addr=public_key,
            payer_addr=public_key,
            market_addr=market_addr,
            order_side=order_side,
            order_type=order_type,
            order_amount=order_amount,
            order_price=order_price,
            open_orders_addr=open_orders,
        )


async def http():
    print("\n*** HTTP Test ***\n")
    async with provider.http() as api:
        await examples.cancel_all_orders(
            api,
            owner_addr=public_key,
            payer_addr=public_key,
            order_side=order_side,
            order_type=order_type,
            order_amount=order_amount,
            order_price=order_price,
            open_orders_addr=open_orders,
            market_addr=market_addr,
        )

        await examples.replace_order_by_client_order_i_d(
            api,
            owner_addr=public_key,
            payer_addr=public_key,
            market_addr=market_addr,
            order_side=order_side,
            order_type=order_type,
            order_amount=order_amount,
            order_price=order_price,
            open_orders_addr=open_orders,
        )


if __name__ == "__main__":
    asyncio.run(main())
