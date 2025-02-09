import hashlib
import requests
import os

from response.response import Response

class SafetyChecker:
    API_URL = "https://api.enzoic.com/v1/passwords"
    
    @staticmethod
    def get_api_key():
        """Fetch API key from an environment variable."""
        return os.getenv("ENZOIC_API_KEY")

    @staticmethod
    def checkPasswordSecurity(password: str):
        """
        Checks if a password has been exposed in data breaches using Enzoic API.
        """
        api_key = SafetyChecker.get_api_key()
        if not api_key:
            return Response(False, "API key is missing. Set ENZOIC_API_KEY in environment variables.")

        headers = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        }

        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        partialHash = hashedPassword[:10]

        try:
            response = requests.post(
                SafetyChecker.API_URL,
                headers=headers,
                json={"partialSHA256": partialHash}
            )

            if response.status_code == 429:
                return Response(False, "Too many requests. Please try again later.")

            if response.status_code != 200:
                return Response(False, f"Error checking password security: {response.text}")

            data = response.json()

            for candidate in data.get("candidates", []):
                if candidate["sha256"] == hashedPassword:
                    exposure_count = candidate.get('exposureCount', 0)
                    if exposure_count > 0:
                        return Response(False, f"This password has been exposed {exposure_count} times! Choose a stronger password.")

            return Response(True, "Password was checked and it is secure!")

        except requests.exceptions.RequestException as e:
            return Response(False, f"Network error while checking password security: {str(e)}")

        except Exception as e:
            return Response(False, f"Unexpected error: {str(e)}")
