
import rsa


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


def encode_public_key(public_key: rsa.PublicKey) -> str:
    """
        Converts PublicKey to Public Key String
    """
    n = hex(public_key.n)[2: ]
    e = hex(public_key.e)[2: ]
    
    n = base58_encode(n)
    e = base58_encode(e)

    return f"{n}-{e}"


def decode_public_key(public_key_string: str) -> rsa.PublicKey:
    n, e = public_key_string.split("-")
    n = base58_decode(n)
    e = base58_decode(e)

    n = int(n, 16)
    e = int(e, 16)

    return rsa.PublicKey(n, e)
