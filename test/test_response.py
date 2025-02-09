import pytest
import json
from src.response.response import Response

def testResponseInitialization():
    """
    Test initializing a Response object.
    """
    response = Response(True, "Operation successful")
    assert response.status is True
    assert response.description == "Operation successful"

def testResponseStr():
    """
    Test the string representation of the Response object.
    """
    response = Response(False, "Something went wrong")
    assert str(response) == "Status: Failure, Description: Something went wrong"

def testResponseToJson():
    """
    Test converting a Response object to a JSON string.
    """
    response = Response(True, "All good")
    json_str = response.toJson()
    expected_json = json.dumps({"status": True, "description": "All good"})
    assert json.loads(json_str) == json.loads(expected_json)

def testResponseFromJson():
    """
    Test creating a Response object from a JSON string.
    """
    json_str = '{"status": false, "description": "An error occurred"}'
    response = Response.fromJson(json_str)
    assert isinstance(response, Response)
    assert response.status is False
    assert response.description == "An error occurred"

def test_response_from_json_missing_fields():
    """
    Test handling missing fields when deserializing from JSON.
    """
    json_str = '{}'
    response = Response.fromJson(json_str)
    assert response.status is False
    assert response.description == "No description provided."

