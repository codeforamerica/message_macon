#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from mock import Mock

import sms
from app import app
from sms import process, find_address, AddressError


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

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)


class ProcessTextMessage(unittest.TestCase):

    def setUp(self):
        sms.respond = Mock()

    def test_fails_against_non_address_text_message(self):
        text = {
            'senderAddress': 'tel:+478-555-5555',
            'message': 'This is a test.'
        }
        self.assertRaises(AddressError, process, text)


class FindAddress(unittest.TestCase):

    def test_can_parse_out_an_address(self):
        text = "123 Any St. Broken garbage lid on trash can."
        response = find_address(text)
        expected = ('123 Any St Macon, GA', text)
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
