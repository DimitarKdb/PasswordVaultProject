import socket
from commands.password.passwordSafetyChecker import SafetyChecker
from commands.command import Command
from response.response import Response

class EchoClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5555) -> None:
        """
        Initializes the EchoClient with a given host and port.
        
        :param host: The server's hostname or IP address.
        :param port: The server's port number.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.isLoggedIn: bool = False

    def initiateConnection(self) -> None:
        """
        Initiates the client connection and manages user authentication and commands.
        """
        self.promptWelcomeMessage()
        self.authenticateUser()

        try:
            while self.isLoggedIn:
                print("-----------------------------------------------------")
                message: str = input("$: ").strip()

                command = Command(userInput=message)
                command.commandType = command.commandType.lower()

                if command.commandType not in Command.getCommandsList() or command.commandType in ["login", "register"]:
                    print(f"Unsupported operation {command.commandType}! Please enter a valid command!")
                    continue

                if command.commandType == "disconnect":
                    self.client.send(Command("logout").toJson().encode())
                    break
                elif command.commandType == "help":
                    self.listCommands()
                    continue
                elif command.commandType == "logout":
                    self.isLoggedIn = False
                    self.client.send(Command("logout").toJson().encode())
                    self.authenticateUser()
                    continue

                if command.commandType in ["save-password", "update-entry"]:
                    response = self.checkSafety(command)
                    if not response.status:
                        print(response.description)
                        continue

                self.client.send(command.toJson().encode())
                responseJson: str = self.client.recv(1024).decode()
                responseDeserialized = Response.fromJson(responseJson)

                print(responseDeserialized.description)
                print("-----------------------------------------------------")
        finally:
            self.client.close()

    def checkSafety(self, command: Command) -> Response:
        """
        Checks the security of a password before saving or updating it.
        
        :param command: The command object containing the password parameters.
        :return: Response indicating whether the password is safe to proceed.
        """
        if len(command.parameters) < 3:
            return Response(False, "No password was provided!")

        securityStatusResponse = SafetyChecker.checkPasswordSecurity(command.parameters[2])

        if not securityStatusResponse.status:
            user_choice: str = ""
            while user_choice not in ("yes", "no"):
                user_choice = input(f"{securityStatusResponse.description} Do you want to save it anyway? (yes/no): ").strip().lower()

            if user_choice != "yes":
                return Response(False, "Password was not saved due to security concerns.")

        return Response(True, "Password is secure.")

    def authenticateUser(self) -> None:
        """
        Handles user authentication by prompting for login or registration.
        """
        while not self.isLoggedIn:
            self.initialPrompt()
            self.listAuthenticationCommands()

            consoleInput: str = input("$:").strip()

            command = Command(userInput=consoleInput)
            command.commandType = command.commandType.lower()

            if command.commandType == "disconnect":
                break

            if command.commandType not in ["login", "register"]:
                self.invalidActionPrompt()
                continue

            self.client.send(command.toJson().encode())
            answer: str = self.client.recv(1024).decode()

            response = Response.fromJson(answer)

            if response.status:
                self.isLoggedIn = True

            print(response.description)

    def promptWelcomeMessage(self) -> None:
        """
        Displays a welcome message to the user.
        """
        print("---------------------Welcome to PASSWORD-VAULT!---------------------")
        print("Use \"help\" to see the supported commands!")
    
    def listAuthenticationCommands(self) -> None:
        """
        Displays available authentication commands.
        """
        for comm in Command.getAuthenticationCommands():
            print(comm)
            
    def listCommands(self) -> None:
        """
        Lists all supported commands.
        """
        print("Supported commands:")
        for comm in Command.getCommandsDescription():
            print("> " + comm)

    def initialPrompt(self) -> None:
        """
        Displays an initial authentication prompt.
        """
        print("-----------------------------------------------------")
        print("Please log in to your account, or register if you do not have an account already!")

    def invalidActionPrompt(self) -> None:
        """
        Displays an error message for invalid authentication attempts.
        """
        print("Invalid action, please authenticate yourself first!")
        print("-----------------------------------------------------")

if __name__ == "__main__":
    client = EchoClient()
    client.initiateConnection()
