import qrcode

def make_qr_file(data, filepath):
    img = qrcode.make(data)
    img.save(filepath)
    return True
