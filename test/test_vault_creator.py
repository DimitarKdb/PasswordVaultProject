import pytest
import os
import json
from unittest.mock import patch, mock_open
from src.commands.vault.vaultCreator import VaultCreator
from src.response.response import Response
from src.commands.vault.vaultCategoryEnum import VaultCategoryEnum

@pytest.fixture
def mock_user():
    return "testUser"

@pytest.fixture
def mock_category():
    return VaultCategoryEnum.DEFAULT.value 

@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def testCreateVaultSuccess(mock_json_dump, mock_open_file, mock_exists, mock_makedirs, mock_user):
    """
    Test creating a new vault when it does not exist.
    """
    response = VaultCreator.createVault(mock_user)

    assert response.status is True
    assert f"Default vault created for user '{mock_user}'." in response.description

@patch("os.makedirs")
@patch("os.path.exists", return_value=True)
def testCreateVaultAlreadyExists(mock_exists, mock_makedirs, mock_user):
    """
    Test trying to create a vault when it already exists.
    """
    response = VaultCreator.createVault(mock_user)

    assert response.status is True
    assert f"Vault already exists for user '{mock_user}'." in response.description

@patch("os.makedirs", side_effect=Exception("Disk full"))
def testCreateVaultFailure(mock_makedirs, mock_user):
    """
    Test vault creation failure due to an exception.
    """
    response = VaultCreator.createVault(mock_user)

    assert response.status is False
    assert "Error creating vault for user" in response.description

@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def testCreateCategoryVaultSuccess(mock_json_dump, mock_open_file, mock_exists, mock_makedirs, mock_user, mock_category):
    """
    Test creating a category vault successfully.
    """
    response = VaultCreator.createCategoryVault(mock_user, mock_category)

    assert response.status is True
    assert f"Vault for category '{mock_category}' created successfully" in response.description

@patch("os.makedirs")
@patch("os.path.exists", return_value=True)
def testCreateCategoryVaultAlreadyExists(mock_exists, mock_makedirs, mock_user, mock_category):
    """
    Test creating a category vault that already exists.
    """
    response = VaultCreator.createCategoryVault(mock_user, mock_category)

    assert response.status is True
    assert f"Vault for category '{mock_category}' already exists" in response.description

@patch("os.makedirs", side_effect=Exception("Permission denied"))
def testCreateCategoryVaultFailure(mock_makedirs, mock_user, mock_category):
    """
    Test failure in creating a category vault due to an exception.
    """
    response = VaultCreator.createCategoryVault(mock_user, mock_category)

    assert response.status is False
    assert "Error creating vault for category" in response.description

def testCreateCategoryVaultInvalidCategory(mock_user):
    """
    Test creating a vault with an invalid category.
    """
    invalid_category = "unknown_category"
    response = VaultCreator.createCategoryVault(mock_user, invalid_category)

    assert response.status is False
    assert "Invalid category" in response.description
