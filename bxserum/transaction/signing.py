import base58, base64
import os

import based58
import solana.keypair
from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.transaction import AccountMeta, Transaction, TransactionInstruction


def sign_tx(unsigned_tx_base64: str):
    # get base58 encoded private key
    pkey_str = os.getenv("PRIVATE_KEY")
    if pkey_str == None:
        raise EnvironmentError("env variable `PRIVATE_KEY` not set")

    # convert b58 private key string to a keypair
    pkey_bytes_base58 = bytes(pkey_str, encoding="utf-8")
    pkey_bytes = base58.b58decode(pkey_bytes_base58)
    key_pair = Keypair.from_secret_key(pkey_bytes)

    # convert base64 transaction string to a transaction
    tx_bytes_base64 = bytes(unsigned_tx_base64, encoding="utf-8")
    tx_bytes = base64.decodebytes(tx_bytes_base64)
    tx = Transaction.deserialize(tx_bytes)
    tx.sign(key_pair)

if __name__ == "__main__":
    sign_tx("AAEAAQPT0EY4p9ErpYaI7SjuRYIJZnZGKpkE0ijKL5XDwhHK8Ntthose+d93bfMQ+Ry51ssLFMiRPqFe27iY7ryDPv3pAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwHDKRQmyQHHokjruWGNrJQWdcYM1ZcQimhLQNbLV0dgECAgABDAIAAAABAAAAAAAAAA==")