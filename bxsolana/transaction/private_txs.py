import base64
from bxsolana_trader_proto import api as proto

from numpy import uint64
from solders import pubkey as pk, keypair
from solders import instruction as inst
from solders import transaction as solders_tx
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import Message, MessageV0
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction, VersionedTransaction
from solders import message as msg


# as of 2/12/2024, this is the bloxRoute tip wallet... check docs to see latest up to date tip wallet:
# https://docs.bloxroute.com/solana/trader-api-v2/front-running-protection-and-transaction-bundle
BloxrouteTipWallet = pk.Pubkey.from_string(
    "HWEoBxYs7ssKuudEjzjmpfJVX7Dvi7wescFsVx2L5yoY"
)


# create_trader_api_tip_instruction creates a tip instruction to send to bloxRoute. This is used if a user wants to send
# bundles or wants front running protection. If using bloXroute API, this instruction must be included in the last
# transaction sent to the API
def create_trader_api_tip_instruction(
        tip_amount: uint64,
        sender_address: Pubkey,
) -> inst.Instruction:
    instruction = transfer(
        TransferParams(
            from_pubkey=sender_address,
            to_pubkey=BloxrouteTipWallet,
            lamports=int(tip_amount),
        )
    )

    return instruction


# create_trader_api_tip_instruction creates a tip transaction to send to bloxRoute. This is used if a user wants to send
# bundles or wants front running protection. If using bloXroute API, this transaction must be the last transaction sent
# to the api
def create_trader_api_tip_tx_signed(
        tip_amount: int, sender_address: Keypair, blockhash: Hash,
) -> proto.TransactionMessage:
    transfer_ix = create_trader_api_tip_instruction(
        uint64(tip_amount), sender_address.pubkey()
    )

    message = MessageV0.try_compile(
        payer=sender_address.pubkey(),
        instructions=[transfer_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )

    tx = VersionedTransaction(message, [sender_address])

    signature = sender_address.sign_message(msg.to_bytes_versioned(tx.message))
    signatures = [signature]

    if len(tx.signatures) > 1:
        signatures.extend(list(tx.signatures[1:]))

    tx = solders_tx.VersionedTransaction.populate(tx.message, signatures)

    # convert transaction back to base64
    signed_tx_bytes_base64 = base64.b64encode(bytes(tx))

    return proto.TransactionMessage(content=signed_tx_bytes_base64.decode('utf-8'), is_cleanup=False)


