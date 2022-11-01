import base64
import unittest

import base58
from solana.keypair import Keypair
from .memo import Memo

from solana.publickey import PublicKey
from solana.blockhash import Blockhash

# key generated for this test
RANDOM_PRIVATE_KEY = "3KWC65p6AvMjvpR2r1qLTC4HVSH4jEFr5TMQxagMLo1o3j4yVYzKsfbB3jKtu3yGEHjx2Cc3L5t8wSo91vpjT63t"
EXPECTED_TXN_DOUBLE_INST = b'AUtsDXEoPs/Le7/K1Q/nmExo+CpTpFqQgPMbGUSCBNAmZrD7hqbyg60kCgWQSq51dHg/s6ZHPJv4\nuh6Bx739hwwBAAECJtRexXabOwki+cTaDA2v4p93KEdHmPKORFtuewaoCqvzoQQP2CW/hYwd0lyG\n8/Zlm8M9Cro+eJpipSyuyZn3gQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAgEAC2hp\nIGZyb20gZGV2AQAMaGkgZnJvbSBkZXYy\n'



class TestMemo(unittest.TestCase):
    def test_adding_memo_to_serialized_tx(self):
        pkey_bytes = bytes(RANDOM_PRIVATE_KEY, encoding="utf-8")
        pkey_bytes_base58 = base58.b58decode(pkey_bytes)
        kp = Keypair.from_secret_key(pkey_bytes_base58)

        instruction = Memo.create_trader_api_memo_instruction("hi from dev")

        recent_block_hash = Blockhash(str(PublicKey(3)))
        instructions = [instruction]

        tx_serialized = Memo.build_fully_signed_txn(recent_block_hash, kp.public_key, instructions, kp)

        txbase64_str = base64.encodebytes(tx_serialized).decode('utf-8')
        tx_bytes = Memo.add_memo_to_serialized_txn(txbase64_str, "hi from dev2", kp.public_key,  kp)
        self.assertEqual(EXPECTED_TXN_DOUBLE_INST, tx_bytes)
