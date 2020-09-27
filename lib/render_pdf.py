import os
import platform
import subprocess
import tempfile
import pdfkit  # @UnresolvedImport

#------------------------------------------------------------------------------

from lib import render_qr

#------------------------------------------------------------------------------

def build_buy_contract(transaction_details, pdf_filepath=None, qr_filepath=None):
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
    <title>AI domains registrations</title>
</head>
<body>
    <table width=100%>
        <tr>
            <td align=right colspan="4">
                <font size=+1>BITCOIN PURCHASE CONTRACT</font>
                <hr>
            </td>
        </tr>
        <tr valign=top>
            <td align=left colspan="4">
                <font size=+2><h1>BitCoin.ai Ltd.</h1></font>
            </td>
        </tr>
        <tr valign=top>
            <td colspan="4">
                <font size=+2>
                <p>Customer selling Bitcoin: <b>{seller[first_name]} {seller[last_name]}</b></p>
                <p>Customer number: {seller[customer_id]}</p>
                <p>Transaction price: <b>${btc_price}</b> US / BTC</p>
                <p>Dollar Amount: <b>${usd_amount}</b> US</p>
                <p>BTC Amount: <b>{btc_amount}</b></p>
                <p>Date: {date}</p>
                <p>Time: {time}</p>
                <hr>
                <br>
                </font>
            </td>
        </tr>
        <tr>
            <td colspan="4" align=center>
                <p>Where customer will send Bitcoin to:</p>
                <font size=26>
                    <code>
                    {buyer[btc_address]}
                </code>
                </font>
            </td>
        </tr>
        <tr>
            <td colspan="4" align=center>
                <img src="{qr_filepath}">
                <br>
                <br>
            </td>
        </tr>
    </table>
    <table width=50% align=left>
        <tr>
            <td align=right colspan="1">
                <font size=+1>Signed:</font>
                <br> 
                <br>
            </td>
            <td align=left colspan="1">
                &nbsp;
                <br>
                <br>
                <hr>
                <font size=+1><b>Vincent Cate</b> for Bitcoin.ai Ltd.</font>
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
                <font size=+1><b>{buyer[first_name]} {buyer[last_name]}</b></font>
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
    params.update(transaction_details)
    rendered_html = html_template.format(**params)
    render_qr.make_qr_file(transaction_details['buyer']['btc_address'], qr_filepath)
    pdfkit.from_string(
        input=rendered_html,
        output_path=pdf_filepath,
        # css=os.path.abspath('print_pdf.css'),
        # options={ 'quiet': '', 'zoom': 2, 'page-size': 'A4', 'dpi': 400, },
    )
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    os.remove(qr_filepath)
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
