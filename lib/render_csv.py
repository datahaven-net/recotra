import csv
import tempfile

#------------------------------------------------------------------------------

def build_transactions_report(selected_transactions, csv_filepath=None, delimiter=';'):
    if not csv_filepath:
        csv_filepath = tempfile.mktemp(suffix='.csv', prefix='transactions-')
    with open(csv_filepath,'w') as fou:
        dw = csv.DictWriter(fou, delimiter=delimiter, fieldnames=[
            'Seller', 'Buyer', 'Amount BTC', 'Amount US $', 'Date', 'Receiving Address',
        ])
        dw.writeheader()
        for t in selected_transactions:
            seller = '' if t['contract_type'] == 'sales' else f"{t['seller']['first_name']} {t['seller']['last_name']}"
            buyer = '' if t['contract_type'] == 'purchase' else f"{t['buyer']['first_name']} {t['buyer']['last_name']}"
            dw.writerow({
                'Seller': f"{seller}".replace(delimiter, ''),
                'Buyer': f"{buyer}".replace(delimiter, ''),
                'Amount BTC': f"{t['btc_amount']}".replace(delimiter, ''),
                'Amount US $': f"{t['usd_amount']}".replace(delimiter, ''),
                'Date': f"{t['date']}".replace(delimiter, ''),
                'Receiving Address': f"{t['buyer']['btc_address']}".replace(delimiter, ''),
            })
    return csv_filepath
