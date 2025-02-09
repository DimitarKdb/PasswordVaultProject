import pytest
import json
import os
from src.commands.entry.entryRemover import EntryRemover
from src.response.response import Response
from unittest.mock import patch, mock_open

@patch("os.path.exists", return_value=True)
@patch("os.listdir", return_value=["default.json"])
@patch("builtins.open", new_callable=mock_open, read_data='{"example.com": {"username": "user1", "password": "encrypted"}}')
def testRemoveAll(mock_open_file, mock_listdir, mock_exists):
    command = type("Command", (object,), {"parameters": ["example.com"]})
    response = EntryRemover.removeAll("testuser", command)

    assert response.status is True
    assert "Successfully removed all entries for 'example.com'" in response.description
    mock_open_file.assert_called()

@pytest.fixture
def mock_vault_data():
    return {
        "example.com": {"username": "testuser", "password": "encryptedpass"},
        "another.com": {"username": "otheruser", "password": "encryptedpass2"}
    }


