import pytest

@pytest.mark.django_db
def test_no_signup_button(client, test_user):
    u = test_user
    client.login(username=u.username, password='test_password')
    response = client.get('/dashboard')

    assert '<button type="button" class="btn">Sign Up </button>' not in response.content
    
    
