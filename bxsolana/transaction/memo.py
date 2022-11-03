import base64

from solana import transaction as solana_transaction
from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.blockhash import Blockhash


BxMemoMarkerMsg = "Powered by bloXroute Trader Api"
TraderAPIMemoProgram = PublicKey("HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx")


# create_trader_api_memo_instruction generates a transaction instruction that places a memo in the transaction log
# Having a memo instruction with signals Trader-API usage is required
def create_trader_api_memo_instruction(
    msg: str,
) -> solana_transaction.TransactionInstruction:
    if msg == "":
        msg = BxMemoMarkerMsg

    data = bytes(msg, "utf-8")
    instruction = solana_transaction.TransactionInstruction(
        keys=[], program_id=TraderAPIMemoProgram, data=data
    )

    return instruction


def add_memo(
    instructions: list[solana_transaction.TransactionInstruction],
    memo_content: str,
    blockhash: Blockhash,
    owner: PublicKey,
    *private_keys: Keypair
) -> str:
    memo = create_trader_api_memo_instruction(memo_content)

    instructions.append(memo)

    txn_bytes = build_fully_signed_txn(
        blockhash, owner, instructions, *private_keys
    )

    return base64.b64encode(txn_bytes).decode("utf-8")


# add_memo_to_serialized_txn adds memo instruction to a serialized transaction, it's primarily used if the user
# doesn't want to interact with Trader-API directly
def add_memo_to_serialized_txn(
    tx_base64: str, memo_content: str, owner: PublicKey, *private_keys: Keypair
) -> str:
    tx_bytes = bytes(tx_base64, encoding="utf-8")
    tx_bytes_base64 = base64.b64decode(tx_bytes)

    tx = solana_transaction.Transaction.deserialize(tx_bytes_base64)

    return add_memo(
        tx.instructions, memo_content, tx.recent_blockhash, owner, *private_keys
    )


def build_fully_signed_txn(
    recent_block_hash: Blockhash,
    owner: PublicKey,
    instructions: list[solana_transaction.TransactionInstruction],
    *private_keys: Keypair
) -> bytes:
    tx = solana_transaction.Transaction(recent_blockhash=recent_block_hash)

    for x in instructions:
        tx.instructions.append(x)

    tx.fee_payer = owner
    tx.sign(*private_keys)

    return tx.serialize()
