import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
from services.api.plex.plexConnector import plexAuth, listServers, connectServer
from services.storage.dataBaseHandler import dataBaseHandler
from services.storage.libraryManager import LibraryManager
app = Flask(__name__)
app.secret_key = 'fdzgfdsgas_sdfg234t_vz_xcv_xcv'
db = dataBaseHandler()

library_mgr = LibraryManager()
library_mgr.ensure_default_user()

@app.route("/")
def home():
    app.config['CURRENT_USER'] = 'user'
    try:
        account = plexAuth()
        resources = listServers(account)
        return render_template("home.html", resources=resources)
    except Exception as e:
        app.logger.error(f"Failed to load servers: {e}")
        return "Failed to connect to Plex.", 500

@app.route("/select_server", methods=["POST"])
def select_server():
    resource_name = request.form.get("resource_name")
    user = app.config.get('CURRENT_USER')
    library_mgr.update_user_server(user, resource_name)
    try:
        account = plexAuth()
        resource_name,sections = connectServer(server=resource_name, account=account)
        app.config['RESOURCE_NAME'] = resource_name
        app.config['SECTIONS'] = sections
        return render_template("sections.html", sections=sections, resource_name=resource_name)
    except Exception as e:
        app.logger.error(f"Connection failed: {e}")
        return "Could not connect to server.", 500

@app.route("/select_section", methods=["POST"])
def select_section():
    selected_library = request.form.get("selected-library")
    print(f"Library Name: {selected_library} ")
    if selected_library:
        app.config['SELECTED_SECTION'] = selected_library
        return redirect(url_for('dashboard'))
    return "Section not found", 404

@app.route("/dashboard")
def dashboard():
    resource_name = app.config.get('RESOURCE_NAME', 'None')
    return f"You are currently connected to {resource_name}"

if __name__ == "__main__":
    app.run(debug=True)