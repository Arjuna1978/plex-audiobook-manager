import plexapi.myplex
import keyring

import requests

def plexAuth():
    token = keyring.get_password("plex_app", "my_token")
    if (token):
        message = ("Locally stored token found")
        account = plexapi.myplex.MyPlexAccount(token=token)
        if (account):
            return [account, message]
        else:
            keyring.delete_password("plex_app", "my_token")
            message = ("Expired token created")
            return [plexPinAuth(),message]
    else:
        message = ("New token created")
        return [plexPinAuth(),message]

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