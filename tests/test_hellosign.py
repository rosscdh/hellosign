from nose.tools import *
from mocktest import *

import requests

from hellosign.hellosign import HelloSign, Signature


class TestHelloSign(mocktest.TestCase):
    def setUp(self):
        self.test_uri = 'http://example.com'
        self.auth = ('monkey', 'password')
        self.subject = HelloSign(base_uri=self.test_uri)

    def test_hellosign_init(self):
        eq_(self.subject.base_uri, self.test_uri)


class TestSignature(mocktest.TestCase):
    def setUp(self):
        self.test_uri = 'http://example.com'
        self.auth = ('monkey', 'password')

    def testInvalidSignature(self):
        self.assertRaises(TypeError, lambda: Signature(base_uri=self.test_uri))

    def testSignatureExceptions(self):
        subject = Signature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
    
        assert subject.base_uri == self.test_uri
    
        self.assertRaises(AttributeError, lambda: subject.create())
        subject.add_signer({})
    
        self.assertRaises(AttributeError, lambda: subject.create())
        subject.add_doc({})

    def testSignatureSend(self):
        subject = Signature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
        when(subject).create(auth=self.auth).then_return({})

        assert subject.base_uri == self.test_uri
        assert subject.params['title'] == 'title'
        assert subject.params['subject'] == 'My Subject'
        assert subject.params['message'] == 'My Message'

        subject.add_signer({})
        self.assertEqual(len(subject.signers), 1)
        subject.add_doc({})
        self.assertEqual(len(subject.docs), 1)

        response = subject.create(auth=self.auth)
        self.assertEqual(response, {})