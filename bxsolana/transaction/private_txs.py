import base64

import solders
from numpy import uint64
from solders import pubkey as pk
from solders import instruction as inst
from solders import transaction as solders_tx
from solders import message as solders_msg
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import Message
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction

from example.bundles.main import public_key

BloxrouteTipWallet = pk.Pubkey.from_string(
    "AFT8VayE7qr8MoQsW3wHsDS83HhEvhGWdbNSHRKeUDfQ"
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
            lamports=tip_amount,
        )
    )

    return instruction


# create_trader_api_tip_instruction creates a tip transaction to send to bloxRoute. This is used if a user wants to send
# bundles or wants front running protection. If using bloXroute API, this transaction must be the last transaction sent
# to the api
def create_trader_api_tip_tx_signed(
    tip_amount: uint64, sender_address: Keypair, blockhash: Hash
) -> solders_tx.Transaction:
    transfer_ix = create_trader_api_tip_instruction(
        tip_amount, sender_address.pubkey()
    )

    message = Message([transfer_ix], sender_address.pubkey())
    tx = Transaction([sender_address], message, blockhash)

    return tx
