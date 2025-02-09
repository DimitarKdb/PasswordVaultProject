import os
import json
from cryptographing.crypting import Crypt
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class PasswordUpdater:
    @staticmethod
    def updatePassword(user: str, command) -> Response:
        """
        Updates a password entry for a given URL and username in the specified category.

        :param user: The username of the vault owner.
        :param command: Command object containing parameters [URL, Username, New Password, Category].
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) != 4:
            return Response(False, "Invalid parameters. Expected: <URL> <Username> <New Password> <Category>.")

        url: str = command.parameters[0]
        username: str = command.parameters[1]
        newPassword: str = command.parameters[2]
        category: str = command.parameters[3]

        vaultPath: str = f"{VaultCreator.VAULTS_DIR}/{user}/{category}.json"

        if not os.path.exists(vaultPath):
            return Response(False, f"Vault '{category}' does not exist for user '{user}'.")

        try:
            with open(vaultPath, "r") as file:
                vaultData: dict = json.load(file)

            if url not in vaultData:
                return Response(False, f"No entry found for '{url}' in '{category}'.")

            if dict(vaultData[url]).get("username") != username:
                return Response(False, f"No matching username '{username}' found for '{url}' in '{category}'.")

            key: bytes = Crypt.generateKey(user)
            encryptedPassword: str = Crypt.encryptPassword(newPassword, key).decode()

            vaultData[url]["password"] = encryptedPassword

            with open(vaultPath, "w") as file:
                json.dump(vaultData, file, indent=4)

            return Response(True, f"Successfully updated password for '{username}' under '{url}' in '{category}'.")

        except (json.JSONDecodeError, FileNotFoundError):
            return Response(False, "Failed to read or update the vault file.")
