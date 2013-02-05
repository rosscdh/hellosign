import os
import requests

try:
    import collections
except:
    raise Exception('You need to install ordereddict as you are running on an older version of python.')


class BaseApiClient(object):
    base_uri = None
    r = None
    _resources = []

    def __init__(self, *args, **kwargs):
        self._resources = []
        self.r = requests
        self.base_uri = self.base_uri if 'base_uri' not in kwargs else kwargs['base_uri']

    def __getattr__(self, key):
        self._resources.append(key)
        return self

    def __getitem__(self, key):
        self._resources.append(key)
        return self

    def __call__(self, **kwargs):
        """ As this is the last item called drop the final method call (get|put|post|head|option)"""
        self._resources = self._resources[:-1]
        return self

    def hasher(self):
        """ used to make php type hashes"""
        return collections.defaultdict(dict)

    @property
    def url(self):
        url = os.path.join(self.base_uri, *self._resources)
        return url

    def get(self, auth=None, **kwargs):
        return self.r.get(self.url, auth=auth, params=kwargs)

    def head(self, auth=None, **kwargs):
        return self.r.head(self.url, auth=auth, params=kwargs)

    def options(self, auth=None, **kwargs):
        return self.r.options(self.url, auth=auth, params=kwargs)

    def delete(self, auth=None, **kwargs):
        return self.r.delete(self.url, auth=auth, params=kwargs)

    def post(self, data=None, auth=None, files=None, **kwargs):
        return self.r.post(self.url, auth=auth, data=data, files=files, params=kwargs)

    def put(self, data=None, auth=None, files=None, **kwargs):
        return self.r.put(self.url, auth=auth, data=data, files=files, params=kwargs)