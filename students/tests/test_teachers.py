from rest_framework import status
import pytest
import random
from model_bakery import baker
from students.models import Teacher, GroupSession


@pytest.mark.django_db
class TestRetrieveTeacherList:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        teachers = baker.make(Teacher, _quantity=5, email=get_random_email)

        response = api_client.get('/ielts/teachers/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        teachers = baker.make(Teacher, _quantity=5, email=get_random_email)

        authenticate_user()
        response = api_client.get('/ielts/teachers/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        teachers = baker.make(Teacher, _quantity=5, email=get_random_email)

        authenticate_user(is_staff=True)
        response = api_client.get('/ielts/teachers/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveTeacher:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)

        response = api_client.get(f'/ielts/teachers/{teacher.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user()
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': teacher.pk,
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'phone': teacher.phone,
            'email': teacher.email,
            'skype_name': teacher.skype_name,
            'about_me': teacher.about_me,
            'groupsessions': []
        }

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': teacher.pk,
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'phone': teacher.phone,
            'email': teacher.email,
            'skype_name': teacher.skype_name,
            'about_me': teacher.about_me,
            'groupsessions': []
        }


@pytest.mark.django_db
class TestCreateTeacher:
    def test_if_user_is_anonymous_returns_401(self, create_new_instance):
        response = create_new_instance(
            '/ielts/teachers/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_new_instance, authenticate_user):
        authenticate_user()
        response = create_new_instance(
            '/ielts/teachers/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_new_instance, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_new_instance(
            '/ielts/teachers/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['phone'] is not None

    def test_if_data_is_valid_returns_201(self, create_new_instance, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_new_instance(
            '/ielts/teachers/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestModifyFullyTeacher:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)

        response = api_client.put(
            f'/ielts/teachers/{teacher.pk}/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user()
        response = api_client.put(
            f'/ielts/teachers/{teacher.pk}/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = api_client.put(
            f'/ielts/teachers/{teacher.pk}/',
            {'first_name': 'kdjsvk', 'last_name': 'kdzjbfv', 'phone': '215658', 'email': 'ka@mail.ru',
             'skype_name': 'kjdfj', 'about_me': 'ajf', 'groupsessions': []}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': teacher.pk,
            'first_name': 'kdjsvk',
            'last_name': 'kdzjbfv',
            'phone': '215658',
            'email': 'ka@mail.ru',
            'skype_name': 'kjdfj',
            'about_me': 'ajf',
            'groupsessions': []
        }


@pytest.mark.django_db
class TestModifyPartlyTeacher:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)

        response = api_client.patch(f'/ielts/teachers/{teacher.pk}/', {'groupsessions': []})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user()
        response = api_client.patch(f'/ielts/teachers/{teacher.pk}/', {'groupsessions': []})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = api_client.patch(f'/ielts/teachers/{teacher.pk}/', {'groupsessions': []})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': teacher.pk,
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'phone': teacher.phone,
            'email': teacher.email,
            'skype_name': teacher.skype_name,
            'about_me': teacher.about_me,
            'groupsessions': []
        }


@pytest.mark.django_db
class TestDeleteTeacher:
    def test_if_user_is_anonymous_returns_401(self, api_client):
       teacher = baker.make(Teacher)

       response = api_client.delete(f'/ielts/teachers/{teacher.pk}/')

       assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user()
        response = api_client.delete(f'/ielts/teachers/{teacher.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/teachers/{teacher.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
