import os
import json
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class EntryRemover:
    @staticmethod
    def removeAll(user: str, command) -> Response:
        """
        Removes all entries with the given URL from every category.

        :param user: The username of the vault owner.
        :param command: Command object with parameters [URL]
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) != 1:
            return Response(False, "Wrong parameters given, expected <URL>")

        url: str = command.parameters[0]
        vaultDirectory: str = f"{VaultCreator.VAULTS_DIR}/{user}"

        if not os.path.exists(vaultDirectory):
            return Response(False, f"Vault directory does not exist for user '{user}'.")

        vaultsChecked: int = 0
        vaultsModified: int = 0

        for vaultFile in os.listdir(vaultDirectory):
            if not vaultFile.endswith(".json"):
                continue

            vaultPath: str = os.path.join(vaultDirectory, vaultFile)
            vaultsChecked += 1

            try:
                with open(vaultPath, "r") as file:
                    vaultData = json.load(file)

                if url in vaultData:
                    del vaultData[url]
                    with open(vaultPath, "w") as file:
                        json.dump(vaultData, file, indent=4)
                    vaultsModified += 1

            except (json.JSONDecodeError, FileNotFoundError):
                continue

        if vaultsModified > 0:
            return Response(True, f"Successfully removed all entries for '{url}' from {vaultsModified} vault(s).")
        elif vaultsChecked > 0:
            return Response(False, f"No entries found for '{url}' in any vault.")
        else:
            return Response(False, "No valid vaults found.")

    @staticmethod
    def removeSpecific(user: str, command) -> Response:
        """
        Removes a specific entry matching both URL and username from the specified category.

        :param user: The username of the vault owner.
        :param command: Command object with parameters [URL, Username, Category]
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) != 3:
            return Response(False, "Wrong parameters given, expected <URL> <Username> <Category>")
        
        url: str = command.parameters[0]
        username: str = command.parameters[1]
        category: str = command.parameters[2]

        vaultPath: str = f"{VaultCreator.VAULTS_DIR}/{user}/{category}.json"

        if not os.path.exists(vaultPath):
            return Response(False, f"Vault '{category}' does not exist for user '{user}'.")

        try:
            with open(vaultPath, "r") as file:
                vaultData = json.load(file)

            if url in vaultData and vaultData[url].get("username") == username:
                del vaultData[url]
                with open(vaultPath, "w") as file:
                    json.dump(vaultData, file, indent=4)
                return Response(True, f"Successfully removed entry for '{url}' with username '{username}' from '{category}'.")
            else:
                return Response(False, f"No matching entry found for '{url}' with username '{username}' in '{category}'.")

        except (json.JSONDecodeError, FileNotFoundError):
            return Response(False, "Failed to read or parse the vault file.")
