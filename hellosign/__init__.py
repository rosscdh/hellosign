import os
import inspect
import requests


class HelloClient(object):
    base_uri = None
    _resources = []

    def __init__(self, *args, **kwargs):
        self.base_uri = None if 'base_uri' not in kwargs else kwargs['base_uri']

    def __getattr__(self, key):
        self._resources.append(key)
        return self

    def __getitem__(self, key):
        print key
        self._resources.append(key)
        return self

    def __call__(self, **kwargs):
        """ As this is the last item called drop the final method call (get|put|post|head|option)"""
        self._resources = self._resources[:-1]
        return self

    @property
    def url(self):
        url = os.path.join(self.base_uri, *self._resources)
        return url

    def get(self, auth=None, **kwargs):
        return requests.get(self.url, auth=auth, params=kwargs)

    def head(self, auth=None, **kwargs):
        return requests.head(self.url, auth=auth, params=kwargs)

    def options(self, auth=None, **kwargs):
        return requests.options(self.url, auth=auth, params=kwargs)

    def delete(self, auth=None, **kwargs):
        return requests.delete(self.url, auth=auth, params=kwargs)

    def post(self, data=None, auth=None, **kwargs):
        return requests.post(self.url, auth=auth, data=data, params=kwargs)

    def put(self, data=None, auth=None, **kwargs):
        return requests.put(self.url, auth=auth, data=data, params=kwargs)