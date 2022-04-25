from rest_framework import status
import pytest
from model_bakery import baker
from model_bakery.recipe import Recipe
from datetime import date
from students.models import Teacher, Review


@pytest.mark.django_db
class TestRetrieveReviewList:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)
        reviews = baker.make(Review, teacher=teacher, _quantity=10)

        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        reviews = baker.make(Review, teacher=teacher, _quantity=10)

        authenticate_user()
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        reviews = baker.make(Review, teacher=teacher, _quantity=10)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        authenticate_user()
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == review.pk

    def test_if_user_is_admin_returns_200(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        authenticate_user(is_staff=True)
        response = api_client.get(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == review.pk

@pytest.mark.django_db
class TestCreateReview:
    def test_if_user_is_anonymous_returns_401(self, create_new_instance):
        teacher = baker.make(Teacher)

        response = create_new_instance(
            f'/ielts/teachers/{teacher.pk}/reviews/',
            {'name': 'kdjsvk', 'description': 'kdzjbfv'}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_201(self, create_new_instance, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user()
        response = create_new_instance(
            f'/ielts/teachers/{teacher.pk}/reviews/',
            {'name': 'kdjsvk', 'description': 'kdzjbfv'}
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, create_new_instance, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = create_new_instance(
            f'/ielts/teachers/{teacher.pk}/reviews/',
            {'name': '', 'description': 'kdzjbfv'}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_data_is_valid_returns_201(self, create_new_instance, authenticate_user):
        teacher = baker.make(Teacher)

        authenticate_user(is_staff=True)
        response = create_new_instance(
            f'/ielts/teachers/{teacher.pk}/reviews/',
            {'name': 'dfdaga', 'description': 'kdzjbfv'}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'dfdaga'


@pytest.mark.django_db
class TestDeleteReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        response = api_client.delete(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        authenticate_user()
        response = api_client.delete(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate_user):
        teacher = baker.make(Teacher)
        review = baker.make(Review, teacher=teacher)

        authenticate_user(is_staff=True)
        response = api_client.delete(f'/ielts/teachers/{teacher.pk}/reviews/{review.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT