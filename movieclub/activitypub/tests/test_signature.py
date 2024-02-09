import uuid

from movieclub.activitypub.signature import create_key_pair, make_digest, make_signature


def test_create_key_pair():
    priv_key, pub_key = create_key_pair()
    assert "RSA PRIVATE KEY" in priv_key
    assert "PUBLIC KEY" in pub_key


def test_make_signature():
    priv_key, _ = create_key_pair()
    assert make_signature(
        "https://example.com",
        private_key=priv_key,
        object_id=uuid.uuid4().hex,
    )


def test_make_signature_with_digest():
    priv_key, _ = create_key_pair()
    assert make_signature(
        "https://example.com",
        private_key=priv_key,
        object_id=uuid.uuid4().hex,
        digest=make_digest({}),
    )
