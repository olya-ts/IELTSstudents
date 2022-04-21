from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def create_curator(api_client):
    def do_create_client(curator):
        return api_client.post('/ielts/curators/', curator)
    return do_create_client


@pytest.mark.django_db
class TestGetCurator:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/ielts/curators/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCreateCurator:
    def test_if_user_is_anonymous_returns_401(self, create_curator):
        response = create_curator({'name': 'a', 'phone': '+53641225321'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_curator, authenticate_user):
        authenticate_user()
        response = create_curator({'name': 'a', 'phone': '+53641225321'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_curator, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_curator({'name': 'a', 'phone': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['phone'] is not None

    def test_if_data_is_valid_returns_201(self, create_curator, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_curator({'name': 'a', 'phone': '+8569233'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestPutCurator:
    def test_if_user_is_anonymous_returns_401(self):
        pass



@pytest.mark.django_db
class TestPatchCurator:
    def test_if_user_is_anonymous_returns_401(self):
        pass


@pytest.mark.django_db
class TestDeleteCurator:
    def test_if_user_is_anonymous_returns_401(self):
        pass
