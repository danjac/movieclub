from Crypto import Random
from Crypto.PublicKey import RSA


def create_key_pair() -> tuple[str, str]:
    """Create random private and public key pair."""
    key = RSA.generate(2048, Random.new().read)
    return (
        key.export_key().decode("utf-8"),
        key.public_key().export_key().decode("utf-8"),
    )
