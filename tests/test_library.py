import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        library.Library_DB = Mock()
        library.Books_API  = Mock()
        self.lib = library.Library()
        self.author = "Rick Riordan"
        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/author_data.txt', 'r') as f:
            self.author_data = json.loads(f.read())



    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)


    def test_is_book_by_author(self):
        self.lib.api.get_ebooks = Mock(return_value=self.author_data)
        self.assertEqual(self.lib.is_book_by_author( ['rick riordan'], ["percy jackson 2"]), False)


    '''
    def test_get_langauges_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=self.json_data)
        book = self.lib.api.get_book_info('learning python')
        self.assertEqual(self.lib.
    '''