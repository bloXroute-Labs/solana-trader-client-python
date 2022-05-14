import os
import base58
import base64
from solana.keypair import Keypair
from solana.transaction import Transaction

# sign_tx uses the environment variable for `PRIVATE_KEY` to sign the message content and replace the zero signature
def sign_tx(unsigned_tx_base64: str) -> str:
    # get base58 encoded private key
    pkey_str = os.getenv("PRIVATE_KEY")
    if pkey_str == None:
        raise EnvironmentError("env variable `PRIVATE_KEY` not set")

    # convert base58 private key string to a keypair
    pkey_bytes = bytes(pkey_str, encoding="utf-8")
    pkey_bytes_base58 = base58.b58decode(pkey_bytes)
    key_pair = Keypair.from_secret_key(pkey_bytes_base58)

    return sign_tx_with_private_key(unsigned_tx_base64, key_pair)

# sign_tx_with_private_key uses the provided private key to sign the message content and replace the zero signature
def sign_tx_with_private_key(unsigned_tx_base64: str, key_pair: Keypair) -> str:
    # convert base64 transaction string to a transaction
    tx_bytes = bytes(unsigned_tx_base64, encoding="utf-8")
    tx_bytes_base64 = base64.decodebytes(tx_bytes)
    tx = Transaction.deserialize(tx_bytes_base64)

    # sign transaction using keypair
    _sign_tx(tx, key_pair)

    # convert transaction back to base64
    signed_tx_bytes_base64 = base64.b64encode(tx.serialize())
    return signed_tx_bytes_base64.decode("utf-8")

def _sign_tx(tx: Transaction, key_pair: Keypair):
    signatures_required = tx.compile_message().header.num_required_signatures
    signatures_present = len(tx.signatures)
    if signatures_present != signatures_required:
        raise Exception(f"transaction requires {signatures_required} signatures and has {signatures_present} signatures")

    _replace_zero_signature(tx, key_pair)

def _replace_zero_signature(tx: Transaction, key_pair: Keypair):
    message_content = tx.serialize_message()
    signed_message_content = key_pair.sign(message_content)
    new_signature = signed_message_content.signature

    if not tx.signatures:
        raise Exception("transaction does not have any signatures")

    zero_sig_index = -1
    for index, pub_key_pair in enumerate(tx.signatures):
        if pub_key_pair.signature == None:
            if zero_sig_index != -1:
                raise Exception("more than one zero signature provided in transaction")
            zero_sig_index = index

    if zero_sig_index == -1:
        raise Exception("no zero signatures to replace in transaction")
    tx.signatures[zero_sig_index].signature = new_signature

if __name__ == "__main__":
    print(sign_tx("AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAED09BGOKfRK6WGiO0o7kWCCWZ2RiqZBNIoyi+Vw8IRyvDbbYaLHvnfd23zEPkcudbLCxTIkT6hXtu4mO68gz796QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAedOROtza44ZAyO1+X+t7VLZ6u9p37/4c1q3S8bO5Kj8BAgIAAQwCAAAAAQAAAAAAAAA="))