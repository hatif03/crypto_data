import os
from dotenv import load_dotenv

load_dotenv()

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint

slug = "BTC,ETH,BNB,MATIC,SOL,USDC"

def pricemonitor():
  url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
  params = {
      "symbol": slug,
      "convert": "INR",
  }
  headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.getenv("API_KEY"),
  }

  # Starting session
  session = Session()
  session.headers.update(headers)

  # Getting data from API
  try:
    response = session.get(url, params=params)
    data = json.loads(response.text)["data"]
    result = []
    for term in slug.split(","):
        result.append(data_sort(data[term][0]))
    return list(result)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
    return(e)


def data_sort(coin_data):
  result = {
      "name": coin_data["name"],
      "symbol": coin_data["symbol"],
      "market_cap": coin_data["quote"]["INR"]["market_cap"],
      "price": coin_data["quote"]["INR"]["price"],
      "percent_change_1h": coin_data["quote"]["INR"]["percent_change_1h"]
  }
  return result