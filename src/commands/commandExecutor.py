from commands.authentication.login import Login
from commands.entry.entryExractor import Extractor
from commands.password.passwordGenerator import PasswordGenerator
from commands.entry.entryRemover import EntryRemover
from commands.password.passwordUpdater import PasswordUpdater
from commands.authentication.register import Register
from commands.entry.entrySaver import EntrySaver
from commands.vault.vaultCreator import VaultCreator
from commands.vault.vaultLister import VaultLister

class CommandExecutor:
    def __init__(self, user: str):
        """
        Initializes the CommandExecutor with the current user.

        :param user: The username of the currently logged-in user.
        """
        self.currentUser = user

    def executeOperation(self, command):
        """
        Executes the requested command based on command type.

        :param command: The command object containing the operation type and parameters.
        :return: Response object indicating the success/failure of the operation.
        """
        if command.commandType == "login":
            return Login.loginUser(command)
        elif command.commandType == "register":
            response = Register.registerUser(command)
            if response.status:
                VaultCreator.createVault(command.parameters[0])
            return response
        elif command.commandType == "save-password":
            return EntrySaver.savePassword(self.currentUser, command)
        elif command.commandType == "generate-password":
            return PasswordGenerator.generate(self.currentUser, command)
        elif command.commandType == "get":
            return Extractor.extractCredentials(self.currentUser, command)
        elif command.commandType == "remove-all":
            return EntryRemover.removeAll(self.currentUser, command)
        elif command.commandType == "remove-specific":
            return EntryRemover.removeSpecific(self.currentUser, command)
        elif command.commandType == "list-category":
            return Extractor.listUrlsInCategory(self.currentUser, command)
        elif command.commandType == "list-vaults":
            return VaultLister.listVaults(self.currentUser)
        elif command.commandType == "update-entry":
            return PasswordUpdater.updatePassword(self.currentUser, command)
