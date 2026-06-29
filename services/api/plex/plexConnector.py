import plexapi.myplex
import logging
import time
import keyring
from keyring.errors import NoKeyringError
from plexapi.exceptions import Unauthorized, BadRequest, PlexApiException


logger = logging.getLogger(__name__)

def plexAuth(retry_count = 0):
    try:
        token = keyring.get_password("plex_app", "my_token")
        if (token):
            try:
                message = "Locally stored token found"
                account = plexapi.myplex.MyPlexAccount(token=token)
                logger.info(message)
                return [account]
            except Unauthorized:
                keyring.delete_password("plex_app", "my_token")
                message = "Expired token re-trying"
                logger.warning(message)
                return [plexPinAuth()]
            except BadRequest as e:
                if retry_count < 2:
                    retry_count += 1
                    message = f"[STATUS] Warning: Posible transient error. Retry {retry_count}/2 in 3 seconds..."
                    logger.warning(message)
                    time.sleep(3)
                    return plexAuth(retry_count=retry_count)
                else:
                    logger.error("Max retries reached. Failing.")
                    raise e
            
            except PlexApiException as e:
                logger.error(f"Exception Type: {type(e)}")
                logger.error(f"Has response? {hasattr(e, 'response')}")
                if hasattr(e, 'response'):
                    logger.error(f"Response Body: {e.response.text}")
            raise e


        else:
            message = ("New token created")
            return [plexPinAuth(),message]
    except NoKeyringError:
        print("Warning: Secure keyring not supported on this machine. Falling back to environment variables.")

def plexPinAuth():
    try:
        pinlogin = plexapi.myplex.MyPlexPinLogin(oauth=True)
        pinlogin.run()
        print(f'Login to Plex at the following url:\n{pinlogin.oauthUrl()}')
        pinlogin.waitForLogin()
        token = pinlogin.token
        keyring.set_password("plex_app", "my_token", token)
        account = plexapi.myplex.MyPlexAccount(token=token)
        return account

    except Exception as e:
        print(f"Failed to connect to Plex: {e}")
        keyring.delete_password("plex_app", "my_token")
    
def listServers (account_name: str):
    return [r for r in account_name.resources() if r.product == 'Plex Media Server']