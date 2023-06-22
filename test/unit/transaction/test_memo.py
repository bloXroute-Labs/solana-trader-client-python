import unittest


from bxsolana.transaction import memo

# key generated for this test
RANDOM_PRIVATE_KEY = "3KWC65p6AvMjvpR2r1qLTC4HVSH4jEFr5TMQxagMLo1o3j4yVYzKsfbB3jKtu3yGEHjx2Cc3L5t8wSo91vpjT63t"
EXPECTED_TX = "AAEAAQMmRmIlQZ625bapZEp3haQ7Bu0r1zqVP0wTF9LYtsuMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA86EED9glv4WMHdJchvP2ZZvDPQq6PniaYqUsrsmZ94GF+Ae/EKhvjYII9uq1QkZIuRVBHwVbIHdB+Y3tmQI1zgIBAAACAB9Qb3dlcmVkIGJ5IGJsb1hyb3V0ZSBUcmFkZXIgQXBp"
EMPTY_TRANSACTION = "AAEAAQImRmIlQZ625bapZEp3haQ7Bu0r1zqVP0wTF9LYtsuMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhfgHvxCob42CCPbqtUJGSLkVQR8FWyB3QfmN7ZkCNc4BAQAA"


class TestMemo(unittest.TestCase):
    def test_adding_memo_to_serialized_tx(self):

        tx_bytes = memo.add_memo_to_serialized_txn(
            EMPTY_TRANSACTION
        )

        self.assertEqual(EXPECTED_TX, tx_bytes)