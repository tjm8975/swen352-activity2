import unittest
from unittest.mock import Mock, call
from library import library_db_interface

class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        library_db_interface.TinyDB = Mock()
        library_db_interface.Patron = Mock()
        library_db_interface.Query = Mock()
        self.db_interface = library_db_interface.Library_DB()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()
        get_fname_mock = Mock()
        get_lname_mock = Mock()
        get_age_mock = Mock()
        get_memberID_mock = Mock()
        get_borrowed_books_mock = Mock()

        patron_mock.get_fname = get_fname_mock
        patron_mock.get_lname = get_lname_mock
        patron_mock.get_age = get_age_mock
        patron_mock.get_memberID = get_memberID_mock
        patron_mock.get_borrowed_books = get_borrowed_books_mock
        self.db_interface.convert_patron_to_db_format(patron_mock)
        get_fname_mock.assert_called()
        get_lname_mock.assert_called()
        get_age_mock.assert_called()
        get_memberID_mock.assert_called()
        get_borrowed_books_mock.assert_called()