from .api import BaseApiClient
from .hello_objects import HelloSigner, HelloDoc
from querystring_parser.builder import build


class HelloSign(BaseApiClient):
    base_uri = 'https://api.hellosign.com/v3/'


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
            self.signers.append(signer)
        else:
            if not signer.validate():
                raise Exception("HelloSigner Errors %s" % (signers.errors,))
            else:
                raise Exception("add_signer signer must be an instance of class HelloSigner")

    def add_doc(self, doc):
        """ Simple dict of {'name': '@filename.pdf'}"""
        if isinstance(doc, HelloDoc) and doc.validate():
            self.docs.append(doc)
        else:
            if not doc.validate():
                raise Exception("HelloDoc Errors %s" % (doc.errors,))
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
        # 'file': []
        }

        for i,signer in enumerate(self.signers):
            data['signers'].append({'email_address': signer.data['email'], 'name': signer.data['name']})

        # for i,doc in enumerate(self.docs):
        #     data['file'].append('@' + doc.data['file_path'])

        data.update(self.params)

        return build(data)

    def files(self):
        files = []

        for i,doc in enumerate(self.docs):
            path = doc.data['file_path']
            name = doc.data['name']

            if name:
                doc_file = {'file': (name, open(path, 'rb'))}
            else:
                doc_file = {'file': open(path, 'rb')}

            files.append(doc_file)
        return files if len(files) > 0 else None

    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self.validate()

        return self.signature_request.send.post(auth=auth, data=self.data(), files=self.files(), **kwargs)