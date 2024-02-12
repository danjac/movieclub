import datetime
import hashlib
import json
from base64 import b64decode, b64encode
from typing import Final
from urllib.parse import urlparse

import httpx
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from django.http import HttpRequest
from django.utils import timezone
from django.utils.http import http_date

MAX_SIGNATURE_AGE: Final = 300

HASH_FUNCTIONS: Final = {
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
}


class InvalidSignatureError(ValueError):
    """Error raised if signature invalid."""


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
    actor_url: str,
    digest: str = "",
    date: datetime.datetime | None = None,
) -> dict[str, str]:
    """Creates a signature from private key."""

    url = urlparse(destination_url)
    date = date or timezone.now()

    http_headers = {
        "(request-target)": f"post {url.path}",
        "host": url.netloc,
        "date": http_date(date.timestamp()),
    }

    if digest:
        http_headers["digest"] = digest

    message = "\n".join([f"{k}: {v}" for k, v in http_headers.items()])

    signer = pkcs1_15.new(RSA.import_key(private_key))
    signed_message = signer.sign(SHA256.new(message.encode("utf-8")))

    signature_headers = {
        "keyId": f"{actor_url}/#main_key",
        "algorithm": "rsa-sha256",
        "headers": " ".join(http_headers.keys()),
        "signature": b64encode(signed_message).decode("utf-8"),
    }

    signature = ",".join(f'{k}="{v}"' for (k, v) in signature_headers.items())

    return {
        **http_headers,
        "Signature": signature,
    }


def verify_signature(request: HttpRequest, client: httpx.Client) -> None:
    """Verify HTTP Signature in request.
    Raises InvalidSignatureError if any mismatch or missing data.
    """

    try:
        sig_header = {
            k: v.replace('"', "")
            for (k, v) in [
                s.split("=", 1) for s in request.headers["Signature"].split(",")
            ]
        }

        key_id = sig_header["keyId"]
        headers = sig_header["headers"]
        signature = b64decode(sig_header["signature"])

        comparisons: list[tuple[str, str]] = []

        for name in headers.split():
            match name:
                case "(request-target)":
                    comparisons.append(("(request-target)", f"post {request.path}"))
                case "digest":
                    verify_digest(request)
                    comparisons.append((name, request.headers[name]))
                # TBD: check date
                case _:
                    comparisons.append((name, request.headers[name]))

        comparison_string = "\n".join([f"{k}: {v}" for k, v in comparisons])

        response = client.get(key_id)
        response.raise_for_status()

        payload = response.json()

        signer = pkcs1_15.new(RSA.import_key(payload["publicKey"]["pubkeyPrem"]))
        digest = SHA256.new()
        digest.update(comparison_string.encode("utf-8"))

        signer.verify(digest, signature)

    except (KeyError, ValueError, httpx.HTTPError) as e:
        raise InvalidSignatureError from e


def verify_digest(request: HttpRequest) -> None:
    """Checks digest is valid"""
    algorithm, digest = request.headers["digest"].split("=", 1)
    match algorithm:
        case "SHA-256":
            hash_function = hashlib.sha256
        case "SHA-512":
            hash_function = hashlib.sha512
        case _:
            raise ValueError(f"Invalid algorithm: {algorithm}")

    if b64decode(digest) != hash_function(request.body).digest():
        raise ValueError("Invalid HTTP Digest header")
