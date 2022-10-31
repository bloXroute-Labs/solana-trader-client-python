import base64

from solana import transaction as solana_transaction, keypair
from solana.publickey import PublicKey
from solana.blockhash import Blockhash
from solana.message import CompiledInstruction, Message, MessageArgs, MessageHeader


class Memo:
    BxMemoMarkerMsg: "Powered by bloXroute Trader Api"
    TraderAPIMemoProgram = PublicKey("HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx")

    # create_trader_api_memo_instruction generates a transaction instruction that places a memo in the transaction log
    # Having a memo instruction with signals Trader-API usage is required
    def create_trader_api_memo_instruction(self, msg: ""):
        if msg == "":
            msg = self.BxMemoMarkerMsg

        data = bytes(msg, 'utf-8')
        instruction = solana_transaction.TransactionInstruction(keys=[], program_id=self.TraderAPIMemoProgram,
                                                                data=data)
        return instruction

    def add_memo(self, instructions, memo_content, blockhash, owner, private_keys):
        memo = self.create_trader_api_memo_instruction(memo_content)

        instructions.append(memo)

        txn_bytes, err = self.build_fully_signed_txn(blockhash, owner, instructions, private_keys)
        if err is not None:
            return "", err

        return base64.encodebytes(txn_bytes), None

    # add_memo_to_serialized_txn adds memo instruction to a serialized transaction, it's primarily used if the user
    # doesn't want to interact with Trader-API directly
    def add_memo_to_serialized_txn(self, tx_base64, memo_content, owner, private_keys):
        tx_bytes = bytes(tx_base64, encoding="utf-8")
        tx_bytes_base64 = base64.decodebytes(tx_bytes)

        tx = solana_transaction.Transaction.deserialize(tx_bytes_base64)

        return self.add_memo(tx.instructions, memo_content, tx.recent_blockhash, owner, private_keys)

    def build_fully_signed_txn(self, recent_block_hash, owner, instructions, private_keys):

        tx = solana_transaction.Transaction(recent_blockhash=recent_block_hash)

        tx.instructions.append(instructions)
        tx.fee_payer = owner
        tx.sign(private_keys)

        return tx.serialize(), None
