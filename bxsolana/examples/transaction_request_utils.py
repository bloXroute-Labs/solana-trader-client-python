import base64
import random
import sys
from typing import Tuple

from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import OrderType
from solders import hash as hs

from .. import provider
from .. import transaction


# if you run this example with the integration wallet be sure to clean up your work afterward
async def do_transaction_requests(
    api: provider.Provider,
    run_trades: bool,
    owner_addr: str,
    payer_addr: str,
    open_orders_addr: str,
    order_id: str,
    usdc_wallet: str,
    market: str,
):
    if not run_trades:
        print("skipping transaction requests: set by environment")
        return

    async def submit_order_with_client_id(client_id: int) -> str:
        return await api.submit_order(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market,
            side=proto.Side.S_ASK,
            types=[OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_SERUM,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_id=client_id,
        )

    async def submit_order() -> Tuple[int, str]:
        _client_order_id = random.randint(1, sys.maxsize)
        _signature = await submit_order_with_client_id(_client_order_id)
        return _client_order_id, _signature

    print(
        "submitting order (generate + sign) to sell 0.1 SOL for USDC at 150_000"
        " USD/SOL"
    )

    client_order_id, signature = await submit_order()
    print(signature)

    print(
        "submitting replace order by client ID (generate + sign) to sell 0.1"
        " SOL for USDC at 150_000 USD/SOL"
    )
    print(
        await api.submit_replace_by_client_order_id(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market,
            side=proto.Side.S_ASK,
            types=[OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_SERUM,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_id=client_order_id,
            skip_pre_flight=True,
        )
    )

    print(
        "submitting replace order (generate + sign) to sell 0.1 SOL for USDC at"
        " 150_000 USD/SOL"
    )
    print(
        await api.submit_replace_order(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market=market,
            side=proto.Side.S_ASK,
            types=[OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_SERUM,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_id=0,
            order_id=order_id,
        )
    )

    # cancel order example: comment out if want to try replace example
    print("submit cancel order")
    print(
        await api.submit_cancel_order(
            order_id=order_id,
            side=proto.Side.S_ASK,
            market_address=market,
            owner_address=owner_addr,
            project=proto.Project.P_SERUM,
            open_orders_address=open_orders_addr,
        )
    )

    # cancel by client order ID example: comment out if want to try replace example
    print("submit cancel order by client ID")
    print(
        await api.submit_cancel_by_client_order_id(
            client_order_id=client_order_id,
            market_address=market,
            owner_address=owner_addr,
            project=proto.Project.P_SERUM,
            open_orders_address=open_orders_addr,
            skip_pre_flight=True,
        )
    )

    print("submit settle order")
    print(
        await api.submit_settle(
            owner_address=owner_addr,
            market=market,
            base_token_wallet=owner_addr,
            quote_token_wallet=usdc_wallet,
            project=proto.Project.P_SERUM,
            open_orders_address="",  # optional
        )
    )

    print("creating transactions with memo")
    await create_transaction_with_memo(api)


async def create_transaction_with_memo(api: provider.Provider):
    private_key = transaction.load_private_key_from_env()

    instruction = transaction.create_trader_api_memo_instruction("hi from dev")

    recent_block_hash_resp = await api.get_recent_block_hash(
        get_recent_block_hash_request=proto.GetRecentBlockHashRequest()
    )
    recent_block_hash = hs.Hash.from_string(recent_block_hash_resp.block_hash)
    instructions = [instruction]

    tx_serialized = transaction.build_fully_signed_txn(
        recent_block_hash, private_key.pubkey(), instructions, private_key
    )
    single_memo_txn = base64.b64encode(tx_serialized).decode("utf-8")
    print("serialized memo single_memo_txn", single_memo_txn)

    post_submit_response = await api.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(single_memo_txn),
            skip_pre_flight=True,
        )
    )
    print("signature for single memo txn", post_submit_response.signature)

    double_memo_txn_signed = transaction.add_memo_to_serialized_txn(
        single_memo_txn, "hi from dev2", private_key.pubkey(), private_key
    )
    print("double_memo_txn_signed", double_memo_txn_signed)
    post_submit_response = await api.post_submit(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(double_memo_txn_signed),
            skip_pre_flight=True,
        )
    )
    print("signature for double memo tx", post_submit_response.signature)
