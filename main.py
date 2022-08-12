import random
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import master_dict
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




@app.route("/")
def index():
    pass

@app.route("/playgame", methods=["POST"])
def playgame():
    pass

@app.route("/gameover", methods=["POST"])
def gameover():
    pass


if (__name__) == (__main__):
    app.run()