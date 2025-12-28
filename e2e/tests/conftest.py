import os
import pytest

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        if 'unusable_password' in kwargs:
             del kwargs['unusable_password']
             # create user with unusable password
             return django_user_model.objects.create_user(**kwargs)
        if 'password' not in kwargs:
             kwargs['password'] = 'password123'
        return django_user_model.objects.create_user(**kwargs)
    return make_user
