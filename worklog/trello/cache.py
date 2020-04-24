import errno
import hashlib
import os


class File:
    def __init__(self, url: str):
        path = '.cache'
        try:
            os.makedirs(path)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

        id_ = url.encode()
        id_ = hashlib.md5(id_).hexdigest()
        self._path = f'{path}/{id_}.json'

    def load(self):
        with open(self._path) as cache:
            return cache.read()

    def store(self, data: str):
        with open(self._path, 'w') as cache:
            cache.write(data)
