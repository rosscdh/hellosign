HelloSignApi
============

Basic Api Objects for accessing the HelloSign.com Api

Makes use of the excellent requests and nosetests and mocktests libs


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

    signature = HelloSignSignature()
    signature.add_signer(HelloSigner(**{'email':'bob@example.com', 'name': 'Bob Examplar'})
    signature.add_doc(HelloDoc(**{'name': '@filename.pdf'}))
    signature.create(auth=authentication)

    api = HelloSign()
    account_info = api.account.get()
    form_list = api.reusable_form.list.get()
    params = {...your params...}
    form_list = api.signature_request.send_with_reusable_form.post(params)


Tests
============

    nosetests -w tests/

