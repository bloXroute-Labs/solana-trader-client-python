import base64
import os
import unittest
import bxserum.transaction.signing as signing


class TestTransaction(unittest.TestCase):
    def test_sign(self):
        os.environ["PRIVATE_KEY"] = "2mvTYCLXLM3e2oucFQCtGbjkibHkEDAJcSkq45abcNuP7xtpvS4nGMBsHZYVRNHGqiktoBEBAdcvgGASU1DTodPJ" # fake private key (afaik)
        tx = signing.sign_tx("AAEAAQPT0EY4p9ErpYaI7SjuRYIJZnZGKpkE0ijKL5XDwhHK8Ntthose+d93bfMQ+Ry51ssLFMiRPqFe27iY7ryDP"
                             "v3pAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwHDKRQmyQHHokjruWGNrJQWdcYM1ZcQimhLQNbLV0dg"
                             "ECAgABDAIAAAABAAAAAAAAAA==")

        tx_base_64_bytes = base64.b64encode(tx.serialize())
        tx_base_64_str = tx_base_64_bytes.decode("utf-8")

        self.assertEqual("ASnYXUDR8hdZsofgeTyri5hEXQSQXmNt3F+QFniUJPqIG5nf74ipPf/7wHeJRYvBYlfaipTRpICmj13FaMVuzAMBAAEE"
                         "ugRPIDG0+TzRhYU+PTXcrGZQ2fPiLO0Ubrj9PhMbHSjT0EY4p9ErpYaI7SjuRYIJZnZGKpkE0ijKL5XDwhHK8Ntthose"
                         "+d93bfMQ+Ry51ssLFMiRPqFe27iY7ryDPv3pAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwHDKRQmyQHHok"
                         "jruWGNrJQWdcYM1ZcQimhLQNbLV0dgEDAgECDAIAAAABAAAAAAAAAA==", tx_base_64_str)