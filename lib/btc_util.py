import requests

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
    result = {}
    json_response = response.json()
    if json_response:
        for tr in ((json_response.get('data', {}) or {}).get('list', []) or []):
            result[tr['hash']] = tr['balance_diff'] / 100000000.0
    return result


def verify_contract(contract_details, price_precision_matching_percent=1.0):
    expected_balance_diff_min = float(contract_details['btc_amount']) * (100.0 - price_precision_matching_percent) / 100.0
    expected_balance_diff_max = float(contract_details['btc_amount']) * (100.0 + price_precision_matching_percent) / 100.0
    if contract_details['contract_type'] == 'sales':
        expected_balance_diff_min *= -1
        expected_balance_diff_max *= -1
    btc_transactions = fetch_transactions(contract_details['buyer']['btc_address'])
    matching_count = 0
    for tr_balance_diff in btc_transactions.values():
        if tr_balance_diff > expected_balance_diff_max:
            continue
        if tr_balance_diff < expected_balance_diff_min:
            continue
        matching_count += 1
    return matching_count
