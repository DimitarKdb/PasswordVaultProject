import json

class Response:
    """
    A class representing a standardized response for commands.
    
    Attributes:
        status (bool): Indicates if the response is successful (True) or failed (False).
        description (str): A message providing details about the response.
    """

    def __init__(self, status: bool, description: str) -> None:
        """
        Initializes a Response object.
        
        :param status: The status of the response (True for success, False for failure).
        :param description: A descriptive message for the response.
        """
        self.status: bool = status
        self.description: str = description

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the response.

        :return: A formatted string representing the response status and description.
        """
        return f"Status: {'Success' if self.status else 'Failure'}, Description: {self.description}"

    @staticmethod
    def fromJson(json_string: str) -> "Response":
        """
        Deserializes a JSON string into a Response object.

        :param json_string: The JSON-formatted string to deserialize.
        :return: A Response object with extracted values.
        """
        data = json.loads(json_string)
        status: bool = data.get("status", False)
        description: str = data.get("description", "No description provided.")
        
        return Response(status, description)

    def toJson(self) -> str:
        """
        Serializes the Response object into a JSON-formatted string.

        :return: A JSON string representing the response.
        """
        data = {
            "status": self.status,
            "description": self.description
        }
        return json.dumps(data)
