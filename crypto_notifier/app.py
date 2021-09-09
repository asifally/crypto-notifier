from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from time import sleep


def get_ada_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
        'symbol': ['ada']
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv("API_KEY"),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    price = data.get('data').get('ADA').get('quote').get('USD').get('price')
    return price


def post_ifttt_webhook(event, value):
    data = {
        "value1": value
    }
    ifttt_webhook_url = f"https://maker.ifttt.com/trigger/{event}/with/key/{os.getenv('IFTTT_KEY')}"
    requests.post(url=ifttt_webhook_url, json=data)


def main():
    while True:
        price = get_ada_price()
        if price < 3.0:
            post_ifttt_webhook(event="ada_price_emergency", value=price)
        sleep(3 * 60) # 3 minutes


if __name__ == "__main__":
    main()