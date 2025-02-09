import os
import json
from response.response import Response
from commands.vault.vaultCategoryEnum import VaultCategoryEnum

class VaultCreator:
    VAULTS_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    VAULTS_DIR = os.path.join(VAULTS_BASE_DIR, "ApplicationStorage", "account_vaults")

    @staticmethod
    def createVault(username):
        """
        Creates a default vault for a user if it doesn't already exist.
        
        :param username: The username for which the vault should be created.
        :return: Response object indicating success or failure.
        """
        userVaultPath = os.path.join(VaultCreator.VAULTS_DIR, username)
        defaultFilePath = os.path.join(userVaultPath, "default.json")

        try:
            os.makedirs(userVaultPath, exist_ok=True)

            if not os.path.exists(defaultFilePath):
                with open(defaultFilePath, "w") as file:
                    json.dump({}, file, indent=4)

                return Response(True, f"Default vault created for user '{username}'.")
            
            return Response(True, f"Vault already exists for user '{username}'.")
        
        except Exception as e:
            return Response(False, f"Error creating vault for user '{username}': {str(e)}")

    @staticmethod
    def createCategoryVault(username: str, category_str: str) -> Response:
        """
        Creates a vault for a specific category within the user's vault directory.
        Only predefined categories (from VaultCategoryEnum) are allowed.

        :param username: The username for whom the category vault is being created.
        :param category_str: The category name as a string.
        :return: Response object indicating success or failure.
        """
        try:
            category_str = category_str.lower()
            category = VaultCategoryEnum(category_str)  # Ensure enum is validated
        except ValueError:
            allowedCategories = [cat.value for cat in VaultCategoryEnum]
            return Response(False, f"Invalid category. Allowed categories: {', '.join(allowedCategories)}")

        userVaultPath = os.path.join(VaultCreator.VAULTS_DIR, username)
        categoryFilePath = os.path.join(userVaultPath, f"{category.value}.json")

        try:
            os.makedirs(userVaultPath, exist_ok=True)

            if not os.path.exists(categoryFilePath):
                with open(categoryFilePath, "w") as file:
                    json.dump({}, file, indent=4)
                return Response(True, f"Vault for category '{category.value}' created successfully for user '{username}'.")
            else:
                return Response(True, f"Vault for category '{category.value}' already exists for user '{username}'.")
        
        except Exception as e:
            return Response(False, f"Error creating vault for category '{category.value}' for user '{username}': {str(e)}")
