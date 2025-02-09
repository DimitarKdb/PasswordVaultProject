from src.commands.authentication.register import Register
from src.commands.authentication.login import Login
from src.response.response import Response
from unittest.mock import patch, mock_open

@patch("os.path.exists", return_value=False)
@patch("builtins.open", new_callable=mock_open)
@patch("commands.authentication.register.Crypt.generateKey", return_value=b"key123")
@patch("commands.authentication.register.Crypt.encryptPassword", return_value=b"encrypted123")
def testRegisterUser(mock_encrypt, mock_key, mock_open_file, mock_exists):
    command = type("Command", (object,), {"parameters": ["newuser", "mypassword", "mypassword"]})
    response = Register.registerUser(command)

    assert response.status is True
    assert "Registration successful" in response.description
    mock_open_file.assert_called()
