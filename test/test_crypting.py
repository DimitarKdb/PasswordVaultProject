import pytest
import base64
import hashlib
from cryptography.fernet import Fernet
from src.cryptographing.crypting import Crypt

@pytest.fixture
def mock_username():
    return "testUser"

@pytest.fixture
def mock_password():
    return "securePassword123!"

@pytest.fixture
def encryption_key(mock_username):
    return Crypt.generateKey(mock_username)

def testGenerateKey(mock_username):
    """
    Test that generateKey returns a valid 32-byte base64-encoded key.
    """
    key = Crypt.generateKey(mock_username)
    assert isinstance(key, bytes)
    assert len(base64.urlsafe_b64decode(key)) == 32

def testEncryptDecryptPassword(mock_password, encryption_key):
    """
    Test that a password is correctly encrypted and decrypted.
    """
    encrypted_password = Crypt.encryptPassword(mock_password, encryption_key)
    assert isinstance(encrypted_password, bytes)

    decrypted_password = Crypt.decryptPassword(encrypted_password.decode(), encryption_key)
    assert decrypted_password == mock_password

def testDecryptWithWrongKey(mock_password, encryption_key):
    """
    Test that decryption with an incorrect key fails.
    """
    wrong_key = Crypt.generateKey("wrongUser")

    encrypted_password = Crypt.encryptPassword(mock_password, encryption_key)

    with pytest.raises(Exception):
        Crypt.decryptPassword(encrypted_password.decode(), wrong_key)
