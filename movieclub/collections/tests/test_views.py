import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub.collections.models import Collection, CollectionItem
from movieclub.collections.tests.factories import (
    create_collection,
    create_collection_item,
)
from movieclub.releases.tests.factories import create_movie
from movieclub.tests.factories import create_batch
from movieclub.users.tests.factories import create_user


@pytest.fixture()
def collection(auth_user):
    return create_collection(user=auth_user)


@pytest.fixture()
def release():
    return create_movie()


class TestCollectionList:
    url = reverse_lazy("collections:collection_list")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_collection, 3)
        assert client.get(self.url).status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client):
        create_collection(name="testme")
        assert (
            client.get(self.url, {"query": "testme"}).status_code == http.HTTPStatus.OK
        )


class TestUserCollectionList:
    @pytest.mark.django_db()
    def test_get(self, client):
        user = create_user()
        create_batch(create_collection, 3, user=user)
        assert (
            client.get(
                reverse("collections:user_collection_list", args=[user.username])
            ).status_code
            == http.HTTPStatus.OK
        )


class TestAddCollection:
    url = reverse_lazy("collections:add_collection")

    @pytest.mark.django_db()
    def test_get(self, client, auth_user):
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        response = client.post(self.url, {"name": "test"})
        assert response.url == reverse("collections:collection_list")
        collection = Collection.objects.get()
        assert collection.name == "test"
        assert collection.user == auth_user


class TestCollectionDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        collection = create_collection()
        create_batch(create_collection_item, 3, collection=collection)

        response = client.get(collection.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestEditCollection:
    @pytest.fixture()
    def url(self, collection):
        return reverse("collections:edit_collection", args=[collection.pk])

    @pytest.mark.django_db()
    def test_get(self, client, collection, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, collection, url):
        response = client.post(url, {"name": "test"})
        collection.refresh_from_db()
        assert collection.name == "test"
        assert response.url == collection.get_absolute_url()


class TestAddReleaseToCollection:
    @pytest.fixture()
    def url(self, collection, release):
        return reverse(
            "collections:add_release_to_collection", args=[collection.pk, release.pk]
        )

    @pytest.mark.django_db()
    def test_post(self, client, auth_user, collection, release, url):
        response = client.post(url)
        assert response.status_code == http.HTTPStatus.OK
        assert CollectionItem.objects.filter(
            collection=collection, release=release
        ).exists()

    @pytest.mark.django_db(transaction=True)
    def test_post_exists(self, client, auth_user, collection, release, url):
        CollectionItem.objects.create(collection=collection, release=release)
        response = client.post(url)
        assert response.status_code == http.HTTPStatus.OK


class TestRemoveReleaseFromCollection:
    @pytest.mark.django_db(transaction=True)
    def test_delete(self, client, auth_user, collection, release):
        CollectionItem.objects.create(collection=collection, release=release)
        response = client.delete(
            reverse(
                "collections:remove_release_from_collection",
                args=[collection.pk, release.pk],
            )
        )
        assert response.status_code == http.HTTPStatus.OK
        assert CollectionItem.objects.count() == 0
