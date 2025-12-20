import jwt
import os
import datetime
import unittest
from unittest.mock import patch
from src.application.use_cases.login_user import SECRET_KEY as LOGIN_SECRET_KEY
from src.interfaces.web.server import SECRET_KEY as SERVER_SECRET_KEY

class TestAuthentication(unittest.TestCase):

    def test_secret_keys_are_consistent(self):
        """
        Tests if the secret key used for encoding and decoding are the same.
        """
        self.assertEqual(LOGIN_SECRET_KEY, SERVER_SECRET_KEY)

    def test_token_creation_and_validation_with_env_variable(self):
        """
        Tests that a token can be created and validated using the secret key from an environment variable.
        """
        test_secret = "testing_secret_key_123"

        with patch.dict(os.environ, {"SECRET_KEY": test_secret}):
            payload = {
                "sub": "12345",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            # Use the key as it is defined in the login use case
            token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")

            # Decode the token to verify it
            decoded_payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])

            self.assertEqual(decoded_payload["sub"], payload["sub"])

            # Test that decoding with the wrong key fails
            with self.assertRaises(jwt.InvalidTokenError):
                jwt.decode(token, "wrong_secret_key", algorithms=["HS256"])

if __name__ == '__main__':
    unittest.main()
