import os
import requests

from urlparse import urlparse

try:
    import collections
except:
    raise Exception('You need to install ordereddict as you are running on an older version of python.')


class BaseApiClient(object):
    base_uri = None
    r = None
    _url = None
    _resources = []

    def __init__(self, *args, **kwargs):
        self._resources = []
        self.r = requests

        self.base_uri = self.base_uri if 'base_uri' not in kwargs else kwargs['base_uri']
        self._url = None

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
        if self._url is None:
            self.url = '/'.join(self._resources)

        return self._url

    @url.setter
    def url(self, value):
        url = urlparse(value)
        if url.scheme in ['', None]:
            # no hostname was passed in
            path = value.split('/')
            self._url = os.path.join(self.base_uri, *path)
        else:
            # passed in a whole url
            self._url = value

    def get(self, url=None, auth=None, headers=None, **kwargs):

        if url is not None:  # allow override
            self.url = url

        return self.r.get(self.url, auth=auth, params=kwargs, headers=headers)

    def head(self, auth=None, data=None, files=None, headers=None, **kwargs):
        return self.r.head(self.url, auth=auth, data=data, files=files, params=kwargs, headers=headers)

    def options(self, auth=None, data=None, files=None, headers=None, **kwargs):
        return self.r.options(self.url, auth=auth, data=data, files=files, params=kwargs, headers=headers)

    def delete(self, auth=None, data=None, files=None, headers=None, **kwargs):
        return self.r.delete(self.url, auth=auth, data=data, files=files, params=kwargs, headers=headers)

    def post(self, auth=None, data=None, files=None, headers=None, **kwargs):
        return self.r.post(self.url, auth=auth, data=data, files=files, params=kwargs, headers=headers)

    def put(self, auth=None, data=None, files=None, headers=None, **kwargs):
        return self.r.put(self.url, auth=auth, data=data, files=files, params=kwargs, headers=headers)
