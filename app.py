import plexapi.myplex
import keyring
from flask import Flask, render_template, request
# Import the service function from your services.py file
from services.services import split_user_name
from services.api.openLibraryConnector import getBookDetails 


app = Flask(__name__)

# check keyring for token
token = keyring.get_password("plex_app", "my_token")
if (token):
    print ("Locally stored token found")
    account = plexapi.myplex.MyPlexAccount(token=token)
    plex = account.resource('Vijflix').connect() 
    if(plex):
        print(f"Successfully connected to: {plex.friendlyName}")
        for section in plex.library.sections():
            print(f"Library Name: {section.title} | Type: {section.type} | ID: {section.key}")
    else:
        keyring.delete_password("plex_app", "my_token")
else:
# intialise plex connection
    try:
        pinlogin = plexapi.myplex.MyPlexPinLogin(oauth=True)
        pinlogin.run()
        print(f'Login to Plex at the following url:\n{pinlogin.oauthUrl()}')
        pinlogin.waitForLogin()
        token = pinlogin.token
        keyring.set_password("plex_app", "my_token", token)
        account = plexapi.myplex.MyPlexAccount(token=token)
        plex = account.resource('Vijflix').connect() 
        print(f"Successfully connected to: {plex.friendlyName}")
        for section in plex.library.sections():
            print(f"Library Name: {section.title} | Type: {section.type} | ID: {section.key}")

    except Exception as e:
        print(f"Failed to connect to Plex: {e}")
        keyring.delete_password("plex_app", "my_token")
        plex = None


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/show-name", methods=["POST"])
def show_name():
    # 1. Grab raw data from the web form submission
    raw_input = request.form.get("full_name_input", "")
    
    # 2. Call the imported service function at the appropriate time
    first, second = split_user_name(raw_input)
    data = getBookDetails (raw_input)

    
    # 3. Pass the clean result variables directly to your HTML view
    return render_template("display.html", first_name=first, second_name=second, book_data= data)

if __name__ == "__main__":
    app.run(debug=True)
