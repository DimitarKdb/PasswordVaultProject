import os
import datetime
from response.response import Response  # Assuming Response is used for status & description

class Logger:
    """
    A simple logging utility to record user actions, executed commands, and their responses.
    
    Attributes:
        BASE_DIR (str): The base directory of the script.
        LOG_FILE (str): The file path where logs are stored.
    """
    
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE: str = os.path.join(BASE_DIR, "ApplicationLogs", "logger.txt")

    @staticmethod
    def log(user: str, commandType: str, response: Response) -> None:
        """
        Logs user activity, command type, and response status in the log file.
        
        :param user: The username executing the command.
        :param commandType: The type of command executed.
        :param response: A Response object containing the status and description.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logEntry: str = (
            f"<LOG>\n   [{timestamp}] User: {user} | Command: {commandType} | "
            f"Status: {'Success' if response.status else 'Failed'} | Message: {response.description}\n<\\LOG>\n"
        )

        os.makedirs(os.path.dirname(Logger.LOG_FILE), exist_ok=True)  # Ensure log directory exists
        with open(Logger.LOG_FILE, "a") as logFile:
            logFile.write(logEntry)

    @staticmethod
    def readLogs() -> str:
        """
        Reads and returns the content of the log file.

        :return: The contents of the log file as a string, or a message if the log file does not exist.
        """
        if not os.path.exists(Logger.LOG_FILE):
            return "Log file is empty."
        
        with open(Logger.LOG_FILE, "r") as logFile:
            return logFile.read()
