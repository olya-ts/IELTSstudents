from rest_framework import status
import pytest
import random
from model_bakery import baker
from students.models import Curator, Student


@pytest.mark.django_db
class TestRetrieveStudentList:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        students = baker.make('students.Student', _quantity=5, email=get_random_email)

        response = api_client.get('/ielts/students/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        students = baker.make(Student, _quantity=5, email=get_random_email)

        authenticate_user()
        response = api_client.get('/ielts/students/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        def get_random_email(email_list=['am@mail.ru', 'bm@mail.ru', 'cm@mail.ru', 'dm@mail.ru', 'em@mail.ru']):
            email = random.choice(email_list)
            email_list.remove(email)
            return email

        students = baker.make(Student, _quantity=5, email=get_random_email)

        authenticate_user(is_staff=True)
        response = api_client.get('/ielts/students/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveStudent:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        student = baker.make(Student)

        response = api_client.get(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user()
        response = api_client.get(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == student.first_name

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == student.first_name


@pytest.mark.django_db
class TestCreateStudent:
    def test_if_user_is_anonymous_returns_401(self, create_new_instance):
        response = create_new_instance(
            '/ielts/students/',
            {'course': 23, 'curator': 5, 'first_name': 'ghgj', 'last_name': 'nghj'}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_new_instance, authenticate_user):
        authenticate_user()
        response = create_new_instance(
            '/ielts/students/',
            {'course': 23, 'curator': 5, 'first_name': 'ghgj', 'last_name': 'nghj'}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_new_instance, authenticate_user):
        authenticate_user(is_staff=True)
        response = create_new_instance(
            '/ielts/students/',
            {'course': 23, 'curator': 5, 'first_name': 'ghgj', 'last_name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['last_name'] is not None


@pytest.mark.django_db
class TestModifyPartlyStudent:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        student = baker.make(Student)

        response = api_client.patch(f'/ielts/students/{student.pk}/', {'first_name': 'm'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user()
        response = api_client.patch(f'/ielts/students/{student.pk}/', {'first_name': 'm'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user(is_staff=True)
        response = api_client.patch(f'/ielts/students/{student.pk}/', {'first_name': 'm'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == student.pk


@pytest.mark.django_db
class TestDeleteStudent:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        student = baker.make(Student)

        response = api_client.delete(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user()
        response = api_client.delete(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate_user):
        student = baker.make(Student)

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/students/{student.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
