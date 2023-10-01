import unittest
from unittest.mock import patch
from config import HandleCommand

class TestHandleCommand(unittest.TestCase):
    @patch('config.SearchCommand')
    @patch('importlib.import_module')
    @patch('importlib.reload')
    def test_command_found(self, mock_reload, mock_import_module, mock_search_command):
        mock_search_command.return_value = 'commands/test_command.py'
        mock_module = mock_import_module.return_value
        mock_class = mock_module.TestCommand
        result = HandleCommand('test_command')
        mock_reload.assert_called_once_with(mock_module)
        mock_import_module.assert_called_once_with('commands.test_command')
        mock_class.assert_called_once_with()
        self.assertEqual(result, mock_class.return_value)

    @patch('config.SearchCommand')
    def test_command_not_found(self, mock_search_command):
        mock_search_command.return_value = False
        result = HandleCommand('nonexistent_command')
        self.assertFalse(result)

    @patch('config.SearchCommand')
    @patch('importlib.import_module')
    @patch('importlib.reload')
    def test_class_not_found(self, mock_reload, mock_import_module, mock_search_command):
        mock_search_command.return_value = 'commands/test_command.py'
        mock_module = mock_import_module.return_value
        mock_class = mock_module.NonexistentClass
        mock_class.side_effect = AttributeError
        result = HandleCommand('test_command')
        mock_reload.assert_called_once_with(mock_module)
        mock_import_module.assert_called_once_with('commands.test_command')
        mock_class.assert_called_once_with()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()