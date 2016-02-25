import pytest
from falcon_app.models import User
from falcon_app.views import profile
from django.contrib.auth.views import login



@pytest.mark.django_db
def test_update_profile_true(client, add_user):
    ''' Test for profile update '''
    add_user('Bob', 'secret')
    client.login(username='Bob', password='secret')
    response = client.get('/profile')
    # assert response.templates[0].name == 'falcon_app/profileupdate.html'
    assert response.status_code == 200
    assert response.resolver_match.func == profile


@pytest.mark.django_db
def test_update_profile_anonymous(client):
    '''Checks whether anonymous users are redirected to login page.'''
    response = client.get('/profile', follow=True)
    # assert response.templates[0].name == 'registration/login.html'
    assert response.resolver_match.func == login
    assert response.status_code == 200


@pytest.mark.django_db
def test_save_data(client, add_user):
    ''' Checks whether user can update data or not '''
    add_user('test1', 'secret')
    client.login(username='test1', password='secret')
    client.post('/profile', {'first_name':'testNew',
                             'last_name':'testLast',
                             'email':'test@example.com',
                             'quota':2048
                         })
    test_user = User.objects.get(username='test1')
    assert test_user.first_name == 'testNew'
    assert test_user.last_name == 'testLast'
    assert test_user.email == 'test@example.com'
    assert test_user.quota == 2048
