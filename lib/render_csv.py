import csv
import tempfile

#------------------------------------------------------------------------------

def build_transactions_report(selected_transactions, csv_filepath=None, delimiter=';'):
    if not csv_filepath:
        csv_filepath = tempfile.mktemp(suffix='.csv', prefix='transactions-')
    with open(csv_filepath,'w') as fou:
        dw = csv.DictWriter(fou, delimiter=delimiter, fieldnames=[
            'Transaction ID', 'Customer', 'Transaction type', 'Amount BTC', 'Amount US $', 'BTC price', 'Date', 'Receiving Address', 'Payment details',
        ])
        dw.writeheader()
        for t in selected_transactions:
            customer_name = f"{t['buyer']['first_name']} {t['buyer']['last_name']}" if t['contract_type'] == 'sales' else f"{t['seller']['first_name']} {t['seller']['last_name']}"
            tr_type = "customer buying BTC" if t['contract_type'] == 'sales' else "customer selling BTC"
            btc_change = -float(t['btc_amount']) if t['contract_type'] == 'sales' else float(t['btc_amount'])
            usd_change = float(t['usd_amount']) if t['contract_type'] == 'sales' else -float(t['usd_amount'])
            dw.writerow({
                'Transaction ID': f"{t['transaction_id']}",
                'Customer': f"{customer_name}".replace(delimiter, ''),
                'Transaction type': tr_type.replace(delimiter, ''),
                'Amount BTC': f"{btc_change}".replace(delimiter, ''),
                'Amount US $': f"{usd_change}".replace(delimiter, ''),
                'BTC price': f"{t['btc_price']}".replace(delimiter, ''),
                'Date': f"{t['date']}".replace(delimiter, ''),
                'Receiving Address': f"{t['buyer']['btc_address']}".replace(delimiter, ''),
                'Payment details': t['seller'].get('bank_info') or 'cash'
            })
    return csv_filepath
