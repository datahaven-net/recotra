import qrcode

def make_qr_file(data, filepath):
    img = qrcode.make(data, border=1)
    img.save(filepath)
    return True
