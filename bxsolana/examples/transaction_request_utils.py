import base64

from solana.blockhash import Blockhash

import bxsolana
from bxsolana import transaction
from bxsolana_trader_proto import api as proto

from .constants import SOL_USDC_MARKET


async def do_transaction_requests(
    api: bxsolana.Provider,
    run_trades,
    owner_addr,
    payer_addr,
    open_orders_addr,
    order_id,
    usdc_wallet,
):
    if not run_trades:
        print("skipping transaction requests: set by environment")
        return

    print("creating transactions with memo")
    await create_transaction_with_memo(api)

    print(
        "submitting order (generate + sign) to sell 0.1 SOL for USDC at 150_000"
        " USD/SOL"
    )
    print(
        await api.submit_order(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market="SOLUSDC",
            side=proto.Side.S_ASK,
            types=[proto.OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_OPENBOOK,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_id=0,
        )
    )

    print("submit cancel order")
    print(
        await api.submit_cancel_order(
            order_i_d=order_id,
            side=proto.Side.S_ASK,
            market_address="SOLUSDC",
            owner_address=owner_addr,
            project=proto.Project.P_OPENBOOK,
            open_orders_address=open_orders_addr,
        )
    )

    print("submit cancel order by client ID")
    print(
        await api.submit_cancel_by_client_order_i_d(
            client_order_i_d=123,
            market_address=SOL_USDC_MARKET,
            owner_address=owner_addr,
            project=proto.Project.P_OPENBOOK,
            open_orders_address=open_orders_addr,
        )
    )
    print("submit settle order")
    print(
        await api.submit_settle(
            owner_address=owner_addr,
            market="SOLUSDC",
            base_token_wallet=owner_addr,
            quote_token_wallet=usdc_wallet,
            project=proto.Project.P_OPENBOOK,
            open_orders_address="",  # optional
        )
    )

    print(
        "submitting order (generate + sign) to sell 0.1 SOL for USDC at 150_000"
        " USD/SOL"
    )
    print(
        await api.submit_replace_by_client_order_i_d(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market="SOLUSDC",
            side=proto.Side.S_ASK,
            types=[proto.OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_OPENBOOK,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_i_d=123,
        )
    )
    print(
        "submitting order (generate + sign) to sell 0.1 SOL for USDC at 150_000"
        " USD/SOL"
    )
    print(
        await api.submit_replace_order(
            owner_address=owner_addr,
            payer_address=payer_addr,
            market="SOLUSDC",
            side=proto.Side.S_ASK,
            types=[proto.OrderType.OT_LIMIT],
            amount=0.1,
            price=150_000,
            project=proto.Project.P_OPENBOOK,
            # optional, but much faster if known
            open_orders_address=open_orders_addr,
            # optional, for identification
            client_order_id=0,
            order_i_d=order_id,
        )
    )


async def create_transaction_with_memo(api: bxsolana.Provider):
    private_key = transaction.load_private_key_from_env()

    instruction = transaction.create_trader_api_memo_instruction("hi from dev")

    recent_block_hash_resp = await api.get_recent_block_hash()
    recent_block_hash = Blockhash(recent_block_hash_resp.block_hash)
    instructions = [instruction]

    tx_serialized = transaction.build_fully_signed_txn(
        recent_block_hash, private_key.public_key, instructions, private_key
    )
    single_memo_txn = base64.b64encode(tx_serialized).decode("utf-8")
    print("serialized memo single_memo_txn", single_memo_txn)

    post_submit_response = await api.post_submit(
        transaction=proto.TransactionMessage(single_memo_txn),
        skip_pre_flight=True,
    )
    print("signature for single memo txn", post_submit_response.signature)

    double_memo_txn_signed = transaction.add_memo_to_serialized_txn(
        single_memo_txn, "hi from dev2", private_key.public_key, private_key
    )
    print("double_memo_txn_signed", double_memo_txn_signed)
    post_submit_response = await api.post_submit(
        transaction=proto.TransactionMessage(double_memo_txn_signed),
        skip_pre_flight=True,
    )
    print("signature for double memo tx", post_submit_response.signature)
