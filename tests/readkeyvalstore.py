import unittest
from unittest.mock import mock_open, patch
from config import ReadKeyValStore

class TestReadKeyValStore(unittest.TestCase):
    def test_empty_file(self):
        with patch('builtins.open', mock_open(read_data='')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {})

    def test_comments_only(self):
        with patch('builtins.open', mock_open(read_data='# This is a comment\n# Another comment\n')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {})

    def test_single_key_value_pair(self):
        with patch('builtins.open', mock_open(read_data='key=value\n')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {'key': 'value'})

    def test_multiple_key_value_pairs(self):
        with patch('builtins.open', mock_open(read_data='key1=value1\nkey2=value2\nkey3=value3\n')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})

    def test_whitespace(self):
        with patch('builtins.open', mock_open(read_data='  key  =  value  \n')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {'key': 'value'})

    def test_no_value(self):
        with patch('builtins.open', mock_open(read_data='key=\n')) as mock_file:
            result = ReadKeyValStore('test.txt')
            self.assertEqual(result, {'key': ''})

    def test_no_key(self):
        with patch('builtins.open', mock_open(read_data='=value\n')) as mock_file:
            with self.assertRaises(ValueError):
                ReadKeyValStore('test.txt')

    def test_duplicate_key(self):
        with patch('builtins.open', mock_open(read_data='key=value1\nkey=value2\n')) as mock_file:
            with self.assertRaises(ValueError):
                ReadKeyValStore('test.txt')

if __name__ == '__main__':
    unittest.main()