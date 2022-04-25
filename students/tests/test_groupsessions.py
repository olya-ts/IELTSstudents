from rest_framework import status
import pytest
from model_bakery import baker
from students.models import Teacher, GroupSession


@pytest.mark.django_db
class TestRetrieveGroupSessionList:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        groupsessions = baker.make(GroupSession, _quantity=10)

        response = api_client.get('/ielts/group_sessions/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        groupsessions = baker.make(GroupSession, _quantity=10)

        authenticate_user()
        response = api_client.get('/ielts/group_sessions/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        groupsessions = baker.make(GroupSession, _quantity=10)

        authenticate_user(is_staff=True)
        response = api_client.get('/ielts/group_sessions/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveGroupSession:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        groupsession = baker.make(GroupSession)

        response = api_client.get(f'/ielts/group_sessions/{groupsession.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user()
        response = api_client.get(f'/ielts/group_sessions/{groupsession.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': groupsession.pk,
            'title': groupsession.title,
            'description': groupsession.description,
            'teacher': []
        }

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/group_sessions/{groupsession.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': groupsession.pk,
            'title': groupsession.title,
            'description': groupsession.description,
            'teacher': []
        }


@pytest.mark.django_db
class TestCreateGroupSession:
    def test_if_user_is_anonymous_returns_401(self, create_new_instance):
        response = create_new_instance(
            '/ielts/group_sessions/',
            {'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': []}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_new_instance, authenticate_user):
        authenticate_user()
        response = create_new_instance(
            '/ielts/group_sessions/',
            {'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': []}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_new_instance, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_new_instance(
            '/ielts/group_sessions/',
            {'title': '', 'description': 'kdzjbfv', 'teacher': []}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_new_instance, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = create_new_instance(
            '/ielts/group_sessions/',
            {'id': 34, 'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': [teacher.pk]}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': 34,
            'title': 'kdjsvk',
            'description': 'kdzjbfv',
            'teacher': [teacher.pk]
        }


@pytest.mark.django_db
class TestModifyFullyGroupSession:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)
        groupsession = baker.make(GroupSession)

        response = api_client.put(
            f'/ielts/group_sessions/{groupsession.pk}/',
            {'id': 1, 'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': [teacher.pk]}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        groupsession = baker.make(GroupSession)

        authenticate_user()
        response = api_client.put(
            f'/ielts/group_sessions/{groupsession.pk}/',
            {'id': 1, 'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': [teacher.pk]}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        groupsession = baker.make(GroupSession)

        authenticate_user(is_staff=True)
        response = api_client.put(
            f'/ielts/group_sessions/{groupsession.pk}/',
            {'id': 1, 'title': 'kdjsvk', 'description': 'kdzjbfv', 'teacher': [teacher.pk]}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': groupsession.pk,
            'title': 'kdjsvk',
            'description': 'kdzjbfv',
            'teacher': [teacher.pk]
        }


@pytest.mark.django_db
class TestModifyPartlyGroupSession:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        groupsession = baker.make(GroupSession)

        response = api_client.patch(f'/ielts/group_sessions/{groupsession.pk}/', {'description': 'blabla'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user()
        response = api_client.patch(f'/ielts/group_sessions/{groupsession.pk}/', {'description': 'blabla'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user(is_staff=True)
        response = api_client.patch(f'/ielts/group_sessions/{groupsession.pk}/', {'description': 'blabla'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': groupsession.pk,
            'title': groupsession.title,
            'description': 'blabla',
            'teacher': []
        }


@pytest.mark.django_db
class TestDeleteGroupSession:
    def test_if_user_is_anonymous_returns_401(self, api_client):
       groupsession = baker.make(GroupSession)

       response = api_client.delete(f'/ielts/group_sessions/{groupsession.pk}/')

       assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user()
        response = api_client.delete(f'/ielts/group_sessions/{groupsession.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate_user):
        groupsession = baker.make(GroupSession)

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/group_sessions/{groupsession.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
