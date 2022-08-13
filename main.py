import random
import os
import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from mm_dicts import countries, man_made
app = Flask(__name__)

# Configure app and sessions
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Postgres Database connected with Heroku
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create Database Model
class Highscores(db.Model):
    __tablename__ = 'highscores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)


class Marketdata(db.Model):
    __tablename = "marketdata"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.BigInteger, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    image_src = db.Column(db.Text)


db.Marketdata.marketdata.drop()
db.create_all()

# Debugging mode, temporarily allow hard-code dictionary
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
    "Largest Diamond Mine (By Reserve)": 604000000000, "1 Trillion Slices of Kraft Singles Cheese": 208300000000,
    "ALL of United Airlines Airplanes": 108000000000, "100 Million Years of Netflix Subscription": 37176000000,
    'Apple': 2707761004480, 'Microsoft': 2140564125101, 'Google': 80898990179, 'Amazon': 1432777709604,
    'Tesla': 898146518998, 'Meta Platforms': 506556482719, 'Visa': 465220320000, 'Exxon Mobil': 388382026331,
    'Coca-Cola': 273403056380, 'McDonald': 190756774025, 'AT&T': 128553040000, 'Netflix': 107223648442,
    'Starbucks': 100133598000, 'Target': 78642911645, 'Airbnb': 73197432000, 'Ford': 62518771547, 'Dell': 34462400000,
    'Zoom': 30905917284, "Kellog's": 25680000000, "American Airlines": 9740000000, 'Elon Musk': 255940425000,
    'Bernard Arnault & family': 174656024000, 'Jeff Bezos': 165114752000,
    'Gautam Adani & family': 130849543000, 'Bill Gates': 113133936000, 'Larry Ellison': 106393052000,
    'Warren Buffett': 102948495000, 'Larry Page': 101384351000, 'Sergey Brin': 98284195000,
    'Mukesh Ambani': 95705176000, 'Bitcoin': 457507207036, 'Ethereum': 229595181591, 'Tether': 66110192252,
    'USD Coin': 54252182355, 'Binance Coin': 53809039092
}

LIST_LENGTH = len(master_dictionary)
# Since questions require two choices, if list length is odd, take off one for more accurate counter check later on
if LIST_LENGTH % 2 != 0:
    LIST_LENGTH -= 1


@app.route("/", methods=["GET", "POST"])
def index():
    # Clear user session before start of game
    session.clear()

    if request.method == "POST":
        # Grab current data from db
        all_rows = db.session.query(Marketdata)
        print("\nStart query without .all()\n")
        print(all_rows)
        for row in all_rows:
            print(row)
        print("\n END! \n")

        # Test heroku run/update process
        all_rowss = db.session.query(Marketdata).all()
        print("\nStart query WITH .all()\n")
        print(all_rowss)
        for row in all_rowss:
            print(row)
        print("\n END! \n")

        # Start Game
        order = []
        session["counter"] = 0
        session["score"] = 0

        # randomize which choices get called, protecting against repeats
        for key in master_dictionary:
            order.append(key)
        random.shuffle(order)
        session["order"] = order

        # Grab two choices for user's first round and add to counter
        choice1 = session["order"][session["counter"]]
        session["counter"] += 1
        choice2 = session["order"][session["counter"]]
        session["counter"] += 1

        return render_template("playgame.html", choice1=choice1, choice2=choice2)

    # might need to add .amount before .desc()
    highscores = db.session.query(Highscores.name, Highscores.score).order_by(Highscores.score.desc())
    return render_template("index.html", highscores=highscores)


@app.route("/playgame", methods=["GET", "POST"])
def playgame():
    if request.method == "POST":
        # Check users answers
        answer = request.form.get("answer")
        other = request.form.get("other")

        # Protects against bugs or intentional client-side changes
        if answer not in master_dictionary or other not in master_dictionary:
            return render_template("404.html")

        if master_dictionary[answer] >= master_dictionary[other]:
            # Correct Answer!
            session["score"] += 1

            # Check if user has reached the end of the list
            if session["counter"] >= LIST_LENGTH:
                return render_template("winner.html")

            # Set up for next question
            choice1 = session["order"][session["counter"]]
            session["counter"] += 1
            choice2 = session["order"][session["counter"]]
            session["counter"] += 1
            return render_template("playgame.html", choice1=choice1, choice2=choice2)

        # Wrong Answer
        score = session["score"]
        return render_template("gameover.html", score=score)

    print("\nGET REQUEST\n")
    return render_template("playgame.html")


@app.route("/savescore", methods=["POST"])
def savescore():
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime('%m/%d/%Y')
    score = session["score"]
    name = request.form.get("name")
    if not name:
        # Means client side changed 'required' in input html
        name = "Nooblet"

    # Save score to database
    new_score = Highscores(name=name,
                           score=score,
                           timestamp=timestamp
                           )
    db.session.add(new_score)
    db.session.commit()

    return redirect("/")


if (__name__) == ("__main__"):
    app.run()
