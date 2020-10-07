import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def cryptocurrency_listings(api_key, start=1, limit=10, convert='USD'):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': str(start),
        'limit': str(limit),
        'convert': convert,
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None
