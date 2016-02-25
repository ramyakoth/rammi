import abc
import os
import functools

from django.conf import settings

class AlreadyExists(Exception):
    """
    Raised when a user tries to store a file with a key that's already
    there in the storage.
    """
    pass

class NotFound(IOError):
    """
    Raised when a user tries to retrieve a file with a key that's not
    there in the storage.
    """
    pass

class Storage(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, location):
        """Initialises the storage container. 

        The location parameter specifies where the files will be
        stored. If this implementation stores it on the file system,
        it would be a base path. If it's an S3 backed storage, it
        would be an S3 bucket URL
        """
        self.location = location

    @abc.abstractmethod
    def open(self, key, mode):
        """
        Should return a handle to an open file managed by the Storage.
        """
        pass


    @abc.abstractmethod
    def delete(self, key):
        """
        Should delete the file with the given key.
        """
       

class StorageFile(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, location, mode):
        self.location = location
        self.mode = mode

    @abc.abstractmethod
    def write(self, data):
        "Writes the given data to the file"
        pass

    @abc.abstractmethod
    def read(self, size=None):
        """Reads at most size bytes from the file. Reads it all if size is
        unspecified."""
        pass

    @abc.abstractmethod
    def close(self):
        """
        Closes the file signalling that the file has been completely stored
        """
        pass
        
        

class FileStorage(Storage):
    def __init__(self, location):
        if not os.path.exists(location):
            os.makedirs(location)
        super(FileStorage, self).__init__(location)
        
    def open(self, key, mode):
        filename = os.path.join(self.location, key)
        if os.path.exists(filename):
            if mode == 'w':
                raise AlreadyExists('{} corresponds to an already existing file'.format(filename))
        else:
            if mode == 'r':
                raise NotFound('{} does not exist'.format(filename))
            
        handler = FileStorageHandle(filename, mode)
        return handler

    def delete(self, key):
        os.remove(os.path.join(self.location, key))


class FileStorageHandle(StorageFile):
   
    def __init__(self, location, mode):
        super(FileStorageHandle, self).__init__(location, mode)
        self.file_obj = open(location, mode)
        
    def write(self, data):
        self.file_obj.write(data)
   
    def read(self, size=None):
        data = self.file_obj.read(size)
        return data
    
    def close(self):
        self.file_obj.close()



def memoise(fn):
    fn.cache = {}
    @functools.wraps(fn)
    def memoised_fn(*largs, **kargs):
        key = largs + tuple(kargs.items())
        if key in fn.cache:
            return fn.cache[key]
        else:
            ret = fn(*largs, **kargs)
            fn.cache[key] = ret
            return ret
    return memoised_fn
    

@memoise
def get_storage():
    storage_class = getattr(__file__, settings.STORAGE_BACKEND['type'])
    file_store = storage_class(settings.STORAGE_BACKEND['location']) #pylint: disable=unused-variable

    return  file_store
