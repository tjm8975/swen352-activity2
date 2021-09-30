import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        self.author = "Rick Riordan"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())
        with open('tests_data/author_data.txt', 'r') as f:
            self.author_data = json.loads(f.read())

    def test_make_request_true(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value=Mock(status_code=200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_false(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value=Mock(status_code=100, **attr))
        self.assertEqual(self.api.make_request(""), None)

    def test_is_book_available_true(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertTrue(self.api.is_book_available(self.book))

    def test_is_book_available_false(self):
        self.api.make_request = Mock(return_value=dict())
        self.assertFalse(self.api.is_book_available(self.book))

    def test_is_book_available_none(self):
        self.api.make_request = Mock(return_value=None)
        self.assertFalse(self.api.is_book_available(self.book))

    def test_books_by_author(self):
        self.api.make_request = Mock(return_value=self.author_data)
        self.assertEqual(self.api.books_by_author(self.author), ["percy jackson 2"])

    def test_books_by_author_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.books_by_author(self.author), [])

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

    def test_get_ebooks_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(self.book), [])
