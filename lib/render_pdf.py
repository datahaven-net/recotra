import os
import platform
import subprocess
import tempfile
import pdfkit  # @UnresolvedImport

#------------------------------------------------------------------------------

from lib import render_qr
from storage import local_storage

#------------------------------------------------------------------------------

def build_buy_contract(customer_info, contract_info, pdf_filepath=None, qr_filepath=None):
    if not pdf_filepath:
        pdf_filepath = tempfile.mktemp(suffix='.pdf', prefix='btc-contract-')
    if not qr_filepath:
        qr_filepath = tempfile.mktemp(suffix='.png', prefix='btc-contract-qr-')
    html_template = """
<html>
<head>
    <title>AI domains registrations</title>
</head>
<body>
    <table width=100%>
        <tr>
            <td align=right colspan="4">
                BITCOIN PURCHASE CONTRACT
                <hr>
            </td>
        </tr>
        <tr valign=top>
            <td align=left colspan="4">
                <h1>BitCoin.ai Ltd.</h1>
            </td>
        </tr>
        <tr valign=top>
            <td colspan="4">
                <p>Customer selling Bitcoin: <b>{first_name} {last_name}</b></p>
                <p>Customer number: {customer_id}</p>
                <p>Transaction price: <b>${btc_price}</b> US / BTC</p>
                <p>Dollar Amount: <b>${usd_amount}</b> US</p>
                <p>BTC Amount: <b>{btc_amount}</b></p>
                <p>Date: {date}</p>
                <p>Time: {time}</p>
                <hr>
                <br>
                <br>
            </td>
        </tr>
        <tr>
            <td colspan="4" align=center>
                <p>Where customer will send Bitcoin to:</p>
                <font size=26>
                    <code>
                    {receive_address}
                </code>
                </font>
            </td>
        </tr>
        <tr>
            <td colspan="4" align=center>
                <img src="{qr_filepath}">
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
            </td>
        </tr>
    </table>
    <table width=50% align=left>
        <tr>
            <td align=right colspan="1">
                Signed:
                <br> 
                <br>
            </td>
            <td align=left colspan="1">
                &nbsp;
                <br>
                <br>
                <hr>
                <b>Vincent Cate</b> for Bitcoin.ai Ltd.
            </td>
            <td colspan="2">
                &nbsp;
            </td>
        </tr>
        <tr>
            <td>
                &nbsp;
                <br>
                <br>
            </td>
        </tr>
        <tr>
            <td align=right colspan="1">
                &nbsp;
                <br>
                <br> 
            </td>
            <td align=left colspan="1">
                &nbsp;
                <br>
                <br> 
                <hr>
                <b>{first_name} {last_name}</b>
            </td>
            <td align=right colspan="2">
                &nbsp;
            </td>
        </tr>
    </table>
</body>
</html>
    """
    params = {
        'qr_filepath': qr_filepath,
    }
    params.update(customer_info)
    params.update(contract_info)
    rendered_html = html_template.format(**params)
    render_qr.make_qr_file(contract_info['receive_address'], qr_filepath)
    pdfkit.from_string(rendered_html, output_path=pdf_filepath)
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    return {
        'body': pdf_raw,
        'filename': pdf_filepath,
    }

#------------------------------------------------------------------------------

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)  # @UndefinedVariable
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
