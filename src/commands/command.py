import json
from typing import List, Optional

class Command:
    """
    A class representing a command with a type and optional parameters.
    Commands can be initialized from user input or directly via parameters.
    """

    def __init__(self, commandType: Optional[str] = None, parameters: Optional[List[str]] = None, userInput: Optional[str] = None):
        """
        Initializes a Command object.

        :param commandType: The type of the command (e.g., "save-password").
        :param parameters: A list of parameters associated with the command.
        :param userInput: A raw input string from the user to be parsed into commandType and parameters.
        """
        if userInput:
            parts = userInput.strip().split()
            self.commandType: str = parts[0].lower() if parts else ""
            self.parameters: List[str] = parts[1:] if len(parts) > 1 else []
        else:
            self.commandType = commandType if commandType else ""
            self.parameters = parameters if parameters else []

    def __str__(self) -> str:
        """
        Returns a string representation of the Command object.

        :return: String describing the command type and its parameters.
        """
        return f"Command(type={self.commandType}, params={self.parameters})"

    def toJson(self) -> str:
        """
        Serializes the Command object into a JSON string.

        :return: JSON string representation of the command.
        """
        return json.dumps({"commandType": self.commandType, "parameters": self.parameters})

    @staticmethod
    def fromJson(json_str: str) -> "Command":
        """
        Deserializes a JSON string into a Command object.

        :param json_str: JSON string containing command data.
        :return: A Command object initialized from the JSON data.
        """
        data = json.loads(json_str)
        return Command(commandType=data["commandType"], parameters=data["parameters"])

    @staticmethod
    def getCommandsList() -> List[str]:
        """
        Returns a list of supported command types.

        :return: List of command names.
        """
        return [
            "help", "save-password", "generate-password", "get",
            "remove-all", "remove-specific", "list-category",
            "list-vaults", "update-entry", "logout", "disconnect"
        ]

    @staticmethod
    def getCommandsDescription() -> List[str]:
        """
        Returns a list of command descriptions with usage details.

        :return: List of command descriptions.
        """
        return [
            "help",
            "disconnect",
            "logout",
            "save-password <URL> <Username> <Password> [optional: Category]",
            "generate-password <URL>, <Username>, [optional: category].",
            "get <password/user/both> <URL> <Category>",
            "remove-all <URL>",
            "remove-specific <URL> <Username> <Category>",
            "list-category <Category>",
            "list-vaults",
            "update-entry <URL> <Username> <Password> <Category>"
        ]

    @staticmethod
    def getAuthenticationCommands() -> List[str]:
        """
        Returns a list of authentication commands.

        :return: List of authentication command descriptions.
        """
        return [
            "Login <user> <password>",
            "Register <user> <password> <confirm-password>"
        ]
