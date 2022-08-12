import random
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# from master_dict import master_dictionary

master_dictionary = {
    'Japan': 4912150000000, 'Germany': 4256540000000, 'United Kingdom': 3376000000000, 'India': 3534740000000,
    'France': 2936700000000, 'Italy': 2058330000000, 'Brazil': 1833270000000, 'Canada': 2221220000000,
    'Russia': 1829050000000, 'Korea': 1804680000000, 'Ireland': 516146000000, 'Greece': 222770000000,
    'Kenya': 114679000000, 'Croatia': 69459000000, 'Nepal': 36315000000, 'Cambodia': 28020000000,
    'Iceland': 27865000000, 'Jamaica': 15721000000, 'Mongolia': 18102000000, 'Maldives': 5502000000,
    'US Interstate Highway System': 535000000000, 'Great Wall of China (Estimate)': 260000000000,
    'International Space Station': 160000000000, '50 B-2 Stealth Bombers': 105000000000,
    '5 of the Most Expensive Aircraft Carrier': 65000000000, '200,000 Lambos': 60000000000,
    '30 Burj Khalifas (Tallest Building)': 45000000000, 'Most Expensive Airport (Osaka, Japan)': 29000000000,
    'ALL of the Royal Caribbean Cruise Ships': 25000000000, 'The Channel Tunnel (UK<-->FR)': 22400000000,
    'Apple': 2707761004480, 'Microsoft': 2140564125101, 'Google': 80898990179, 'Amazon': 1432777709604,
    'Tesla': 898146518998, 'Meta Platforms': 506556482719, 'Visa': 465220320000, 'Exxon Mobil': 388382026331,
    'Coca-Cola': 273403056380, 'McDonald': 190756774025, 'AT&T': 128553040000, 'Netflix': 107223648442,
    'Starbucks': 100133598000, 'Target': 78642911645, 'Airbnb': 73197432000, 'Ford': 62518771547, 'Dell': 34462400000,
    'Zoo': 30905917284, 'Elon Musk': 255940425000, 'Bernard Arnault & family': 174656024000, 'Jeff Bezos': 165114752000,
    'Gautam Adani & family': 130849543000, 'Bill Gates': 113133936000, 'Larry Ellison': 106393052000,
    'Warren Buffett': 102948495000, 'Larry Page': 101384351000, 'Sergey Brin': 98284195000,
    'Mukesh Ambani': 95705176000, 'Bitcoin': 457507207036, 'Ethereum': 229595181591, 'Tether': 66110192252,
    'USD Coin': 54252182355, 'Binance Coin': 53809039092
}

app = Flask(__name__)

# Configure app and sessions
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moneymatters.db")

# MAKE TABLES
# CREATE TABLE ............

print(master_dictionary)


@app.route("/", methods=["GET", "POST"])
def index():
    # Clear user session before start of game
    session.clear()

    highscores = [22, 8, 7, 6, 1]
    if request.method == "POST":

        # Clear out any previous store values
        session.clear()

        # Start Game
        order = []
        session["counter"] = 0
        session["score"] = 0

        # randomize which choices get called, protecting against repeats
        for key in master_dictionary:
            order.append(key)
        random.shuffle(order)
        session["order"] = order

        # Debugging
        print("\nsession list")
        print(session["order"])
        for key in session:
            print(f"Key: {key}  Value: {session[key]}")

        choice1 = session["order"][session["counter"]]
        session["counter"] += 1
        choice2 = session["order"][session["counter"]]
        session["counter"] += 1
        return render_template("playgame.html", choice1=choice1, choice2=choice2)
    return render_template("index.html", highscores=highscores)


@app.route("/playgame", methods=["GET", "POST"])
def playgame():
    if request.method == "POST":
        print("POST REQUEST")
        # Check users answers
        answer = request.form.get("answer")
        other = request.form.get("other")
        if answer or other not in master_dictionary:
            return
        return render_template("playgame.html")
    print("\nGET REQUEST\n")
    return render_template("playgame.html")

@app.route("/gameover", methods=["POST"])
def gameover():
    pass


if (__name__) == ("__main__"):
    app.run()