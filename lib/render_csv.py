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
            dw.writerow({
                'Seller': f"{t['seller']['first_name']} {t['seller']['last_name']}".replace(delimiter, ''),
                'Buyer': f"{t['buyer']['first_name']} {t['buyer']['last_name']}".replace(delimiter, ''),
                'Amount BTC': f"{t['btc_amount']}".replace(delimiter, ''),
                'Amount US $': f"{t['usd_amount']}".replace(delimiter, ''),
                'Date': f"{t['date']}".replace(delimiter, ''),
                'Receiving Address': f"{t['buyer']['btc_address']}".replace(delimiter, ''),
            })
    return csv_filepath
