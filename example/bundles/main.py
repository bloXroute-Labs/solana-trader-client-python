import asyncio
import os

from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import OrderType

from bxsolana.transaction import signing

from bxsolana import provider, examples

# TODO: Add some logic here to indicate to user if missing needed environment variables for tests
public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
open_orders = os.getenv("OPEN_ORDERS")
base_token_wallet = os.getenv("BASE_TOKEN_WALLET")
quote_token_wallet = os.getenv("QUOTE_TOKEN_WALLET")

market_addr = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT"  # SOL/USDC
order_side = proto.Side.S_ASK
order_type = OrderType.OT_LIMIT
order_price = 170200
order_amount = 0.1


async def main():
    # await ws()
    await grpc()
    # await http()


async def ws():
    print("\n*** WS Example using Openbook bundles ***\n")
    async with provider.ws_testnet() as api:
        openbook_bundle_tx = await api.post_order_v2(post_order_request_v2=proto.PostOrderRequestV2(
            owner_address=public_key,
            payer_address=public_key,
            market="SOLUSDC",
            side="ASK",
            amount=0.01,
            price=150_000,
            type="limit",
            tip=1030
            ))

        print(f'created OPENBOOK tx with bundle tip of 1030: {openbook_bundle_tx.transaction.content}')

        signed_tx = signing.sign_tx(openbook_bundle_tx.transaction.content)

        post_submit_response = await api.post_submit(
            post_submit_request=proto.PostSubmitRequest(
                transaction=proto.TransactionMessage(content=signed_tx),
                skip_pre_flight=True,
                front_running_protection=True
            )
        )

        print(f'submitted OPENBOOK tx with front running protection: {openbook_bundle_tx.transaction.content}')

async def grpc():
    print("\n*** GRPC Test ***\n")
    async with provider.grpc_testnet() as api:
        raydium_bundle_tx = await api.post_raydium_swap(proto.PostRaydiumSwapRequest(owner_address=public_key,
                                                                                  in_token="SOL",
                                                                                  out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                                                                  slippage=0.2,
                                                                                  in_amount=0.01,
                                                                                  tip=1030))

        print(f'created RAYDIUM swap tx with bundle tip of 1030: {raydium_bundle_tx.transaction.content}')

        signed_tx = signing.sign_tx(raydium_bundle_tx.transaction.content)

        post_submit_response = await api.post_submit(
            post_submit_request=proto.PostSubmitRequest(
                transaction=proto.TransactionMessage(content=signed_tx),
                skip_pre_flight=True,
                front_running_protection=True
            )
        )

        print(f'submitted RAYDIUM tx with front running protection: {post_submit_response.transaction.content}')

async def http():
    print("\n*** HTTP Test ***\n")
    async with provider.http_testnet() as api:
        raydium_bundle_tx = await api.post_raydium_swap(proto.PostRaydiumSwapRequest(owner_address=public_key,
                                                                                     in_token="SOL",
                                                                                     out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                                                                     slippage=0.2,
                                                                                     in_amount=0.01,
                                                                                     tip=1030))

        print(f'created RAYDIUM swap tx with bundle tip of 1030: {raydium_bundle_tx.transactions[0].content}')

        signed_tx = signing.sign_tx(raydium_bundle_tx.transactions[0].content)

        post_submit_response = await api.post_submit(
            post_submit_request=proto.PostSubmitRequest(
                transaction=proto.TransactionMessage(content=signed_tx),
                skip_pre_flight=True,
                front_running_protection=True
            )
        )

        print(f'submitted RAYDIUM tx with front running protection: {post_submit_response.signature}')

if __name__ == "__main__":
    asyncio.run(main())
