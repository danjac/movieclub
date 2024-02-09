import datetime
import hashlib
import json
from base64 import b64encode
from urllib.parse import urlparse

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from django.utils import timezone
from django.utils.http import http_date


def create_key_pair() -> tuple[str, str]:
    """Create random private and public key pair."""
    key = RSA.generate(2048, Random.new().read)
    return (
        key.export_key().decode("utf-8"),
        key.public_key().export_key().decode("utf-8"),
    )


def make_digest(data: dict) -> str:
    """Creates digest string."""
    encoded = b64encode(
        hashlib.sha256(json.dumps(data).encode("utf-8")).digest()
    ).decode("utf-8")

    return f"SHA-256={encoded}"


def make_signature(
    destination_url: str,
    *,
    private_key: str,
    object_id: str,
    digest: str = "",
    method: str = "POST",
    date: datetime.datetime | None = None,
) -> str:
    """Creates a signature from private key."""

    url = urlparse(destination_url)
    date = date or timezone.now()

    signature_headers = {
        "(request-target)": f"{method} {url.path}",
        "host": f"{url.netloc}",
        "date": http_date(date.timestamp()),
    }

    if digest:
        signature_headers["digest"] = digest

    message = "\n".join([f"{k}: {v}" for k, v in signature_headers.items()])

    signer = pkcs1_15.new(RSA.import_key(private_key))
    signed_message = signer.sign(SHA256.new(message.encode("utf-8")))

    signature = {
        "keyId": f"{object_id}/#main_key",
        "algorithm": "rsa-sha256",
        "headers": " ".join(signature_headers.keys()),
        "signature": b64encode(signed_message).decode("utf-8"),
    }

    return ",".join(f'{k}="{v}"' for (k, v) in signature.items())
