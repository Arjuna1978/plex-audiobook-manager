from flask import Flask, render_template, request
# Import the service function from your services.py file
from services.services import split_user_name
from services.api.openLibraryConnector import getBookDetails

app = Flask(__name__)

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
