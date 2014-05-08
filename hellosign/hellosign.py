from .api import BaseApiClient
from .hello_objects import HelloSigner, HelloDoc


class HelloSign(BaseApiClient):
    base_uri = 'https://api.hellosign.com/v3/'


class HelloSignSignature(HelloSign):
    kwargs = None
    params = {}
    signers = []
    docs = []

    def __init__(self, *args, **kwargs):
        # Reinitialze params always
        self.params = {}
        self.signers = []
        self.docs = []

        self.kwargs = kwargs

        self.params['title'] = kwargs.get('title')
        self.params['subject'] = kwargs.get('subject')
        self.params['message'] = kwargs.get('message')

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
        data = {}

        for i,signer in enumerate(self.signers):
            data['signers[%d][name]' % (i,)] = signer.data['name']
            data['signers[%d][email_address]' % (i,)] = signer.data['email']
            
        # Append the initial params
        data.update(self.params)

        return data

    def files(self):
        files = {
            'file': ()
        }

        for i, doc in enumerate(self.docs):
            path = doc.data['file_path']

            files['file'] = open(path, 'rb')

        return files

    def detail(self, signature_request_id, auth):
        return self.get(url='signature_request/%s' % signature_request_id, auth=auth)

    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self.validate()

        return self.signature_request.send.post(auth=auth, data=self.data(), files=self.files(), **kwargs)


class HelloSignEmbeddedDocumentSignature(HelloSignSignature):
    """
    Override the url to the embedded form as per emailed beta docs
    curl -u"EMAIL_ADDRESS:PASSWORD" https://api.hellosign.com/v3/signature_request/create_embedded \
         -F"client_id=YOUR_APP_CLIENT_ID" \
         -F"reusable_form_id=REUSABLE_FORM_ID" \
         -F"subject=My First embedded signature request with a reusable form" \
         -F"message=Isn't it cool" \
         -F"signers[ROLE_NAME][name]=John Doe" \
         -F"signers[ROLE_NAME][email_address]=john.doe@domain.com"
    """
    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self.validate()

        return self.signature_request.create_embedded.post(auth=auth, data=self.data(), files=self.files(), **kwargs)


class HelloSignEmbeddedDocumentSigningUrl(HelloSign):
    """
    Once you have sent a document for signing you also need to get "signing url"
    the signature_url returned in the original
    HelloSignEmbeddedDocumentSignature.request is NOT the signing url
    """
    signature_id = None

    def __init__(self, signature_id, *args, **kwargs):
        self.signature_id = signature_id
        super(HelloSignEmbeddedDocumentSigningUrl, self).__init__(*args, **kwargs)

    def create(self, **kwargs):
        """
        returns the JSON object
        {'embedded': {
          'sign_url': 'https://www.hellosign.com/editor/embeddedSign?signature_id={signature_id}&token={token}',
          'expires_at': {timestamp}
        }}        
        """
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        self._url = '%s%s%s' % (self.base_uri, 'embedded/sign_url/', self.signature_id)

        return self.embedded.sign_url.get(auth=auth, **kwargs)


class HelloSignUnclaimedDraftDocumentSignature(HelloSignSignature):
    """
    NB: from beta docs
    There is also a way to specify ahead of time who needs to signer and be CC'd.
    In this case the user won't be asked to input those values but only where they need to fill in the document.
    curl -u"API_KEY:" https://api.hellosign.com/v3/unclaimed_draft/create_embedded \
         -F"client_id=YOUR_APP_CLIENT_ID" \
         -F"requester_email_address=requester@example.com" \ 
         -F"file[0]=@FILE_PATH" \
         -F"file[1]=@ANOTHER_FILE_PATH" \
         -F"type=request_signature" \
         -F"subject=Embedded Signature Request" \ 
         -F"message=This is the message that goes along with your request." \ 
         -F"is_for_embedded_signing=1" \ ## Added by rosscdh for a mix we want embedded signing too
         -F"signers[0][name]=John Doe" \ 
         -F"signers[0][email_address]=john.doe@example.com" \ 
         -F"signers[1][name]=Jane Doe" \ 
         -F"signers[1][email_address]=jane.doe@example.com" \ 
         -F"cc_email_addresses[0]=some.guy@example.com",
         -F"test_mode=1"
    """
    def detail(self, claim_id, auth):
        raise NotImplementedError
        return self.get(url='unclaimed_draft/%s' % claim_id, auth=auth)

    def create(self, *args, **kwargs):
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del(kwargs['auth'])

        # not valid for this type of signature request
        del self.params['title']

        self.validate()

        kwargs.update({
            'type': 'request_signature',
            'is_for_embedded_signing': 1,
        })

        return self.unclaimed_draft.create_embedded.post(auth=auth, data=self.data(), files=self.files(), **kwargs)