from src.commands.authentication.register import Register
from src.commands.authentication.login import Login
from src.response.response import Response
from unittest.mock import patch, mock_open

@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='{"newuser": {"password": "encrypted123"}}')
@patch("src.commands.authentication.login.Crypt.generateKey", return_value=b"key123")
@patch("src.commands.authentication.login.Crypt.decryptPassword", return_value="mypassword")
def testLoginUser(mock_decrypt, mock_key, mock_open_file, mock_exists):
    command = type("Command", (object,), {"parameters": ["newuser", "mypassword"]})
    response = Login.loginUser(command)

    assert response.status is True
    assert "successfully logged in" in response.description
    mock_open_file.assert_called()