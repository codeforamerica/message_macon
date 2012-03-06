#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from mock import Mock

import sms
from app import app
from sms import process


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)

    def test_default_redirecting(self):
        rv = self.app.get('/issue')
        self.assertEquals(rv.status_code, 302)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEquals(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)


class ProcessTextMessage(unittest.TestCase):

    def setUp(self):
        sms.respond = Mock()
        sms.seeclickfix = Mock()

    def test_against_a_fake_text_message(self):
        text = {
            'senderAddress': 'tel:+478-555-5555',
            'message': 'This is a test.'
        }
        process(text)
        sms.respond.assert_called_with('478-555-5555')
        sms.seeclickfix.assert_called_with('This is a test.')


if __name__ == '__main__':
    unittest.main()
