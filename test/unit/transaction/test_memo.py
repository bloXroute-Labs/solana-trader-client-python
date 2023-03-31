import base64
import unittest

import base58
from solders.hash import Hash
from solders.keypair import Keypair

from bxsolana.transaction import memo

# key generated for this test
RANDOM_PRIVATE_KEY = "3KWC65p6AvMjvpR2r1qLTC4HVSH4jEFr5TMQxagMLo1o3j4yVYzKsfbB3jKtu3yGEHjx2Cc3L5t8wSo91vpjT63t"
EXPECTED_TX = "AUtsDXEoPs/Le7/K1Q/nmExo+CpTpFqQgPMbGUSCBNAmZrD7hqbyg60kCgWQSq51dHg/s6ZHPJv4uh6Bx739hwwBAAECJtRexXabOwki+cTaDA2v4p93KEdHmPKORFtuewaoCqvzoQQP2CW/hYwd0lyG8/Zlm8M9Cro+eJpipSyuyZn3gQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAgEAC2hpIGZyb20gZGV2AQAMaGkgZnJvbSBkZXYy"


class TestMemo(unittest.TestCase):
    def test_adding_memo_to_serialized_tx(self):
        pkey_bytes = bytes(RANDOM_PRIVATE_KEY, encoding="utf-8")
        pkey_bytes_base58 = base58.b58decode(pkey_bytes)
        kp = Keypair.from_bytes(pkey_bytes_base58)

        instruction = memo.create_trader_api_memo_instruction("hi from dev")

        recent_block_hash = Hash.from_string("11111111111111111111111111111114")
        instructions = [instruction]

        tx_serialized = memo.build_fully_signed_txn(
            recent_block_hash, kp.pubkey(), instructions, kp
        )

        txbase64 = base64.encodebytes(tx_serialized).decode("ascii")
        tx_bytes = memo.add_memo_to_serialized_txn(
            txbase64, "hi from dev2", kp.pubkey(), kp
        )

        self.assertEqual(EXPECTED_TX, tx_bytes)
