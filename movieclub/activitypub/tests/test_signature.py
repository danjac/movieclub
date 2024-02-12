import http

import httpx

from movieclub.activitypub.signature import (
    create_key_pair,
    make_digest,
    make_signature,
    verify_signature,
)


def test_create_key_pair():
    priv_key, pub_key = create_key_pair()
    assert "RSA PRIVATE KEY" in priv_key
    assert "PUBLIC KEY" in pub_key


def test_verify_signature(rf):
    priv_key, pub_key = create_key_pair()
    url = "https://example.com/inbox"
    headers = make_signature(
        url,
        private_key=priv_key,
        actor_url="https://domain.com/tester/",
    )

    req = rf.post(
        "/inbox",
        **{f"HTTP_{k.upper()}": v for k, v in headers.items()},
    )

    def _handle(request):
        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "publicKey": {"pubkeyPrem": pub_key},
        }

        return httpx.Response(http.HTTPStatus.OK, json=json)

    client = httpx.Client(transport=httpx.MockTransport(_handle))
    verify_signature(req, client)


def test_make_signature():
    priv_key, _ = create_key_pair()
    assert make_signature(
        "https://example.com",
        private_key=priv_key,
        actor_url="https://example.com/actor/",
    )


def test_make_signature_with_digest():
    priv_key, _ = create_key_pair()
    assert make_signature(
        "https://example.com",
        private_key=priv_key,
        actor_url="https://example.com/actor/",
        digest=make_digest(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "id": "https://social.example/alyssa/",
                "name": "Alyssa P. Hacker",
                "preferredUsername": "alyssa",
                "summary": "Lisp enthusiast hailing from MIT",
                "inbox": "https://social.example/alyssa/inbox/",
                "outbox": "https://social.example/alyssa/outbox/",
                "followers": "https://social.example/alyssa/followers/",
                "following": "https://social.example/alyssa/following/",
                "liked": "https://social.example/alyssa/liked/",
            }
        ),
    )
