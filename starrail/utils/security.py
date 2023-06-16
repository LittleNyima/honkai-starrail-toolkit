import base64
from typing import Tuple

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


class AES192:
    """
    AES192 supports AES-192 encryption and decryption.
    """

    @staticmethod
    def encrypt(plaintext: str, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypts the given plaintext using the provided key.

        Args:
            plaintext (str): The plaintext to be encrypted as a string.
            key (bytes): The 192-bit key to be used for encryption as bytes.

        Returns:
            Tuple[bytes, bytes]: A tuple containing the initialization vector
                (IV) and the encrypted cipher text as bytes.
        """

        cipher = AES.new(key=key, mode=AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return iv, ciphertext

    @staticmethod
    def decrypt(ciphertext: str, key: bytes, iv: bytes) -> str:
        """
        Decrypts the given ciphertext using the provided key and IV.

        Args:
            ciphertext (bytes): The ciphertext to be decrypted as bytes.
            key (bytes): The 192-bit key to be used for decryption as bytes.
            iv (bytes): The initialization vector (IV) used during encryption
                as bytes.

        Returns:
            str: The decrypted plaintext as a string.
        """

        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()


class Base64:
    """
    Base64 supports base64 encoding and decoding.
    """

    @staticmethod
    def encode(plainbytes: bytes) -> str:
        """
        Encodes the given bytes using Base64 encoding.

        Args:
            plainbytes (bytes): The bytes to be encoded.

        Returns:
            str: The Base64 encoded string.
        """

        encoded = base64.b64encode(plainbytes)
        return encoded.decode()

    @staticmethod
    def decode(encodedtext: str) -> bytes:
        """
        Decodes the given Base64 encoded string.

        Args:
            encodedtext (str): The base64 encoded string to be decoded.

        Returns:
            bytes: The decoded bytes.
        """

        encoded = encodedtext.encode()
        decoded = base64.b64decode(encoded)
        return decoded


"""
The 16-bit secret key for cookie aes128 encryption and decryption.
"""
cookie_aes128_key16b = b'W3zh;FLIc94@D,ag'
