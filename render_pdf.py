import os
import platform
import subprocess

import pdfkit  # @UnresolvedImport

#------------------------------------------------------------------------------

import local_storage

#------------------------------------------------------------------------------

def build_buy_contract():
    html_template = """
<html>
<head>
    <title>Bitcoin Purchase Contract</title>
</head>
<body>

</body>
</html>
    """
    rendered_html = html_template.format()
    destination_path = os.path.join(local_storage.contracts_dir(), 'buy_1234.pdf')
    pdfkit.from_string(rendered_html, destination_path)
    with open(destination_path, "rb") as pdf_file:
        pdf_raw = pdf_file.read()
    return {
        'body': pdf_raw,
        'filename': destination_path,
    }

#------------------------------------------------------------------------------

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)  # @UndefinedVariable
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
