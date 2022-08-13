import os
import requests
import urllib.parse
from mm_dicts import countries, stocks, man_made
import random

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

random_num = random.randint(1, 2222)


def stock_check(symbol):
    """Gets current stock data for symbol."""

    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote/marketCap?token={api_key}"
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
        results = response.json()
    except requests.RequestException:
        return None
    print("\nBillionaire Data Processing:")
    for result in results:
        wealth = result["finalWorth"]
        fortune = int(float(wealth) * 1000000)
        dict[result["personName"]] = fortune
    print(dict)
    return dict


def crypto_check():
    """Gets current financial data for top cryptocurrencies."""
    dict = {}
    url = "https://api.coinlore.net/api/tickers/?start=0&limit=5"
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
    except requests.RequestException:
        return None
    print("\n Cryptocurrency Data Processing:")
    for result in results["data"]:
        cap = result["market_cap_usd"]
        total = round(float(cap))
        dict[result["name"]] = total
    print(dict)
    return dict


master_dictionary = {}
stock_caps = {}
billionaires = {}
cryptos = {}

print(stocks)
# Look up current stock price to get accurate marketcap valuations
for symbol in stocks:
    m_cap = stock_check(symbol)
    # creates new dictionary with {company name: market cap}
    stock_caps[stocks[symbol]] = m_cap[symbol]
print(stock_caps)

# Look up current net worth of top 10 billionaires
billionaires = billionaire_check()

# Look up current market cap for top 5 cryptocurrencies
cryptos = crypto_check()

master_dictionary = countries | man_made | stock_caps | billionaires | cryptos

# Testing for heroku run/update process
master_dictionary["random_number"] = random_num
print(f"Random num: {random_num}")
print(master_dictionary["random_number"])
print("INNER dictionary")
print(master_dictionary)



