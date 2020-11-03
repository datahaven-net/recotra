
def clean_btc_address_input(inp):
    ret = inp
    if ret.lower().startswith('bitcoin:'):
        ret = ret[8:]
    if ret.count('?'):
        ret, _, _ = ret.partition('?')
    return ret
