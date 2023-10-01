import unittest
from unittest.mock import patch
from config import SearchCommand

class TestSearchCommand(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_command_found(self, mock_check_output):
        mock_check_output.return_value = 'commands/ping.py\n'
        result = SearchCommand('ping')
        self.assertEqual(result, 'commands/ping.py')

    @patch('subprocess.check_output')
    def test_command_not_found(self, mock_check_output):
        mock_check_output.return_value = ''
        result = SearchCommand('nonexistent_command')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()