from rest_framework import status
from django.db.models import ProtectedError
import pytest
from model_bakery import baker
from students.models import Curator, Student


@pytest.fixture
def create_curator(api_client):
    def do_create_client(curator):
        return api_client.post('/ielts/curators/', curator)
    return do_create_client


@pytest.mark.django_db
class TestRetrieveCuratorList:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        curators = baker.make(Curator, _quantity=10)

        response = api_client.get('/ielts/curators/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        curators = baker.make(Curator, _quantity=10)

        authenticate_user()
        response = api_client.get('/ielts/curators/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        curators = baker.make(Curator, _quantity=10)

        authenticate_user(is_staff=True)
        response = api_client.get('/ielts/curators/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveCurator:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        curator = baker.make(Curator)

        response = api_client.get(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user()
        response = api_client.get(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': curator.pk,
            'name': curator.name,
            'phone': curator.phone
        }

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': curator.pk,
            'name': curator.name,
            'phone': curator.phone
        }


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
class TestModifyFullyCurator:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        curator = baker.make(Curator)

        response = api_client.put(f'/ielts/curators/{curator.pk}/', {'name': 'm', 'phone': '896512'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user()
        response = api_client.put(f'/ielts/curators/{curator.pk}/', {'name': 'm', 'phone': '896512'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user(is_staff=True)
        response = api_client.put(f'/ielts/curators/{curator.pk}/', {'name': 'm', 'phone': '896512'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': curator.pk,
            'name': 'm',
            'phone': '896512'
        }



@pytest.mark.django_db
class TestModifyPartlyCurator:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        curator = baker.make(Curator)

        response = api_client.patch(f'/ielts/curators/{curator.pk}/', {'name': 'm'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user()
        response = api_client.patch(f'/ielts/curators/{curator.pk}/', {'name': 'm'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user(is_staff=True)
        response = api_client.patch(f'/ielts/curators/{curator.pk}/', {'name': 'm'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': curator.pk,
            'name': 'm',
            'phone': curator.phone
        }


@pytest.mark.django_db
class TestDeleteCurator:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        curator = baker.make(Curator)

        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user()
        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate_user):
        curator = baker.make(Curator)

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestDeleteRelatedToStudentCurator:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        student = baker.make(Student)
        curator = student.curator

        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        student = baker.make(Student)
        curator = student.curator

        authenticate_user()
        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_405(self, api_client, authenticate_user):
        student = baker.make(Student)
        curator = student.curator

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/curators/{curator.pk}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
