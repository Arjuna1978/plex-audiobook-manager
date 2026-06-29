import logging
from flask import Flask, render_template, request
from services.services import split_user_name
from services.api.dataSources.openLibraryConnector import getBookDetails 
from services.api.plex.plexConnector import plexAuth, listServers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)
app.logger.info("Starting Plex/Flask Application...")

try:
    plex_account = plexAuth()
    plex_server = plex_account.resource('Vijflix').connect()
    app.logger.info(f"Successfully connected")
    app.config['PLEX_SERVER'] = listServers(plex_account)
    
except Exception as e:
    app.logger.error(f"Failed to connect to Plex: {e}")
    app.config['PLEX_SERVER'] = None

@app.route("/")
def home():
    plex_account = plexAuth()
    app.config['PLEX_ACCOUNT'] = plex_account
    return render_template("home.html")

@app.route("/select_server", methods=["POST"])
def select_server():
    resource_name = request.form.get("resource_name")
    account = plexAuth()
    resouce = account.resource(resource_name).connect()
    app.config['RESOURCE'] = resouce
    app.config['RESOURCE_NAME'] = resource_name
    app.logger.info(f"User selected and connected to: {resource_name}")
    
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    server_name = session.get('selected_server')
    return f"You are currently connected to {server_name}"
if __name__ == "__main__":
    app.run(debug=True)