import pytest


@pytest.mark.django_db
def test_login_true(client, add_user):
    '''Check whether user is logged in or not'''
    add_user('Bob', 'secret')
    value = client.login(username='Bob', password='secret')
    assert value == True


@pytest.mark.django_db
def test_login_false(client):
    ''' Check whether unknow user not logged in'''
    value = client.login(username='Unknown', password='notsecret')
    assert value == False
