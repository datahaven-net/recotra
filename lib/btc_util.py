import requests
import time
import datetime

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
    response = requests.get(url, headers={
        'User-Agent': 'curl/7.68.0',
        'Accept': '*/*',
    })
    result = {}
    json_response = response.json()
    if json_response:
        for tr in ((json_response.get('data', {}) or {}).get('list', []) or []):
            result[tr['hash']] = {
                'balance_diff': tr['balance_diff'] / 100000000.0,
                'block_time': tr['block_time'],
                'hash': tr['hash'],
            }
            if _Debug:
                print('fetch_transactions', tr['balance_diff'] / 100000000.0, 'at', time.asctime(time.localtime(tr['block_time'])))
    if _Debug:
        print('fetch_transactions found %d' % len(result))
    return result


def verify_contract(contract_details, price_precision_matching_percent=1.0, time_matching_seconds_before=0.0, time_matching_seconds_after=0.0):
    expected_balance_diff_min = float(contract_details['btc_amount']) * ((100.0 - price_precision_matching_percent) / 100.0)
    expected_balance_diff_max = float(contract_details['btc_amount']) * ((100.0 + price_precision_matching_percent) / 100.0)
    btc_transactions = fetch_transactions(contract_details['buyer']['btc_address'])
    contract_local_time = datetime.datetime.strptime('{} {}'.format(contract_details['date'], contract_details['time']), '%b %d %Y %I:%M %p')
    if _Debug:
        print('verify_contract', contract_local_time, expected_balance_diff_min, expected_balance_diff_max, )
    matching_transactions = []
    for tr_info in btc_transactions.values():
        balance_diff = tr_info['balance_diff']
        block_time = tr_info['block_time']
        block_local_time = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=block_time)
        diff_seconds = (block_local_time - contract_local_time).total_seconds()
        if _Debug:
            print('    %s %r : %r +/- %r [%r : %r]' % (
                contract_details['contract_type'], balance_diff, block_local_time, diff_seconds,
                -time_matching_seconds_before, time_matching_seconds_after, ))
        if time_matching_seconds_before:
            if diff_seconds < -time_matching_seconds_before:
                continue
        if time_matching_seconds_after:
            if diff_seconds > time_matching_seconds_after:
                continue
        if expected_balance_diff_min <= balance_diff and balance_diff <= expected_balance_diff_max:
            matching_transactions.append(tr_info)
    if _Debug:
        print('verify_contract', len(matching_transactions), len(btc_transactions))
    return matching_transactions
