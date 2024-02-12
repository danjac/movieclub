import http

import httpx
import pytest

from movieclub.activitypub.signature import (
    create_key_pair,
    make_digest,
    make_signature,
    verify_signature,
)


class TestSignature:
    actor_url = "https://movieclub.social/actor/"
    inbox_url = "https://example.com/inbox/"

    payload = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "https://activitypub.academy/16606771-befe-483b-9e2c-0b8b85062373",
        "type": "Follow",
        "actor": "https://activitypub.academy/users/alice",
        "object": "https://techhub.social/users/berta",
    }

    @pytest.fixture()
    def keypair(self):
        return create_key_pair()

    @pytest.fixture()
    def private_key(self, keypair):
        return keypair[0]

    @pytest.fixture()
    def public_key(self, keypair):
        return keypair[1]

    def test_create_key_pair(self, private_key, public_key):
        assert "RSA PRIVATE KEY" in private_key
        assert "PUBLIC KEY" in public_key

    def test_verify_signature(self, rf, private_key, public_key):
        headers = make_signature(
            self.inbox_url,
            private_key=private_key,
            actor_url=self.actor_url,
        )
        req = rf.post(
            self.inbox_url,
            self.payload,
            **{f"HTTP_{k.upper()}": v for k, v in headers.items()},
        )

        def _handle(request):
            json = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "publicKey": {"pubkeyPrem": public_key},
            }

            return httpx.Response(http.HTTPStatus.OK, json=json)

        client = httpx.Client(transport=httpx.MockTransport(_handle))

        verify_signature(req, client)

    def test_verify_signature_with_digest(self, rf, private_key, public_key):
        digest = make_digest(self.payload)

        headers = make_signature(
            self.inbox_url,
            private_key=private_key,
            actor_url="https://domain.com/tester/",
            digest=digest,
        )

        req = rf.post(
            self.inbox_url,
            self.payload,
            content_type="application/json",
            **{f"HTTP_{k.upper()}": v for k, v in headers.items()},
        )

        def _handle(request):
            json = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "publicKey": {"pubkeyPrem": public_key},
            }

            return httpx.Response(http.HTTPStatus.OK, json=json)

        client = httpx.Client(transport=httpx.MockTransport(_handle))
        verify_signature(req, client)

    def test_make_signature(self, private_key):
        assert make_signature(
            "https://example.com",
            private_key=private_key,
            actor_url=self.actor_url,
        )

    def test_make_signature_with_digest(self, private_key):
        assert make_signature(
            "https://example.com",
            private_key=private_key,
            actor_url=self.actor_url,
            digest=make_digest(self.payload),
        )
