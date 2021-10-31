import unittest
from unittest.mock import Mock, call
from library import patron
from library.patron import InvalidNameException


class TestPatron(unittest.TestCase):

    def setUp(self):
        self.patron = patron.Patron("Nolan", "Porter", 69, 1234)
        self.patron2 = patron.Patron("Jacob", "Auger", 20, 4321)
        self.book = "Learning Python"

    def test_init(self):
        with self.assertRaises(InvalidNameException) as context:
            self.patron3 = patron.Patron("Nol4n", "Porter", 25, 2468)

        self.assertEqual("Name should not contain numbers", str(context.exception))

    def test_init_mutant(self):
        with self.assertRaises(InvalidNameException):
            self.patron3 = patron.Patron("Nolan", "8", 25, 2468)

    def test_get_borrowed_books(self):
        self.assertEqual(self.patron.get_borrowed_books(), [])

    def test_add_borrowed_book(self):
        self.patron.add_borrowed_book(self.book)
        self.assertEqual(self.patron.get_borrowed_books(), ["learning python"])

    def test_return_borrowed_book(self):
        self.patron.add_borrowed_book(self.book)
        self.patron.return_borrowed_book(self.book)
        self.assertEqual(self.patron.get_borrowed_books(), [])

    def test_get_fname(self):
        self.assertEqual(self.patron.get_fname(), "Nolan")

    def test_get_lname(self):
        self.assertEqual(self.patron.get_lname(), "Porter")

    def test_get_age(self):
        self.assertEqual(self.patron.get_age(), 69)

    def test_get_memberID(self):
        self.assertEqual(self.patron.get_memberID(), 1234)

    def test_eq(self):
        self.assertTrue(self.patron.__eq__(self.patron))

    def test_ne(self):
        self.assertTrue(self.patron.__ne__(self.patron2))
