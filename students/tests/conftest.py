from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate_user(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate_user


@pytest.fixture
def create_new_instance(api_client):
    def do_create_new_instance(endpoint, instance):
        return api_client.post(endpoint, instance)
    return do_create_new_instance
