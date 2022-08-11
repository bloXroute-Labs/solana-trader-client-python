import base64
from typing import List

from solana import transaction as solana_transaction, keypair
from solana.utils import shortvec_encoding as shortvec


class PartialTransaction:
    signatures: List[bytes]
    message: bytes

    def __init__(self, message_bytes: bytes, signatures: List[bytes]):
        self.message = message_bytes
        self.signatures = signatures

    def complete_signing(self, private_key: keypair.Keypair):
        new_signature = private_key.sign(self.message)

        for i, existing_signature in enumerate(self.signatures):
            if is_zero(existing_signature):
                self.signatures[i] = new_signature.signature
                break

    def serialize(self) -> bytes:
        output = bytearray()

        signature_count = shortvec.encode_length(len(self.signatures))
        output.extend(signature_count)

        for signature in self.signatures:
            output.extend(signature)

        output.extend(self.message)
        return bytes(output)

    @classmethod
    def deserialize(cls, tx_base64: str) -> "PartialTransaction":
        tx_bytes = bytes(tx_base64, encoding="utf-8")
        tx_bytes_base64 = base64.decodebytes(tx_bytes)

        signatures = []
        signature_count, offset = shortvec.decode_length(tx_bytes_base64)
        zero_signatures = 0
        for _ in range(signature_count):
            signature_bytes = tx_bytes_base64[
                offset : offset + solana_transaction.SIG_LENGTH
            ]
            if is_zero(signature_bytes):
                zero_signatures += 1

            signatures.append(signature_bytes)
            offset += solana_transaction.SIG_LENGTH

        message_bytes = tx_bytes_base64[offset:]
        num_required_signatures = message_bytes[0]

        if zero_signatures != 1:
            raise ValueError()

        if num_required_signatures != len(signatures):
            raise ValueError()

        return PartialTransaction(message_bytes, signatures)


def is_zero(signature_bytes: bytes) -> bool:
    return signature_bytes == bytes(64)
