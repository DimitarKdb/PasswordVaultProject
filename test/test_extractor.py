import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.commands.entry.entryExractor import Extractor
from src.response.response import Response

@pytest.fixture
def mock_vault_data():
    return {
        "example.com": {
            "username": "testUser",
            "password": "encryptedPassword123"
        }
    }

@pytest.fixture
def mock_command_extract():
    return type("Command", (), {"parameters": ["both", "example.com", "default"]})()

@pytest.fixture
def mock_command_list():
    return type("Command", (), {"parameters": ["default"]})()

@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists", return_value=True)
@patch("cryptographing.crypting.Crypt.generateKey", return_value=b"mock_key")
@patch("cryptographing.crypting.Crypt.decryptPassword", return_value="decryptedPassword123")
def testExtractCredentials(mock_decrypt, mock_key, mock_exists, mock_file, mock_vault_data, mock_command_extract):
    """
    Test extracting credentials from a vault.
    """
    mock_file.return_value.read.return_value = json.dumps(mock_vault_data)
    
    user = "testUser"
    response = Extractor.extractCredentials(user, mock_command_extract)

    assert response.status is True
    assert "Extracted credentials for example.com" in response.description

@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists", return_value=True)
def testListUrlsInCategory(mock_exists, mock_file, mock_vault_data, mock_command_list):
    """
    Test listing all stored URLs in a given vault category.
    """
    mock_file.return_value.read.return_value = json.dumps(mock_vault_data)

    user = "testUser"
    response = Extractor.listUrlsInCategory(user, mock_command_list)

    assert response.status is True
    assert "Stored URLs in default" in response.description
