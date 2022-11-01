import base64

from solana import transaction as solana_transaction, keypair
from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.blockhash import Blockhash
from solana.message import CompiledInstruction, Message, MessageArgs, MessageHeader


class Memo:
    BxMemoMarkerMsg = "Powered by bloXroute Trader Api"
    TraderAPIMemoProgram = PublicKey("HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx")

    # create_trader_api_memo_instruction generates a transaction instruction that places a memo in the transaction log
    # Having a memo instruction with signals Trader-API usage is required
    @staticmethod
    def create_trader_api_memo_instruction(msg):
        if msg == "":
            msg = Memo.BxMemoMarkerMsg

        data = bytes(msg, 'utf-8')
        instruction = solana_transaction.TransactionInstruction(keys=[], program_id=Memo.TraderAPIMemoProgram,
                                                                data=data)

        return instruction

    @staticmethod
    def add_memo(instructions: list[solana_transaction.TransactionInstruction], memo_content: str, blockhash, owner, private_keys):
        memo = Memo.create_trader_api_memo_instruction(memo_content)

        instructions.append(memo)

        txn_bytes = Memo.build_fully_signed_txn(blockhash, owner, instructions, private_keys)

        return base64.encodebytes(txn_bytes)

    # add_memo_to_serialized_txn adds memo instruction to a serialized transaction, it's primarily used if the user
    # doesn't want to interact with Trader-API directly
    @staticmethod
    def add_memo_to_serialized_txn(tx_base64: str, memo_content: str, owner, private_keys: Keypair):
        tx_bytes = bytes(tx_base64, encoding="utf-8")
        tx_bytes_base64 = base64.decodebytes(tx_bytes)

        tx = solana_transaction.Transaction.deserialize(tx_bytes_base64)

        return Memo.add_memo(tx.instructions, memo_content, tx.recent_blockhash, owner, private_keys)

    @staticmethod
    def build_fully_signed_txn(recent_block_hash, owner, instructions: list[solana_transaction.TransactionInstruction], private_keys: Keypair):

        tx = solana_transaction.Transaction(recent_blockhash=recent_block_hash)

        for x in instructions:
            tx.instructions.append(x)

        tx.fee_payer = owner
        tx.sign(private_keys)

        return tx.serialize()
