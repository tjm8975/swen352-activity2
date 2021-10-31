import unittest
from unittest.mock import Mock, call
from library import library_db_interface
from library import patron


class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        library_db_interface.TinyDB = Mock()
        library_db_interface.Patron = Mock()
        library_db_interface.Query = Mock()
        self.db_interface = library_db_interface.Library_DB()

    def test_init(self):
        self.assertEqual(self.db_interface.DATABASE_FILE, 'db.json')

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        mock_data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                     'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=mock_data)
        self.db_interface.db.insert = Mock(side_effect=lambda data: None if data is None else 10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_insert_patron_none(self):
        self.assertEqual(self.db_interface.insert_patron(None), None)

    def test_insert_patron_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=patron_mock)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_get_patron_count(self):
        data = {1, 2, 3, 4, 5}
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_patron_count(), len(data))

    def test_get_all_patrons(self):
        data = {1, 2, 3, 4, 5}
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_all_patrons(), data)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_update_patron_none_data(self):
        convert_patron_mock = Mock()
        self.db_interface.convert_patron_to_db_format = convert_patron_mock
        self.db_interface.update_patron(Mock())
        convert_patron_mock.assert_called()

    def test_update_patron_not_equal(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.update = Mock()
        self.db_interface.update_patron(Mock())
        args = self.db_interface.db.update.call_args.args
        # No patrons in db yet, so query.memberID == patron.get_memberID() will be false
        self.assertEqual(args, (data, False))

    def test_update_patron_none(self):
        self.assertEqual(self.db_interface.insert_patron(None), None)

    def test_retrieve_patron_none(self):
        self.db_interface.db.search = Mock(return_value=None)
        self.assertEqual(self.db_interface.retrieve_patron(10), None)

    def test_retrieve_patron(self):
        data = [{'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 10,
                 'borrowed_books': []}]
        self.db_interface.db.search = Mock(return_value=data)
        self.assertNotEqual(self.db_interface.retrieve_patron(10), None)

    def test_close_db(self):
        db_close_mock = Mock()
        self.db_interface.db.close = db_close_mock
        self.db_interface.close_db()
        db_close_mock.assert_called()

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
