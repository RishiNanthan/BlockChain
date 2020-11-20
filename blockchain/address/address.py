from ecdsa import VerifyingKey as PublicKey, SECP256k1 as curve, SigningKey as PrivateKey
import ecdsa
from ..encoding.encoding import encode_private_key, encode_public_key


def generate_keys() -> tuple:
    """
        Generates ECDSA keys

        Returns
        (public_key, private_key)

    """
    private_key = ecdsa.SigningKey.generate(curve=curve)
    public_key = private_key.get_verifying_key()

    private_key = encode_private_key(private_key)
    public_key = encode_public_key(public_key)

    return public_key, private_key