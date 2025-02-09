import json
import os

from cryptographing.crypting import Crypt
from response.response import Response
from commands.vault.vaultCreator import VaultCreator

class EntrySaver:
    @staticmethod
    def savePassword(currentUser: str, command) -> Response:
        """
        Saves a password to the appropriate vault file after checking security.

        :param currentUser: The username of the vault owner.
        :param command: Command object with parameters [place, userAccount, password, optional category].
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) < 3:
            return Response(False, "Invalid command. Expected at least 3 parameters (place, user, password).")

        place: str = command.parameters[0]  
        userAccount: str = command.parameters[1]
        password: str = command.parameters[2]
        category: str | None = command.parameters[3] if len(command.parameters) > 3 else None  

        if category:
            vaultResponse = VaultCreator.createCategoryVault(currentUser, category)
            if not vaultResponse.status:
                return vaultResponse  
            vaultFile = os.path.join(VaultCreator.VAULTS_DIR, currentUser, f"{category}.json")
        else:
            VaultCreator.createVault(currentUser)  
            vaultFile = os.path.join(VaultCreator.VAULTS_DIR, currentUser, "default.json")

        key: bytes = Crypt.generateKey(currentUser)
        encryptedPassword: str = Crypt.encryptPassword(password, key).decode()

        os.makedirs(VaultCreator.VAULTS_DIR, exist_ok=True)

        if not os.path.exists(vaultFile):
            with open(vaultFile, "w") as file:
                json.dump({}, file)

        with open(vaultFile, "r") as file:
            try:
                vaultData: dict = json.load(file)
            except json.JSONDecodeError:
                vaultData = {}

        vaultData[place] = {
            "username": userAccount,
            "password": encryptedPassword
        }

        with open(vaultFile, "w") as file:
            json.dump(vaultData, file, indent=4)

        return Response(True, f"Password for {place} saved successfully in {'default' if not category else category} vault.")
