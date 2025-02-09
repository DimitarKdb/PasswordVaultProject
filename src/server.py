import socket
import threading

from commands.command import Command
from response.response import Response
from serverlog.logger import Logger
from commands.commandExecutor import CommandExecutor

class Server:
    """
    A multi-threaded server that handles client connections and processes commands.

    Attributes:
        server (socket.socket): The server socket.
        connectionsCount (int): The number of active client connections.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 5555) -> None:
        """
        Initializes the server, binds it to the given host and port, and starts listening for connections.

        :param host: The IP address to bind the server to.
        :param port: The port to listen on.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.connectionsCount = 0
        print(f"Server listening on {host}:{port}...")

    def handleClient(self, clientSocket: socket.socket, address: tuple[str, int]) -> None:
        """
        Handles communication with a connected client, processing commands until the connection is closed.

        :param clientSocket: The socket object for the connected client.
        :param address: The client's address (IP, port).
        """
        executor = CommandExecutor("")
        
        try:
            while True:
                message = clientSocket.recv(1024).decode()
                if not message:
                    break

                command = Command.fromJson(message)

                if command.commandType == "logout":
                    Logger.log(executor.currentUser, "logout", Response(True, f"User {executor.currentUser} has logged out!"))
                    executor = CommandExecutor("")
                    continue
                
                response = executor.executeOperation(command)

                if response.status and command.commandType in ("login", "register"):
                    executor = CommandExecutor(command.parameters[0])

                if response.status or command.commandType != "register":
                    Logger.log(executor.currentUser, command.commandType, response)
                           
                clientSocket.send(response.toJson().encode())
        finally:
            self.connectionsCount -= 1
            print(f"Client {address} has just closed their connection, active connections: {self.connectionsCount}")
            clientSocket.close()

    def start(self) -> None:
        """
        Starts the server, accepting client connections and handling them in separate threads.
        """
        while True:
            client, address = self.server.accept()
            
            self.connectionsCount += 1
            print(f"Accepted connection from {address}, active connections: {self.connectionsCount}")

            clientHandler = threading.Thread(target=self.handleClient, args=(client, address))
            clientHandler.start()

if __name__ == "__main__":
    server = Server()
    server.start()
