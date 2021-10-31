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
        self.book2 = "Learning Python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/author_data.txt', 'r') as f:
            self.author_data = json.loads(f.read())

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_mutant(self):
        self.lib.api.get_ebooks = Mock(return_value=[{'title': self.book2, 'ebook_count': 1}])
        self.assertTrue(self.lib.is_ebook(self.book2))

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

    def test_get_languages_for_book_mutant(self):
        self.lib.api.get_book_info = Mock(return_value=[{'language': "English"}])
        language = self.lib.get_languages_for_book(self.book)
        english = ['E', 'n', 'g', 'l', 'i', 's', 'h']
        for ch in language:
            if ch in english:
                english.remove(ch)
        self.assertEqual(english, [])

    def test_get_languages_mutant_81(self):
        self.lib.api.get_book_info = Mock(return_value=[{'language': "English"}])
        self.assertNotEqual(set(), self.lib.get_languages_for_book(self.book))

    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=10)
        self.assertEqual(self.lib.register_patron("Nolan", "Porter", 20, 10), 10)

    def test_register_patron_none(self):
        self.lib.db.insert_patron = Mock(side_effect=lambda patron: None if patron is None else
        10)
        self.assertEqual(self.lib.register_patron("Nolan", "Porter", 20, 10), 10)

    def test_is_patron_registered(self):
        patron_mock = Mock()
        self.lib.db.retrieve_patron = Mock(return_value=patron_mock)
        self.assertTrue(self.lib.is_patron_registered(patron_mock))

    def test_is_patron_registered_none(self):
        patron_mock = Mock()
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(patron_mock))

    def test_borrow_book(self):
        patron_mock = Mock()
        add_borrowed_book_mock = Mock()
        patron_mock.add_borrowed_book = add_borrowed_book_mock
        self.lib.borrow_book(self.book, patron_mock)
        add_borrowed_book_mock.assert_called()
        self.lib.db.update_patron.assert_called()

    def test_return_borrowed_book(self):
        patron_mock = Mock()
        return_borrowed_book_mock = Mock()
        patron_mock.return_borrowed_book = return_borrowed_book_mock
        self.lib.return_borrowed_book(self.book, patron_mock)
        return_borrowed_book_mock.assert_called()
        self.lib.db.update_patron.assert_called()

    def test_is_book_borrowed(self):
        patron_mock = Mock()
        get_borrowed_books_mock = Mock(return_value=self.book)
        patron_mock.get_borrowed_books = get_borrowed_books_mock
        self.assertTrue(self.lib.is_book_borrowed(self.book, patron_mock))
