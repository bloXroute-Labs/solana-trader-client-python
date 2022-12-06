import os
import base58
import base64

from solana import keypair as kp

from .deserializer import PartialTransaction
from bxsolana_trader_proto import api as proto


def load_private_key(pkey_str: str) -> kp.Keypair:
    # convert base58 private key string to a keypair
    pkey_bytes = bytes(pkey_str, encoding="utf-8")
    pkey_bytes_base58 = base58.b58decode(pkey_bytes)
    return kp.Keypair.from_secret_key(pkey_bytes_base58)


def load_private_key_from_env() -> kp.Keypair:
    # get base58 encoded private key
    pkey_str = os.getenv("PRIVATE_KEY")
    if pkey_str is None:
        raise EnvironmentError("env variable `PRIVATE_KEY` not set")

    return load_private_key(pkey_str)


def load_open_orders() -> str:
    open_orders = os.getenv("OPEN_ORDERS")
    if open_orders is None:
        raise EnvironmentError("env variable `OPEN_ORDERS` not set")

    return open_orders


def sign_tx(unsigned_tx_base64: str) -> str:
    """
    Uses environment variable `PRIVATE_KEY` to sign message content and replace zero signatures.

    :param unsigned_tx_base64: transaction bytes in base64
    :return: signed transaction
    """
    keypair = load_private_key_from_env()
    return sign_tx_with_private_key(unsigned_tx_base64, keypair)


def sign_tx_with_private_key(
    unsigned_tx_base64: str, keypair: kp.Keypair
) -> str:
    """
    Signs message content and replaces placeholder zero signature with signature.

    :param unsigned_tx_base64: transaction bytes in base64
    :param keypair: key pair to sign with
    :return: signed transaction
    """
    partial_tx = PartialTransaction.deserialize(unsigned_tx_base64)
    partial_tx.complete_signing(keypair)

    # convert transaction back to base64
    signed_tx_bytes_base64 = base64.b64encode(partial_tx.serialize())
    return signed_tx_bytes_base64.decode("utf-8")


def sign_tx_message_with_private_key(
    tx_message: proto.TransactionMessage, keypair: kp.Keypair
) -> proto.TransactionMessage:
    return proto.TransactionMessage(
        sign_tx_with_private_key(tx_message.content, keypair),
        tx_message.is_cleanup,
    )
