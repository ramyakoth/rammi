import pytest
from falcon_app.models import User

@pytest.mark.django_db
def test_basic_database(add_user):
    add_user('john', 'passwd')
    test_user = User.objects.get(username='john')
    assert test_user.username == 'john'

