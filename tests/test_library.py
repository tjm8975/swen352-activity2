import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        library.Library_DB = Mock()
        library.Books_API = Mock()
        self.lib = library.Library()
        self.author = "Rick Riordan"
        self.book = "percy jackson 2"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/author_data.txt', 'r') as f:
            self.author_data = json.loads(f.read())

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=[])
        self.assertFalse(self.lib.is_ebook('learning python'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_get_ebooks_count_0(self):
        self.lib.api.get_ebooks = Mock(return_value=[])
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 0)

    def test_is_book_by_author(self):
        self.lib.api.books_by_author = Mock(return_value=[self.book])
        self.assertTrue(self.lib.is_book_by_author(self.author, self.book))

    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=[self.book])
        self.assertFalse(self.lib.is_book_by_author(self.author, "not by Rick Riordan"))

    def test_get_langauges_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=set())
        self.assertEqual(self.lib.get_languages_for_book(self.book), set())

    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=10)
        self.assertEqual(self.lib.register_patron("Nolan", "Porter", 20, 10), 10)

    def test_is_patron_registered(self):
        patron_mock = Mock()
        self.lib.db.retrieve_patron = Mock(return_value=patron_mock)
        self.assertTrue(self.lib.is_patron_registered(patron_mock))

    def test_is_patron_registered_none(self):
        patron_mock = Mock()
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(patron_mock))
