from urllib.parse import urlencode

#------------------------------------------------------------------------------

from kivy.network.urlrequest import UrlRequest

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

def cryptocurrency_listings(api_key, start=1, limit=10, convert='USD', cb=None):
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
    url += '?' + urlencode(parameters)
    req = UrlRequest(
        url=url,
        on_success=cb,
        on_redirect=cb,
        on_failure=cb,
        on_error=cb,
        req_headers=headers,
    )
    if cb:
        if _Debug:
            print('cryptocurrency_listings', req, cb)
        return req
    req.wait()
    if _Debug:
        print('cryptocurrency_listings', req.result)
    return req.result
