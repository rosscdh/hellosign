HelloSignApi
============

Basic Api Objects for accessing the HelloSign.com Api

Makes use of the excellent requests, WTForms, nosetests and mocktests libs
as well as querystring-parser for encoding the requests in the required
HelloSign format.

1. Requests: http://docs.python-requests.org/en/latest/
2. WTForms: http://wtforms.simplecodes.com/docs/1.0.2/
3. nosetests: https://nose.readthedocs.org/en/latest/#
4. mocktests: http://gfxmonk.net/dist/doc/mocktest/doc/
5. querystring-parser:


Installation 
============

Into your virtualenv or system env:

    python setup.py install

or manually:

    git clone https://github.com/stard0g101/HelloSignApi.git
    cd HelloSignApi
    pip install -r requirements.txt


Usage
============
    from hellosign import HelloSign, HelloSignSignature
    from hellosign import HelloSigner, HelloDoc

    authentication = ("username@example.com", "secret_password")

    signature = HelloSignSignature(title='title', subject='My Subject', message='My Message')
    signature.add_signer(HelloSigner(**{'email':'bob@example.com', 'name': 'Bob Examplar'}))
    signature.add_doc(HelloDoc(**{'name': '@filename.pdf'}))
    signature.create(auth=authentication)

    api = HelloSign()
    account_info = api.account.get(auth=authentication)
    form_list = api.reusable_form.list.get()
    params = {...your params...}
    form_list = api.signature_request.send_with_reusable_form.post(auth=authentication, **params)


Tests
============

    nosetests -w tests/

