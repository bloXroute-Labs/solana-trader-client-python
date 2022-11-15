import base64
import unittest

import base58
from solana.keypair import Keypair

from solana.publickey import PublicKey
from solana.blockhash import Blockhash

from bxsolana.transaction import memo

# key generated for this test
RANDOM_PRIVATE_KEY = "3KWC65p6AvMjvpR2r1qLTC4HVSH4jEFr5TMQxagMLo1o3j4yVYzKsfbB3jKtu3yGEHjx2Cc3L5t8wSo91vpjT63t"
RANDOM_PRIVATE_KEY2 = "5DtQgvZgb2F86bda5aAojyLyhLiFT2b3PtTqz1UNzrXtt21tk1wt3C5tCgzS12np3ZYiWR88oQWWg1nGQo1qHsbh"
EXPECTED_TXN_DOUBLE_INST = "AktsDXEoPs/Le7/K1Q/nmExo+CpTpFqQgPMbGUSCBNAmZrD7hqbyg60kCgWQSq51dHg/s6ZHPJv4uh6Bx739hwyfu81NGDUMP2uNH2P7A6Pj9pCFGz0tVu+pe3NG8rr+TClvGvc59Br2Rvl85kerayaoaFxBqvsx6MTvOZOyGAIKAQABAibUXsV2mzsJIvnE2gwNr+KfdyhHR5jyjkRbbnsGqAqr86EED9glv4WMHdJchvP2ZZvDPQq6PniaYqUsrsmZ94EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwIBAAtoaSBmcm9tIGRldgEADGhpIGZyb20gZGV2Mg=="


class TestMemo(unittest.TestCase):
    def test_adding_memo_to_serialized_tx(self):
        pkey_bytes = bytes(RANDOM_PRIVATE_KEY, encoding="utf-8")
        pkey_bytes2 = bytes(RANDOM_PRIVATE_KEY2, encoding="utf-8")
        pkey_bytes_base58 = base58.b58decode(pkey_bytes)
        pkey_bytes_base58_2 = base58.b58decode(pkey_bytes2)
        kp = Keypair.from_secret_key(pkey_bytes_base58)
        kp2 = Keypair.from_secret_key(pkey_bytes_base58_2)

        instruction = memo.create_trader_api_memo_instruction("hi from dev")

        recent_block_hash = Blockhash(str(PublicKey(3)))
        instructions = [instruction]

        tx_serialized = memo.build_fully_signed_txn(
            recent_block_hash, kp.public_key, instructions, kp
        )

        txbase64 = base64.encodebytes(tx_serialized).decode("ascii")
        tx_bytes = memo.add_memo_to_serialized_txn(
            txbase64, "hi from dev2", kp.public_key, kp, kp2
        )
        self.assertEqual(EXPECTED_TXN_DOUBLE_INST, tx_bytes)
