import json
import os
import random
import string

from cryptographing.crypting import Crypt
from commands.vault.vaultCreator import VaultCreator
from response.response import Response

class PasswordGenerator:
    @staticmethod
    def generateStrongPassword(length=16):
        """
        Generates a strong password containing uppercase, lowercase, numbers, and special characters.
        Filters out ambiguous characters.
        """
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
        characters = string.ascii_letters + string.digits + special_chars

        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def generate(user, command):
        """
        Generates a strong password and securely saves it in the user's vault.

        :param user: The username of the account owner.
        :param command: Command object with parameters [website, username, optional category]
        :return: Response object indicating success or failure.
        """
        if len(command.parameters) < 2:
            return Response(False, "Invalid parameters. Expected: website, username, [optional: category].")

        website = command.parameters[0]
        username = command.parameters[1]
        category = command.parameters[2] if len(command.parameters) > 2 else "default"

        generatedPassword = PasswordGenerator.generateStrongPassword()

        key = Crypt.generateKey(user)
        encryptedPassword = Crypt.encryptPassword(generatedPassword, key).decode()

        vaultDirectory = os.path.join(VaultCreator.VAULTS_DIR, user)
        vaultFile = os.path.join(vaultDirectory, f"{category}.json")

        createResponse = VaultCreator.createCategoryVault(user, category)
        if not createResponse.status:
            return createResponse  

        try:
            if os.path.exists(vaultFile):
                with open(vaultFile, "r") as file:
                    vaultData = json.load(file)
            else:
                vaultData = {}

            if website not in vaultData:
                vaultData[website] = []

            vaultData[website] = {
                "username": username,
                "password": encryptedPassword
            }

            with open(vaultFile, "w") as file:
                json.dump(vaultData, file, indent=4)

            return Response(True, f"Generated and saved a strong password for {website}.")

        except Exception as e:
            return Response(False, f"Error saving password: {str(e)}")
