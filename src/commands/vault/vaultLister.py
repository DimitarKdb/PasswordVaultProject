import os
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class VaultLister:
    @staticmethod
    def listVaults(user):
        """
        Lists all available vaults for the given user.

        :param user: The username whose vaults should be listed.
        :return: Response object containing the list of vaults or an error message.
        """
        vaultDirectory = os.path.join(VaultCreator.VAULTS_DIR, user)

        if not os.path.exists(vaultDirectory):
            return Response(False, f"No vaults found for user '{user}'.")

        vaults = [file.replace(".json", "") for file in os.listdir(vaultDirectory) if file.endswith(".json")]

        if not vaults:
            return Response(False, f"User '{user}' exists but has no saved vaults.")

        return Response(True, f"Available vaults: {', '.join(vaults)}")
