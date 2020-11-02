import os
import tempfile
import pdfkit  # @UnresolvedImport

#------------------------------------------------------------------------------

from lib import render_qr

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
                    Transaction price: <b>${btc_price}</b> US / BTC
                    <br>
                    Dollar Amount: <b>${usd_amount}</b> US
                    <br>
                    BTC Amount: <b>{btc_amount}</b>
                    <br>
                    Fee: {fee_percent}%
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
                <p>Where {sender} will send <b>{btc_amount} BTC</b> to:</p>
                <font size=+2>
                    <code>
                        {buyer[btc_address]}
                    </code>
                </font>
                <img src="{qr_filepath}" width="600">
                <hr>
                <p align=left>{disclosure_statement}</p>
                <br>
            </td>
        </tr>
    </table>

    <table width=100% align=left cellspacing=50>
        <tr>
            <td align=left width=50%>
                &nbsp;
                <br>
                <hr>
                <font size=+1><b>Vincent Cate</b> for Bitcoin.ai Ltd.</font>
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
        'fee_percent': '0.0',
        'disclosure_statement': disclosure_statement,
    }
    params.update(transaction_details)
    if str(params['fee_percent']).endswith('.0'):
        params['fee_percent'] = str(params['fee_percent'])[:-2]
    render_qr.make_qr_file(transaction_details['buyer']['btc_address'], qr_filepath)
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
