import pytest
import json
import os
from src.commands.entry.entrySaver import EntrySaver
from src.response.response import Response
from unittest.mock import patch, mock_open

@pytest.fixture
def mock_vault_dir(tmp_path):
    """Creates a temporary vault directory for testing."""
    vault_dir = tmp_path / "vaults"
    vault_dir.mkdir()
    return vault_dir

@patch("builtins.open", new_callable=mock_open, read_data="{}")
@patch("os.path.exists", return_value=True)
@patch("commands.vault.vaultCreator.VaultCreator.createCategoryVault", return_value=Response(True, "Created"))
@patch("commands.vault.vaultCreator.VaultCreator.createVault")
@patch("src.commands.entry.entrySaver.Crypt.generateKey", return_value=b"key123")
@patch("src.commands.entry.entrySaver.Crypt.encryptPassword", return_value=b"encrypted123")
def test_save_password(mock_encrypt, mock_key, mock_create_vault, mock_create_category, mock_exists, mock_file, mock_vault_dir):
    command = type("Command", (object,), {"parameters": ["example.com", "user1", "password123", "social"]})
    response = EntrySaver.savePassword("testuser", command)

    assert response.status is True
    assert "Password for example.com saved successfully" in response.description
    mock_file.assert_called()
