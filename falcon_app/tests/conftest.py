import pytest
from falcon_app.models import User, Document
import datetime

@pytest.fixture
def add_user():
    '''Fixture for add user'''
    def add_user_function(username, password):
        ''' function for fixture returne '''
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
    return add_user_function

@pytest.fixture
def test_user(add_user): #pylint: disable=redefined-outer-name
    '''Fixture to add specific user'''
    return add_user('test_user', 'test_password') 
        
@pytest.fixture
def test_doc(test_user): #pylint: disable=redefined-outer-name
    doc = Document(file_name='test_doc',
                          file_type='doc',
                          file_size=500,
                          upload_time=datetime.datetime.now(),
                          hash_address='afrasfasdf32Q',
                          owner=test_user
                          )
    doc.save()
    return doc
