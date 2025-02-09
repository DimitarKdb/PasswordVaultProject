import os
import json
from cryptographing.crypting import Crypt
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class Login:
    """
    Handles user authentication by verifying stored encrypted credentials.
    """

    ACCOUNTS_FILE: str = VaultCreator.VAULTS_BASE_DIR + "/ApplicationStorage/accounts/accounts.json"

    @staticmethod
    def loginUser(command) -> Response:
        """
        Authenticates a user by checking the stored encrypted password.

        :param command: Command object containing parameters [username, password].
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) != 2:
            return Response(False, "Wrong parameters used with login command, expected <user> <password>!")

        username: str = command.parameters[0]
        password: str = command.parameters[1]

        if not os.path.exists(Login.ACCOUNTS_FILE):
            return Response(False, "No registered users found. Please register first.")

        try:
            with open(Login.ACCOUNTS_FILE, "r") as file:
                accounts: dict = json.load(file)
        except json.JSONDecodeError:
            return Response(False, "Error reading account data. The file may be corrupted.")

        if username not in accounts:
            return Response(False, f"User {username} was not found, please try again!")

        encrypted_password: str = accounts[username]["password"]

        encryptionKey: bytes = Crypt.generateKey(username)

        try:
            decryptedPassword: str = Crypt.decryptPassword(encrypted_password, encryptionKey)
        except Exception:
            return Response(False, "Failed to decrypt password. Possible data corruption.")

        if decryptedPassword == password:
            return Response(True, f"You have successfully logged in! Welcome, {username}!")

        return Response(False, "Wrong password, please try again!")
