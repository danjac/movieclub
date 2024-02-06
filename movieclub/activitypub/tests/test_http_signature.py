from movieclub.activitypub.http_signature import create_key_pair


def test_create_key_pair():
    priv_key, pub_key = create_key_pair()
    assert "RSA PRIVATE KEY" in priv_key
    assert "PUBLIC KEY" in pub_key
