import mock
import __builtin__
from  falcon_app.storage import storage


def test_FileHandler_write(monkeypatch):
    mock_open = mock.Mock()
    mock_obj = mock.Mock()
    mock_open.return_value = mock_obj
    
    monkeypatch.setattr(__builtin__,'open',mock_open)
   

    file_object = storage.FileStorageHandle('a.txt','w')
    file_object.write('data')
    mock_obj.write.assert_called_with('data')

    monkeypatch.undo()



def test_FileHandler_read(monkeypatch):
    mock_open = mock.Mock()
    mock_obj = mock.Mock()
    mock_open.return_value = mock_obj
    monkeypatch.setattr(__builtin__,'open',mock_open)
    
    file_object = storage.FileStorageHandle('a.txt','r')
    file_object.read(size=100)
    mock_obj.read.assert_called_with(100)

    monkeypatch.undo()
