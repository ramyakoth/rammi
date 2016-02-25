from falcon_app.views import index

def test_index(client):
    '''Test to direct login page'''
    response = client.get('/')
    assert response.resolver_match.func == index
    assert response.status_code == 200
    
