import pytest
import os
from unittest.mock import patch
from src.commands.vault.vaultLister import VaultLister
from src.response.response import Response

@pytest.fixture
def mock_user():
    return "testUser"

@patch("os.path.exists", return_value=True)
@patch("os.listdir", return_value=["social.json", "work.json"])
def testListVaultsSuccess(mock_listdir, mock_exists, mock_user):
    """
    Test listing vaults when user has saved vaults.
    """
    response = VaultLister.listVaults(mock_user)

    assert response.status is True
    assert "Available vaults: social, work" in response.description

@patch("os.path.exists", return_value=True)
@patch("os.listdir", return_value=[])
def testListVaultsEmpty(mock_listdir, mock_exists, mock_user):
    """
    Test listing vaults when user exists but has no saved vaults.
    """
    response = VaultLister.listVaults(mock_user)

    assert response.status is False
    assert f"User '{mock_user}' exists but has no saved vaults." in response.description

@patch("os.path.exists", return_value=False)
def testListVaultsNoUser(mock_exists, mock_user):
    """
    Test listing vaults when the user has no vault directory.
    """
    response = VaultLister.listVaults(mock_user)

    assert response.status is False
    assert f"No vaults found for user '{mock_user}'." in response.description
