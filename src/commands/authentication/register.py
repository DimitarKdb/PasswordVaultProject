import os
import json
from cryptographing.crypting import Crypt
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class Register:
    """
    Handles user registration by storing encrypted credentials in a JSON file.
    """
    
    ACCOUNTS_FILE: str = VaultCreator.VAULTS_BASE_DIR + "/ApplicationStorage/accounts/accounts.json"

    @staticmethod
    def registerUser(command) -> Response:
        """
        Registers a new user by storing their encrypted password.

        :param command: Command object containing parameters [username, password, confirm-password].
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) != 3:
            return Response(False, "Wrong parameters were used when registering, expected <user> <password> <confirm-password>")

        username: str = command.parameters[0]
        password: str = command.parameters[1]
        confPassword: str = command.parameters[2]

        if password != confPassword:
            return Response(False, "<password> and <confirm-password> do not match!")

        accounts: dict = {}

        if os.path.exists(Register.ACCOUNTS_FILE):
            with open(Register.ACCOUNTS_FILE, "r") as file:
                try:
                    accounts = json.load(file)
                except json.JSONDecodeError:
                    accounts = {}

        if username in accounts:
            return Response(False, f"User {username} already exists!")

        encryptionKey: bytes = Crypt.generateKey(username)

        encryptedPassword: bytes = Crypt.encryptPassword(password, encryptionKey)

        accounts[username] = {"password": encryptedPassword.decode()}

        os.makedirs(os.path.dirname(Register.ACCOUNTS_FILE), exist_ok=True)
        
        with open(Register.ACCOUNTS_FILE, "w") as file:
            json.dump(accounts, file, indent=4)

        return Response(True, f"Registration successful! Welcome aboard, {username}!")
