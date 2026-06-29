import keyring
import logging

logger = logging.getLogger(__name__)

class TokenStorage:
    _instance = None  # Singleton pattern

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenStorage, cls).__new__(cls)
            cls._instance.use_keyring = cls._instance._check_keyring()
        return cls._instance

    def _check_keyring(self):
        try:
            keyring.get_keyring()
            logger.info("Keyring service detected")
            return True
        except Exception:
            logger.warning("key rign service not detected. Credentials will not be stored")
            return False
    def get_plex_token(self):
        if self.use_keyring:
            return keyring.get_password("plex_app", "my_token")
        return None # Explicitly return None if no storage is available

    def set_token(self, token):
        if self.use_keyring:
            keyring.set_password("plex_app", "my_token", token)
            logger.info("Token saved to secure keyring.")
        else:
            logger.warning("Keyring unavailable. Token NOT saved to disk.")