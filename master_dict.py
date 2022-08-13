import os
import requests
import urllib.parse
import datetime
from mm_dicts import stocks
from main import Marketdata, db
import random

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

API_KEY = os.environ.get("API_KEY")
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime('%m/%d/%Y')
print(timestamp)
random_num = random.randint(1, 2222)


def google_check(symbol):
    """Manually calculates market cap for Google since normal IEX Api route returns oddly low valuations"""
    try:
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        price = float(quote["latestPrice"])
        # Google has roughly 13 billion shares
        market_cap = int(price * 13044000000)
        return {symbol: market_cap}
    except (KeyError, TypeError, ValueError):
        return None


def stock_check(symbol):
    """Gets current stock data for symbol."""
    try:
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote/marketCap?token={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {symbol: quote}
    except (KeyError, TypeError, ValueError):
        return None


def billionaire_check():
    """Gets current net worth for the richest billionaires."""
    dict = {}
    url = "https://forbes400.herokuapp.com/api/forbes400?limit=10"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse response
    try:
        results = response.json()
        for result in results:
            wealth = result["finalWorth"]
            fortune = int(float(wealth) * 1000000)
            dict[result["personName"]] = fortune
        return dict
    except (KeyError, TypeError, ValueError):
        return None


def crypto_check():
    """Gets current financial data for top cryptocurrencies."""
    dict = {}
    url = "https://api.coinlore.net/api/tickers/?start=0&limit=5"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse response
    try:
        results = response.json()
        for result in results["data"]:
            cap = result["market_cap_usd"]
            total = round(float(cap))
            dict[result["name"]] = total
        return dict
    except (KeyError, TypeError, ValueError):
        return None


payload = {}
stock_caps = {}
billionaires = {}
cryptos = {}

# Look up current stock price to get accurate marketcap valuations
for symbol in stocks:
    # IEX Stock data for market caps returns odd values for Google
    if symbol == "GOOG":
        m_cap = google_check(symbol)
    else:
        m_cap = stock_check(symbol)
    # creates new dictionary with {company name: market cap}
    stock_caps[stocks[symbol]] = m_cap[symbol]

# Look up current net worth of top 10 billionaires
billionaires = billionaire_check()

# Look up current market cap for top 5 cryptocurrencies
cryptos = crypto_check()

payload = stock_caps | billionaires | cryptos

# Test whether main.py receives updated table info
payload["random_num"] = random_num


print(payload)
# Clear table values
try:
    num_rows_deleted = db.session.query(Marketdata).delete()
    db.session.commit()
except:
    db.session.rollback()

# Create table objects from payload to batch update Marketdata
objects = []
for key in payload:
    objects.append(Marketdata(name=key, value=payload[key], timestamp=timestamp))


print(objects)

db.session.bulk_save_objects(objects)
db.commit()


# Batch update without deleting rows option
# Problems arise if a new entry comes along (new billionaire/crypto)
# db.query(Marketdata).filter(Marketdata.name.in_(payload)).update(
#     {Marketdata.value: case(payload, value=Marketdata.col1,)})






