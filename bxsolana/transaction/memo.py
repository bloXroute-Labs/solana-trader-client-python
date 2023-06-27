import base64

from solders import pubkey as pk
from solders import instruction as inst
from solders import transaction as solders_tx
from solders import message as solders_msg

BxMemoMarkerMsg = "Powered by bloXroute Trader Api"
TraderAPIMemoProgram = pk.Pubkey.from_string(
    "HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx"
)


# create_trader_api_memo_instruction generates a transaction instruction that places a memo in the transaction log
# Having a memo instruction with signals Trader-API usage is required
def create_trader_api_memo_instruction(
    msg: str,
) -> inst.Instruction:
    if msg == "":
        msg = BxMemoMarkerMsg

    data = bytes(msg, "utf-8")
    instruction = inst.Instruction(TraderAPIMemoProgram, data, [])

    return instruction


def create_compiled_memo_instruction(
    program_id_index: int,
) -> inst.CompiledInstruction:
    data = bytes(BxMemoMarkerMsg, "utf-8")
    instruction = inst.CompiledInstruction(program_id_index, data, bytes([]))

    return instruction


def add_memo(
    tx: solders_tx.VersionedTransaction,
) -> solders_tx.VersionedTransaction:
    instructions = tx.message.instructions
    accounts = tx.message.account_keys
    msg = tx.message

    cutoff = len(tx.message.account_keys)

    for i in range(len(instructions)):
        idxs = list(instructions[i].accounts)
        for j in range(len(idxs)):
            if idxs[j] >= cutoff:
                idxs[j] = idxs[j] + 1

    memo = create_compiled_memo_instruction(cutoff)

    accounts.append(TraderAPIMemoProgram)
    instructions.append(memo)
    if isinstance(msg, solders_msg.MessageV0):
        message = solders_msg.MessageV0(
            msg.header,
            accounts,
            msg.recent_blockhash,
            instructions,
            msg.address_table_lookups,
        )
        return solders_tx.VersionedTransaction.populate(message, tx.signatures)
    else:
        message = solders_msg.Message.new_with_compiled_instructions(
            msg.header.num_required_signatures,
            msg.header.num_readonly_signed_accounts,
            msg.header.num_readonly_unsigned_accounts,
            accounts,
            msg.recent_blockhash,
            instructions,
        )
        return solders_tx.VersionedTransaction.populate(message, tx.signatures)


# add_memo_to_serialized_txn adds memo instruction to a serialized transaction, it's primarily used if the user
# doesn't want to interact with Trader-API directly
def add_memo_to_serialized_txn(tx_base64: str) -> str:
    b = base64.b64decode(tx_base64)

    raw_tx = solders_tx.VersionedTransaction.from_bytes(b)

    tx = add_memo(raw_tx)

    return base64.b64encode(bytes(tx)).decode("utf-8")
