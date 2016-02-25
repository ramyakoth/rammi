import os
import pytest
import mock

from falcon_app.storage import storage

base_dir = os.path.dirname(__file__)



def test_storage_open_write_exists(monkeypatch):

    obj = storage.FileStorage('/tmp')

    mock_exists = mock.Mock()
    mock_exists.return_value = True
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    with pytest.raises(storage.AlreadyExists):
        obj.open('test_file', 'w')

    monkeypatch.undo()

def test_storage_open_read_notexists(monkeypatch):
    
    obj = storage.FileStorage('/tmp')

    mock_exists = mock.Mock()    
    mock_exists.return_value = False
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    with pytest.raises(storage.NotFound):
        obj.open('test_file', 'r')
        
    monkeypatch.undo()

def test_storage_open_write_notexists(monkeypatch):

    obj = storage.FileStorage('/tmp')

    mock_exists = mock.Mock()
    mock_exists.return_value = False
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    handle = obj.open('test_file', 'w')

    assert isinstance(handle, storage.FileStorageHandle)
    monkeypatch.undo()

def test_storage_open_read_exists(monkeypatch):
    mock_exists = mock.Mock()
    mock_exists.return_value = True
    monkeypatch.setattr(os.path, 'exists', mock_exists)

    obj = storage.FileStorage('/tmp')
    handle = obj.open('test_file', 'r')

    assert isinstance(handle, storage.FileStorageHandle)
    monkeypatch.undo()
