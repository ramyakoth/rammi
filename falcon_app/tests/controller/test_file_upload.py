import hashlib
import mock
import pytest
import json

from falcon_app.storage import storage
from django.core.urlresolvers import reverse

    
@pytest.mark.django_db
def test_file_upload(client, test_user, tmpdir): #pylint: disable=unused-argument
    orig_getstorage = storage.get_storage
    storage.get_storage = mock.Mock()
    tfile = tmpdir.mkdir("test_dir").join("test_file.txt")
    tfile.write("test_data")
    file_path = str(tfile.realpath())
    
    client.login(username='test_user',password='test_password')
    with open(file_path,'rb') as fp:
        response = client.post(reverse('jfu_upload'),{'files[]':fp})
        j_data = str(response).split('\r\n\r\n')[1]
        file_name = json.loads(j_data)['files'][0]['name']
        assert file_name == 'test_file.txt'
    storage.get_storage = orig_getstorage

        
@pytest.mark.django_db
def test_file_storage_save(client, test_user, tmpdir): #pylint: disable=unused-argument
    orig_getstorage = storage.get_storage
    storage.get_storage = mock.Mock()
    store_obj = mock.Mock()
    storage.get_storage.return_value = store_obj
    mock_file = mock.Mock()
    store_obj.open.return_value = mock_file
    tfile = tmpdir.mkdir("test_dir").join("test_file.txt")
    tfile.write("test_data")
    file_path = str(tfile.realpath())
    
    client.login(username='test_user',password='test_password')
    with open(file_path,'rb') as fp:
        client.post(reverse('jfu_upload'),{'files[]':fp})
        fp.seek(0)
        f_name = hashlib.sha1(fp.read()).hexdigest()
        
        fp.seek(0)
        storage.get_storage.assert_called_with()
        store_obj.open.assert_called_with(f_name, 'w')
        mock_file.write.assert_called_with(fp.read())
        mock_file.close.assert_called_with()

    storage.get_storage = orig_getstorage

@pytest.mark.django_db
def test_file_upload_no_quota(client,test_user,test_doc, tmpdir): #pylint: disable=unused-argument
    test_doc.file_size = 1024
    test_doc.save()
    tfile = tmpdir.mkdir("test_dir").join("test_file.txt")
    tfile.write("test_data")
    file_path = str(tfile.realpath())
    
    client.login(username='test_user',password='test_password')
    with open(file_path,'rb') as fp:
        response = client.post(reverse('jfu_upload'),{'files[]':fp})

    assert 'Sorry insufficient storage'  in str(response.content)
