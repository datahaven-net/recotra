
def clean_btc_address_input(inp):
    ret = inp.lower()
    if ret.startswith('bitcoin:'):
        ret = ret[8:]
    if ret.count('?'):
        ret, _, _ = ret.partition('?')
    return ret
