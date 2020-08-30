
from ecdsa import VerifyingKey as PublicKey, SECP256k1 as curve, SigningKey as PrivateKey


base58_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(hex_string: str) -> str:
    global base58_string
    number = int(hex_string, 16)
    encoded_string = ""

    while number > 0:
        r = number % 58
        encoded_string = base58_string[r] + encoded_string
        number //= 58

    return encoded_string


def base58_decode(encoded_string: str) -> str:
    global base58_string
    n = len(encoded_string)
    number = 0
    for i in range(n-1, -1, -1):
        number += base58_string.index(encoded_string[i]) * 58 ** (n-i-1)
    return hex(number)[2: ]


def encode_public_key(public_key: PublicKey) -> str:
    """
        PublicKey -> Base58 String
    """
    hex_key = public_key.to_string().hex()
    return base58_encode(hex_key)


def decode_public_key(public_key_string: str) -> PublicKey:
    """
        Base58 String -> PublicKey
    """
    hex_key = bytes.fromhex(base58_decode(public_key_string))
    return PublicKey.from_string(hex_key, curve=curve)


def encode_private_key(private_key: PrivateKey) -> str:
    """
        PublicKey -> Base58 String
    """
    hex_key = private_key.to_string().hex()
    return base58_encode(hex_key)


def decode_private_key(private_key_string: str) -> PrivateKey:
    """
        Base58 String -> Private Key
    """
    hex_key = bytes.fromhex(base58_decode(private_key_string))
    return PrivateKey.from_string(hex_key, curve=curve)

