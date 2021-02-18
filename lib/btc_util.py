import requests
import datetime

import lib.btc_validator

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

LatestKnownBTCPrice = None

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

def clean_btc_amount(inp):
    if not inp:
        return '0.0'
    if isinstance(inp, float):
        inp = str(inp)
    if isinstance(inp, int):
        inp = str(inp)
    inp = inp.replace(',', '.')
    if inp.count('.') >= 2:
        inp = '.'.join(inp.split('.')[:2])
    return inp

#------------------------------------------------------------------------------

def fetch_transactions(btc_address):
    url = 'https://chain.api.btc.com/v3/address/{}/tx'.format(btc_address)
    try:
        response = requests.get(url, headers={
            'User-Agent': 'curl/7.68.0',
            'Accept': '*/*',
        })
        json_response = response.json()
    except Exception as exc:
        txt = ''
        try:
            txt = response.text
        except:
            pass
        if txt.count('Access denied'):
            txt = 'Access denied'
        else:
            txt = str(exc)
        if _Debug:
            print('fetch_transactions ERROR:', txt)
        return {}
    result = {}
    if json_response:
        for tr in ((json_response.get('data', {}) or {}).get('list', []) or []):
            result[tr['hash']] = {
                'balance_diff': tr['balance_diff'] / 100000000.0,
                'block_time': tr['block_time'],
                'hash': tr['hash'],
            }
    if _Debug:
        print('fetch_transactions found %d' % len(result))
    return result


def verify_contract(contract_details, price_precision_matching_percent=1.0, price_precision_fixed_amount=25, time_matching_seconds_before=0.0, time_matching_seconds_after=0.0):
    global LatestKnownBTCPrice
    expected_balance_diff_min = float(contract_details['btc_amount']) * ((100.0 - price_precision_matching_percent) / 100.0)
    expected_balance_diff_max = float(contract_details['btc_amount']) * ((100.0 + price_precision_matching_percent) / 100.0)
    expected_balance_fixed_diff_min = float(contract_details['btc_amount'])
    expected_balance_fixed_diff_max = float(contract_details['btc_amount'])
    if LatestKnownBTCPrice is not None:
        expected_balance_fixed_diff_min -= price_precision_fixed_amount / LatestKnownBTCPrice
        expected_balance_fixed_diff_max += price_precision_fixed_amount / LatestKnownBTCPrice
    btc_transactions = fetch_transactions(contract_details['buyer']['btc_address'])
    contract_local_time = datetime.datetime.strptime('{} {}'.format(contract_details['date'], contract_details['time']), '%b %d %Y %I:%M %p')
    if _Debug:
        print('verify_contract', contract_local_time, contract_details['btc_amount'], expected_balance_diff_min, expected_balance_diff_max,
              expected_balance_fixed_diff_min, expected_balance_fixed_diff_max)
    if not btc_transactions:
        if _Debug:
            print('NO TRANSACTIONS FOUND FOR THAT BTC ADDRESS', contract_details['buyer']['btc_address'], )
        return []
    matching_transactions = []
    for tr_info in btc_transactions.values():
        balance_diff = tr_info['balance_diff']
        block_time = tr_info['block_time']
        block_local_time = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=block_time)
        diff_seconds = (block_local_time - contract_local_time).total_seconds()
        if _Debug:
            print('    compare with %r %r %r' % (tr_info['hash'], block_local_time, balance_diff, ))
        if time_matching_seconds_before:
            if diff_seconds < -time_matching_seconds_before:
                continue
        if time_matching_seconds_after:
            if diff_seconds > time_matching_seconds_after:
                continue
        if (expected_balance_diff_min <= balance_diff and balance_diff <= expected_balance_diff_max) or (
            expected_balance_fixed_diff_min <= balance_diff and balance_diff <= expected_balance_fixed_diff_max):
            matching_transactions.append(tr_info)
    if _Debug:
        if len(matching_transactions) == 1:
            print('    SUCCESS', contract_local_time, contract_details['btc_amount'], expected_balance_diff_min, expected_balance_diff_max)
        else:
            print('    NO MATCHING TRANSACTIONS FOUND', contract_local_time, expected_balance_diff_min, expected_balance_diff_max, matching_transactions, )
    return matching_transactions


def validate_btc_address(inp):
    return lib.btc_validator.Validation.is_btc_address(inp)
