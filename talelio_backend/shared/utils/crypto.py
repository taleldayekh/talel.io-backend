from base64 import b64decode, b64encode
from typing import Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (Encoding, NoEncryption, PrivateFormat,
                                                          PublicFormat)


def generate_master_encryption_key() -> str:
    master_encryption_key = Fernet.generate_key()

    return b64encode(master_encryption_key).decode('utf-8')


def generate_key_pair() -> Tuple[bytes, bytes]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(encoding=Encoding.PEM,
                                                format=PrivateFormat.PKCS8,
                                                encryption_algorithm=NoEncryption())
    public_key_pem = public_key.public_bytes(encoding=Encoding.PEM,
                                             format=PublicFormat.SubjectPublicKeyInfo)

    return private_key_pem, public_key_pem


def encrypt(data: bytes, encryption_key: bytes) -> bytes:
    if len(encryption_key) != 32:
        raise ValueError('Encryption key must be 32 bytes')

    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(data)

    return encrypted_data


def decrypt(data: bytes, encryption_key: bytes) -> bytes:
    if len(encryption_key) != 32:
        raise ValueError('Encryption key must be 32 bytes')

    fernet = Fernet(encryption_key)
    decrypted_data = fernet.decrypt(data)

    return decrypted_data
