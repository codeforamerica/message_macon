#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from mock import Mock

import sms
from sms import process, find_address, AddressError


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
        expected = ('123 Any St Macon, GA', 'Broken garbage lid on trash can.')
        self.assertEqual(response, expected)

    def test_can_parse_out_a_long_description(self):
        text = "123 Any St. Broken something. Another something.  More stuff."
        response = find_address(text)
        expected = (
            '123 Any St Macon, GA',
            'Broken something. Another something. More stuff.'
        )
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
