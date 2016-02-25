import pytest

@pytest.mark.django_db
def test_main_page(add_user,client):
    
    users = set()
    for i in range(10):
        users.add(add_user("user-{}".format(i), "passwd"))
    response = client.get('/users')
    assert response.templates[0].name == 'falcon_app/users.html'
    assert set(response.context['userlist']) == users
    


        
