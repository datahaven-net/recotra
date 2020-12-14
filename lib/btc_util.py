import requests

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

def parse_btc_url(inp):
    addr = inp
    if addr.lower().startswith('bitcoin:'):
        addr = addr[8:]
    params = ''
    if addr.count('?'):
        addr, _, params = addr.partition('?')
    result = {
        'address': addr,
    }
    if params:
        params = params.split('&')
        for p in params:
            key, _, value = p.partition('=')
            result[key] = value
    return result


#------------------------------------------------------------------------------

def fetch_transactions(btc_address):
    url = 'https://chain.api.btc.com/v3/address/{}/tx'.format(btc_address)
    response = requests.get(url)
    if _Debug:
        print('fetch_transactions', response.status_code, response.text)
    result = {}
    json_response = response.json()
    if json_response:
        for tr in ((json_response.get('data', {}) or {}).get('list', []) or []):
            result[tr['hash']] = tr['balance_diff'] / 100000000.0
    if _Debug:
        print('found such transactions:', list(result.values()))
    return result


def verify_contract(contract_details, price_precision_matching_percent=1.0):
    expected_balance_diff_min = float(contract_details['btc_amount']) * ((100.0 - price_precision_matching_percent) / 100.0)
    expected_balance_diff_max = float(contract_details['btc_amount']) * ((100.0 + price_precision_matching_percent) / 100.0)
    btc_transactions = fetch_transactions(contract_details['buyer']['btc_address'])
    matching_count = 0
    for tr_balance_diff in btc_transactions.values():
        balance_diff = tr_balance_diff
        if contract_details['contract_type'] == 'sales':
            balance_diff = tr_balance_diff * -1.0
        if expected_balance_diff_min <= balance_diff and balance_diff <= expected_balance_diff_max:
            matching_count += 1
    if _Debug:
        print('verify_contract', matching_count, expected_balance_diff_min, expected_balance_diff_max, len(btc_transactions))
    return matching_count
