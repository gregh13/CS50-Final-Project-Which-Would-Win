import os
import requests
import urllib.parse
from mm_dicts import countries, stocks, man_made

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


def stock_check(symbol):
    """Gets current stock data for symbol."""

    # Contact API
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
        print(f"\n\nQUOTE:\n\n{quote}\n\n")
        return {
            symbol: quote["marketCap"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        try:
            quote = response.json()
            return {symbol: quote}
        except:
            return None

market_caps = {}

for symbol in stocks:
    m_cap = stock_check(symbol)
    print(f"\nreturned value:\n{m_cap}\n")
    # creates new dictionary with {company name: market cap}
    market_caps[stocks["symbol"]] = m_cap[symbol]

print(market_caps)

