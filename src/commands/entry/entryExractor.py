import os
import json
from cryptographing.crypting import Crypt
from response.response import Response
from commands.vault.vaultCategoryEnum import VaultCategoryEnum
from commands.vault.vaultCreator import VaultCreator

class Extractor:
    @staticmethod
    def extractCredentials(user: str, command: object) -> Response:
        """
        Searches for the given URL in a specific user vault category and extracts username, password, or both.

        :param user: Username of the vault owner.
        :param command: Command object with parameters [fieldType, URL, category (optional)]
                        - fieldType: "user", "password", or "both".
                        - URL: The URL to search for.
                        - category: (Optional) The vault category to search in. Defaults to "default".
        :return: Response object with extracted credentials or failure message.
        """
        if len(command.parameters) < 2:
            return Response(False, "Invalid parameters. Expected: fieldType URL [category].")

        fieldType: str = command.parameters[0]
        url: str = command.parameters[1]
        category: str = command.parameters[2] if len(command.parameters) > 2 else "default"

        if fieldType not in ["password", "user", "both"]:
            return Response(False, "Wrong field type, expected: password/user/both")

        vaultPath: str = f"{VaultCreator.VAULTS_DIR}/{user}/{category}.json"

        if not os.path.exists(vaultPath):
            return Response(False, f"Vault '{category}' does not exist for user '{user}'.")

        key: bytes = Crypt.generateKey(user)

        try:
            with open(vaultPath, "r") as file:
                vaultData = json.load(file)

            if url in vaultData:
                storedData = dict(vaultData[url])
                extractedInfo = {}

                if fieldType in ["user", "both"]:
                    extractedInfo["username"] = storedData["username"]

                if fieldType in ["password", "both"]:
                    encryptedPassword: str = storedData["password"]
                    decryptedPassword: str = Crypt.decryptPassword(encryptedPassword, key)
                    extractedInfo["password"] = decryptedPassword

                responseMessage: str = f"Extracted credentials for {url}: {extractedInfo}"
                return Response(True, responseMessage)

        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return Response(False, "Error reading vault file.")

        return Response(False, f"No credentials found for {url} in category '{category}'.")
    
    @staticmethod
    def listUrlsInCategory(user: str, command: object) -> Response:
        """
        Lists all URLs stored in a given category.

        :param user: Username of the vault owner.
        :param command: Command object with parameters [category]
                        - category: The category whose URLs should be listed.
        :return: Response object with a list of URLs or failure message.
        """
        if len(command.parameters) != 1:
            return Response(False, "Invalid parameters count, expected: <Category>")
        
        category: str = command.parameters[0]
        validVaults: list = [command.value for command in VaultCategoryEnum]

        if category not in validVaults:
            return Response(False, f"Invalid vault category, valid categories: {validVaults}")

        vaultDirectory: str = f"{VaultCreator.VAULTS_DIR}/{user}"
        categoryFile: str = os.path.join(vaultDirectory, f"{category}.json")

        if not os.path.exists(vaultDirectory):
            return Response(False, "User vault does not exist.")

        if not os.path.exists(categoryFile):
            return Response(False, f"No vault found for category: {category}")

        try:
            with open(categoryFile, "r") as file:
                vaultData = json.load(file)

            urls: list = list(vaultData.keys())

            if not urls:
                return Response(False, f"No credentials stored in category: {category}")

            responseMessage: str = f"Stored URLs in {category}: {', '.join(urls)}"
            return Response(True, responseMessage)

        except json.JSONDecodeError:
            return Response(False, "Error reading vault file. It may be corrupted.")
