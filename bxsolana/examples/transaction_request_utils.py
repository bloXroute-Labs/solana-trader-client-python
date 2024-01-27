import random
import sys
from typing import Tuple

from bxsolana_trader_proto import api as proto
from bxsolana_trader_proto.common import OrderType

from .. import provider
from .. import transaction


# if you run this example with the integration wallet be sure to clean up your work afterward
async def do_transaction_requests(
    api: provider.Provider,
    run_trades: bool,
):
    if not run_trades:
        print("skipping transaction requests: set by environment")
        return

    print("marking transactions with memo")
    await mark_transaction_with_memo(api)


async def mark_transaction_with_memo(api: provider.Provider):
    private_key = transaction.load_private_key_from_env()
    public_key = private_key.pubkey()
    response = await api.post_jupiter_swap(
        post_jupiter_swap_request=proto.PostJupiterSwapRequest(
            owner_address=str(public_key),
            in_token="USDT",
            in_amount=0.01,
            out_token="USDC",
            slippage=0.01,
        )
    )

    tx = response.transactions[0].content
    tx = transaction.add_memo_to_serialized_txn(tx)

    signed_tx = transaction.sign_tx_with_private_key(tx, private_key)

    post_submit_response = await api.post_submit_v2(
        post_submit_request=proto.PostSubmitRequest(
            transaction=proto.TransactionMessage(signed_tx),
            skip_pre_flight=True,
        )
    )
    print("signature for single memo txn", post_submit_response.signature)
