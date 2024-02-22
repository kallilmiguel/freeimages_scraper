#%%
import unittest
from unittest.mock import ANY, call, patch, MagicMock
from utils import insert_image_url

class TestImageURLInsertion(unittest.TestCase):
    @patch('utils.sqlite3')
    def test_insert_image_url(self, mock_sqlite):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_sqlite.connect.return_value = mock_conn

        insert_image_url('./db/mock_db', 'https://freeimages.com/dogs/a_little_dog')

        # Assert the cursor executed the expected SQL command
        mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, createdAt TIMESTAMP)")
        
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        
        # Assert the connection was closed
        self.assertTrue(mock_conn.close.called)

    @patch('utils.sqlite3')
    def test_insert_duplicate_image_url(self, mock_sqlite):
        """
        Test that inserting a duplicate URL does not raise an exception
        and does not duplicate entries in the database.
        """
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_sqlite.connect.return_value = mock_conn

        # URL to be tested for duplication
        test_url = 'https://freeimages.com/dogs/a_little_dog'

        # First insertion (to potentially create the entry)
        insert_image_url('./db/mock_db', test_url)

        # Second insertion of the same URL (to test handling of duplicates)
        insert_image_url('./db/mock_db', test_url)

        # Check that the database connection was established twice
        self.assertEqual(mock_sqlite.connect.call_count, 2)


        # Expected calls sequence
        expected_calls = [
            call("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, createdAt TIMESTAMP)"),
            call("INSERT OR IGNORE INTO images (url, createdAt) VALUES (?, ?)", (ANY, ANY)),
            call("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, createdAt TIMESTAMP)"),
            call("INSERT OR IGNORE INTO images (url, createdAt) VALUES (?, ?)", (ANY, ANY))
        ]
        
        # Verify that all expected calls were made in order
        mock_cursor.execute.assert_has_calls(expected_calls, any_order=False)
        
        # Ensure the commit method was called after each insert attempt
        self.assertEqual(mock_conn.commit.call_count, 2)
        
        # Ensure the connection was closed properly
        self.assertEqual(mock_conn.close.call_count, 2)



if __name__ == '__main__':
    unittest.main()
