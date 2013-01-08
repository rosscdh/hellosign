import requests
from restkit import BasicAuth

from . import HelloClient


class HelloSign(HelloClient):
    base_uri = 'https://api.hellosign.com/v3/'
    url_path = None
    params = {}
    auth = None

    def __init__(self, *args, **kwargs):
        kwargs['base_uri'] = kwargs['base_uri'] if 'base_uri' in kwargs else self.base_uri

        super(HelloSign, self).__init__(*args, **kwargs)


class Signature(HelloSign):
    params = {}
    signers = []
    docs = []

    def __init__(self, title, subject, message, *args, **kwargs):
        self.params['title'] = title
        self.params['subject'] = subject
        self.params['message'] = message

        super(Signature, self).__init__(*args, **kwargs)

    def add_signer(self, signer):
        """ Simple dict of {'name': 'John Doe', 'email': 'name@example.com'}"""
        self.signers.append(signer)

    def add_doc(self, doc):
        """ Simple dict of {'name': '@filename.pdf'}"""
        self.docs.append(doc)

    def validate(self):
        if len(self.signers) == 0:
            raise AttributeError('You need to specify at least 1 person as a signer')
        if len(self.docs) == 0:
            raise AttributeError('You need to specify at least 1 document')

    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self.validate()

        return self.signature_request.send.post(auth=auth, data=self.params, **kwargs)