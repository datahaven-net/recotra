import os
import tempfile
import pdfkit  # @UnresolvedImport

#------------------------------------------------------------------------------

from lib import render_qr

from storage import local_storage

#------------------------------------------------------------------------------

def build_pdf_contract(transaction_details, disclosure_statement='', pdf_filepath=None, qr_filepath=None):
    if not pdf_filepath:
        pdf_filepath = tempfile.mktemp(suffix='.pdf', prefix='btc-contract-')
    if os.path.isfile(pdf_filepath):
        os.remove(pdf_filepath)
    if not qr_filepath:
        qr_filepath = tempfile.mktemp(suffix='.png', prefix='btc-contract-qr-')
    if os.path.isfile(qr_filepath):
        os.remove(qr_filepath)
    html_template = """
<html>
<head>
    <title>Bitcoin.ai Ltd.</title>
</head>
<body>

    <table width=100%>
        <tr>
            <td align=right colspan="4">
                <font size=+1>BITCOIN {contract_type_str} CONTRACT</font>
                <hr>
            </td>
        </tr>
        <tr valign=top>
            <td align=left colspan="4">
                <font size=+1><h1>BitCoin.ai Ltd.</h1></font>
            </td>
        </tr>
        <tr valign=top>
            <td colspan="4">
                <font size=+2>
                <p>
                    Customer {buying_selling} Bitcoin: <b>{first_name} {last_name}</b>
                    <br>
                    Customer number: {customer_id}
                    <br>
                    Price at coinmarketcap.com: <b>${world_btc_price}</b> US / BTC
                    <br>
                    Price offset: {fee_percent}%
                    <br>
                    Price for this contract: <b>${btc_price}</b> US / BTC
                    <br>
                    Dollar Amount: <b>${usd_amount}</b> US
                    <br>
                    Bitcoin Amount: {btc_amount}
                    <br>
                    Date: {date}
                    <br>
                    Time: {time}
                </p>
                </font>
                <hr>
            </td>
        </tr>
        <tr>
            <td colspan="4" align=center>
                <p>Where {sender} will send {btc_amount} to:</p>
                <font size=+2>
                    <code>
                        {buyer[btc_address]}
                    </code>
                </font>
                <img src="{qr_filepath}" width="600">
                <hr>
                <p align=left>{disclosure_statement}</p>
            </td>
        </tr>
    </table>

    <table width=100% align=left cellspacing=50>
        <tr>
            <td align=left width=50%>
                &nbsp;
                <br>
                <hr>
                <font size=+1><b>{business_owner_first_name} {business_owner_last_name}</b> for {business_company_name}</font>
            </td>
            <td align=left width=50%>
                &nbsp;
                <br>
                <hr>
                <font size=+1><b>{first_name} {last_name}</b></font>
            </td>
        </tr>
    </table>

</body>
</html>
    """
    cur_settings = local_storage.read_settings()
    contract_type = transaction_details['contract_type']
    buyer = transaction_details['buyer']
    seller = transaction_details['seller']
    params = {
        'qr_filepath': qr_filepath,
        'contract_type_str': contract_type.upper(),
        'buying_selling': 'selling' if contract_type == 'purchase' else 'buying',
        'first_name': seller['first_name'] if contract_type == 'purchase' else buyer['first_name'],
        'last_name': seller['last_name'] if contract_type == 'purchase' else buyer['last_name'],
        'customer_id': seller['customer_id'] if contract_type == 'purchase' else buyer['customer_id'],
        'sender': '{} {}'.format(seller['first_name'], seller['last_name']),
        'business_company_name': cur_settings.get('business_company_name') or '',
        'business_owner_first_name': cur_settings.get('business_owner_first_name') or '',
        'business_owner_last_name': cur_settings.get('business_owner_last_name') or '',
        'fee_percent': '0.0',
        'disclosure_statement': disclosure_statement,
    }
    params.update(transaction_details)
    if str(params['fee_percent']).endswith('.0'):
        params['fee_percent'] = str(params['fee_percent'])[:-2]
    if 'world_btc_price' not in params:
        params['world_btc_price'] = ''
    qr_src_text = 'bitcoin:{}?label={}'.format(
        transaction_details['buyer']['btc_address'],
        cur_settings.get('business_company_name', '').replace(' ', '_'),
    )
    if params['btc_amount']:
        qr_src_text = 'bitcoin:{}?amount={}'.format(
            transaction_details['buyer']['btc_address'],
            params['btc_amount'],
        )
        params['btc_amount'] = '<b>{} BTC</b>  ( {} mBTC )'.format(
            params['btc_amount'], str(round(float(params['btc_amount']) * 1000.0, 6)))
    render_qr.make_qr_file(qr_src_text, qr_filepath)
    rendered_html = html_template.format(**params)
    pdfkit.from_string(
        input=rendered_html,
        output_path=pdf_filepath,
    )
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    os.remove(qr_filepath)
    return {
        'body': pdf_raw,
        'filename': pdf_filepath,
    }

#------------------------------------------------------------------------------

def build_id_card(customer_info, customer_photo_filepath=None, pdf_filepath=None):
    if not pdf_filepath:
        pdf_filepath = tempfile.mktemp(suffix='.pdf', prefix='id-card-')
    if os.path.isfile(pdf_filepath):
        os.remove(pdf_filepath)
    qr_filepath = tempfile.mktemp(suffix='.png', prefix='id-card-qr-')
    html_template = """
<html>
<head>
    <title>Bitcoin.ai Ltd.</title>
</head>
<body>
    <table border=1 cellspacing=0 cellpadding=5 >
        <tr>
            <td align=left colspan="2">
                <img height=200 src="{photo_filepath}">
                <img width=200 height=200 src="{qr_filepath}">
            </td>
        </tr>
        <tr valign=top>    
            <td align=left colspan="1" width=320>
                &nbsp;&nbsp;&nbsp;<font size=+3>{first_name} {last_name}</font>
            </td>
            <td align=right valign=bottom colspan="1">
                <font size=-1>customer #{customer_id}</font>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    params = {
        'customer_id': customer_info['customer_id'],
        'first_name': customer_info['first_name'],
        'last_name': customer_info['last_name'],
        'photo_filepath': customer_photo_filepath or '',
        'qr_filepath': qr_filepath,
    }
    render_qr.make_qr_file(customer_info['customer_id'], qr_filepath)
    rendered_html = html_template.format(**params)
    pdfkit.from_string(
        input=rendered_html,
        output_path=pdf_filepath,
    )
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    os.remove(qr_filepath)
    return {
        'body': pdf_raw,
        'filename': pdf_filepath,
    }

#------------------------------------------------------------------------------

def build_transactions_report(selected_transactions, selected_month, selected_year, pdf_filepath=None):
    if not pdf_filepath:
        pdf_filepath = tempfile.mktemp(suffix='.pdf', prefix='transactions-')
    html_template = """
<html>
<head>
    <title>Bitcoin.ai Ltd.</title>
</head>
<body>
    <h3>{selected_month} {selected_year}</h3>
    <table border=1 cellspacing=0 cellpadding=5 >
        <tr>
            <th>Seller</th>
            <th>Buyer</th>
            <th>Amount BTC</th>
            <th>Amount US $</th>
            <th>Date</th>
            <th>Receiving Address</th>
        </tr>
{table_content}
    </table>
<br>
<table>
<tr><td>
    <p>
        Total BTC received: <b>{total_btc_bought}</b>
    </p>
    <p>
        Total Dollars paid out: <b>{total_usd_sold}</b> US $
    </p>
</td>
<td>&nbsp;&nbsp;&nbsp;</td>
<td>
    <p>
        Total BTC paid out: <b>{total_btc_sold}</b>
    </p>
    <p>
        Total Dollars received: <b>{total_usd_bought}</b> US $
    </p>
</td></tr>
</table>
</body>
</html>
    """
    table_content = ''
    total_btc_bought = 0.0
    total_usd_bought = 0.0
    total_btc_sold = 0.0
    total_usd_sold = 0.0
    for t in selected_transactions:
        seller = '' if t['contract_type'] == 'sales' else f"{t['seller']['first_name']} {t['seller']['last_name']}"
        buyer = '' if t['contract_type'] == 'purchase' else f"{t['buyer']['first_name']} {t['buyer']['last_name']}"
        table_content += f'''
        <tr>
            <td nowrap>{seller}</td>
            <td nowrap>{buyer}</td>
            <td nowrap>{t['btc_amount']}</td>
            <td nowrap>{t['usd_amount']}</td>
            <td nowrap>{t['date']}</td>
            <td nowrap>{t['buyer']['btc_address']}</td>
        </tr>
        '''
        if t['contract_type'] == 'sales':
            total_btc_sold += float(t['btc_amount'])
            total_usd_bought += float(t['usd_amount'])
        else:
            total_btc_bought += float(t['btc_amount'])
            total_usd_sold += float(t['usd_amount'])
    params = {
        'table_content': table_content,
        'selected_month': selected_month.replace('-', ''),
        'selected_year': selected_year.replace('-', ''),
        'total_btc_bought': round(total_btc_bought, 6),
        'total_usd_bought': round(total_usd_bought, 2),
        'total_btc_sold': round(total_btc_sold, 6),
        'total_usd_sold': round(total_usd_sold, 2),
    }
    rendered_html = html_template.format(**params)
    pdfkit.from_string(
        input=rendered_html,
        output_path=pdf_filepath,
    )
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    return {
        'body': pdf_raw,
        'filename': pdf_filepath,
    }
