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
        self.empty_book = "aabbcc"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())
        with open('tests_data/author_data.txt', 'r') as f:
            self.author_data = json.loads(f.read())
        with open('tests_data/empty_book_data.txt', 'r') as f:
            self.empty_book_data = json.loads(f.read())
        with open('tests_data/json_data_single.txt', 'r') as f:
            self.json_data_single = json.loads(f.read())

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
        self.api.make_request = Mock(return_value=self.empty_book_data)
        self.assertFalse(self.api.is_book_available(self.empty_book))

    def test_is_book_available_none(self):
        self.api.make_request = Mock(return_value=None)
        self.assertFalse(self.api.is_book_available(self.book))

    def test_is_book_available_single(self):
        self.api.make_request = Mock(return_value=self.json_data_single)
        self.assertTrue(self.api.is_book_available(self.book))

    def test_books_by_author(self):
        self.api.make_request = Mock(return_value=self.author_data)
        self.assertEqual(self.api.books_by_author(self.author), ["percy jackson 2"])

    def test_books_by_author_none(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.books_by_author(self.author), [])

    def test_get_book_info(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertNotEqual(self.api.get_book_info(self.book), [])

    def test_get_book_info_single(self):
        self.api.make_request = Mock(return_value=self.json_data_single)
        self.assertEqual(self.api.get_book_info(self.book), [{'title': 'Advanced Data Analytics Using Python: With '
                                                                       'Machine Learning, Deep Learning and NLP '
                                                                       'Examples', 'publisher': ["Apress"],
                                                              'publish_year': [2018], 'language': 'English'}])

    def test_get_book_info_empty(self):
        self.api.make_request = Mock(return_value=self.empty_book_data)
        self.assertEqual(self.api.get_book_info(self.empty_book), [])

    def test_get_book_info_none(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_book_info(self.empty_book), [])

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

    def test_get_ebooks_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(self.book), [])
