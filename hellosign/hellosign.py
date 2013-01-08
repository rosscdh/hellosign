import requests
from wtforms import Form, TextField, validators

from . import BaseApiClient


class HelloSign(BaseApiClient):
    base_uri = 'https://api.hellosign.com/v3/'


class HelloSigner(Form):
    name = TextField('Name', [validators.Length(min=2, max=32)])
    email = TextField('Email Address', [validators.Length(min=6, max=128), validators.Email()])


class HelloDoc(Form):
    name = TextField('name', [validators.Length(min=1, max=25)])


class HelloSignSignature(HelloSign):
    params = {}
    signers = []
    docs = []

    def __init__(self, title, subject, message, *args, **kwargs):
        self.params = {}
        self.signers = []
        self.docs = []

        self.params['title'] = title
        self.params['subject'] = subject
        self.params['message'] = message

        super(HelloSignSignature, self).__init__(*args, **kwargs)

    def add_signer(self, signer):
        """ Simple dict of {'name': 'John Doe', 'email': 'name@example.com'}"""
        if isinstance(signer, HelloSigner) and signer.validate():
            self.signers.append(signer.data)
        else:
            raise Exception("add_signer signer must be an instance of class HelloSigner")

    def add_doc(self, doc):
        """ Simple dict of {'name': '@filename.pdf'}"""
        if isinstance(doc, HelloDoc) and doc.validate():
            self.docs.append(doc.data)
        else:
            raise Exception("add_doc doc must be an instance of class HelloDoc")

    def validate(self):
        if len(self.signers) == 0:
            raise AttributeError('You need to specify at least 1 person as a signer')
        if len(self.docs) == 0:
            raise AttributeError('You need to specify at least 1 document')

    def data(self):
        data = {
        'signers': [],
        'files': []
        }

        for i,signer in enumerate(self.signers):
            data['signers'].append({'email_address': signer['email'], 'name': signer['name']})

        for i,doc in enumerate(self.docs):
            data['files'].append(doc['name'])

        data.update(self.params)
        return data

    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self.validate()

        return self.signature_request.send.post(auth=auth, data=self.data(), **kwargs)