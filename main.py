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


db.create_all()

master_dictionary = countries | man_made


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


@app.route("/", methods=["GET", "POST"])
def index():
    # Clear user session before start of game
    session.clear()

    if request.method == "POST":
        # Set default value
        session["gameover"] = "false"

        # Grab current data from db
        all_rows = db.session.query(Marketdata).all()

        # Add data into master_dictionary
        for row in all_rows:
            master_dictionary[row.name] = row.value

        # Start Game
        order = []
        list_length = len(master_dictionary)

        # Since questions require two choices, if list length is odd, take off one for more accurate counter check
        if list_length % 2 != 0:
            list_length -= 1

        # Initialize session variables
        session["list_length"] = list_length
        session["counter"] = 0
        session["score"] = 0
        score = session["score"]
        session["master_dictionary"] = master_dictionary

        # Protection against rapid form submission (which racks up points)
        session["form_controller"] = 0
        f_con = session["form_controller"]

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

        return render_template("playgame.html", choice1=choice1, choice2=choice2,
                               score=score, f_con=f_con)

    # Get request, grab highscores and display on homepage
    highscores = db.session.query(Highscores.name, Highscores.score).order_by(Highscores.score.desc()).limit(10)
    return render_template("index.html", highscores=highscores)


@app.route("/playgame", methods=["GET", "POST"])
def playgame():
    if request.method == "POST":
        # Get users score
        score = session["score"]

        # Protects against using back button in browser
        if session["gameover"] == "true":
            return render_template("gameover.html", score=score)

        # Check users answers and form_controller (prevents multiple submission increase score bug)
        answer = request.form.get("answer")
        other = request.form.get("other")
        f_con = int(request.form.get("f_con"))

        if (f_con - 1) != session["form_controller"]:
            return render_template("404.html")

        # Protects against bugs or intentional client-side changes
        if answer not in session["master_dictionary"] or other not in session["master_dictionary"]:
            return render_template("404.html")

        if session["master_dictionary"][answer] >= session["master_dictionary"][other]:
            # Correct Answer! Update score values
            session["score"] += 1
            score = session["score"]

            # Protect against rapid form submission
            session["form_controller"] += 1
            f_con = session["form_controller"]

            # Check if user has reached the end of the list
            if session["counter"] >= session["list_length"]:
                return render_template("winner.html", score=score)

            # Set up for next question
            choice1 = session["order"][session["counter"]]
            session["counter"] += 1
            choice2 = session["order"][session["counter"]]
            session["counter"] += 1
            return render_template("playgame.html", choice1=choice1, choice2=choice2,
                                   score=score, f_con=f_con)
        # Wrong Answer
        session["gameover"] = "true"
        return render_template("gameover.html", score=score)
    print("GET REQUEST")
    return render_template("playgame.html")


@app.route("/savescore", methods=["POST"])
def savescore():
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime('%m/%d/%Y')
    score = session["score"]
    name = request.form.get("name")
    highscores = db.session.query(Highscores.name, Highscores.score).order_by(Highscores.score.desc()).limit(15)
    lowest = highscores[-1][1]

    if score < lowest:
        # Score is worse than the 15th highest score, not necessary to add to db as only top 10 scores show up
        return redirect("/")

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
