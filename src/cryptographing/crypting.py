import base64
import hashlib
from cryptography.fernet import Fernet

class Crypt:
    """
    A utility class for encryption and decryption of passwords.
    Uses SHA-256 hashing and Fernet symmetric encryption.
    """

    @staticmethod
    def generateKey(username: str) -> bytes:
        """
        Generates an encryption key based on the username.

        :param username: The username used as the base for key generation.
        :return: A 32-byte base64-encoded encryption key.
        """
        salt: str = username[-1]
        keyMaterial: str = username + salt
        
        hashedKey: bytes = hashlib.sha256(keyMaterial.encode()).digest()
        
        return base64.urlsafe_b64encode(hashedKey[:32]) 

    @staticmethod
    def decryptPassword(encryptedPassword: str, key: bytes) -> str:
        """
        Decrypts an encrypted password using the given key.

        :param encryptedPassword: The encrypted password (base64 encoded).
        :param key: The encryption key used for decryption.
        :return: The decrypted password as a string.
        """
        fernet = Fernet(key)
        decryptedPassword: str = fernet.decrypt(encryptedPassword.encode()).decode()
        return decryptedPassword

    @staticmethod
    def encryptPassword(password: str, key: bytes) -> bytes:
        """
        Encrypts a given password using the provided key.

        :param password: The plaintext password to encrypt.
        :param key: The encryption key used for encryption.
        :return: The encrypted password as a byte string.
        """
        fernet = Fernet(key)
        encryptedPassword: bytes = fernet.encrypt(password.encode())
        return encryptedPassword
