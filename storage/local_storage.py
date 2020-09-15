from io import open
import os
import platform

#------------------------------------------------------------------------------

from lib import jsn
from lib import strng

#------------------------------------------------------------------------------

def init():
    create_home_dir()

#------------------------------------------------------------------------------

def home_dir():
    return os.path.expanduser('~/.btc_contracts')


def contracts_dir():
    return os.path.join(home_dir(), 'contracts')

#------------------------------------------------------------------------------

def temp_dir():
    return os.path.join(home_dir(), 'temp')


def transactions_filepath():
    return os.path.join(home_dir(), 'transactions')


def customers_dir():
    return os.path.join(home_dir(), 'customers')


def customer_dir(customer_id):
    return os.path.join(customers_dir(), str(customer_id))


def customer_info_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'info.json')


def customer_photo_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'photo.jpg')


def customer_passport_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'passport.jpg')

#------------------------------------------------------------------------------

def create_home_dir():
    if not os.path.isdir(home_dir()):
        os.mkdir(home_dir())
    if not os.path.isdir(contracts_dir()):
        os.mkdir(contracts_dir())
    if not os.path.isdir(customers_dir()):
        os.mkdir(customers_dir())
    if not os.path.isdir(temp_dir()):
        os.mkdir(temp_dir())

#------------------------------------------------------------------------------

def load_transactions_list():
    create_home_dir()
    src = ReadTextFile(transactions_filepath())
    src = src or '{"items":[]}'
    json_data = jsn.loads_text(src)
    return json_data['items']


def save_transactions(transactions_list):
    create_home_dir()
    json_data = {'items': transactions_list, }
    return WriteTextFile(transactions_filepath(), jsn.dumps(json_data, indent=2))

#------------------------------------------------------------------------------

def load_customers_list():
    create_home_dir()
    result = []
    for customer_id in os.listdir(customers_dir()):
        src = ReadTextFile(customer_info_filepath(customer_id))
        src = src or ('{"customer_id": %s}' % customer_id)
        json_data = jsn.loads_text(src)
        result.append(json_data)
    return result


def save_customers_list(customers_list):
    create_home_dir()
    for customer_info in customers_list:
        if not WriteTextFile(customer_info_filepath(customer_info['customer_id']), jsn.dumps(customer_info, indent=2)):
            return False
    return True

#------------------------------------------------------------------------------

def create_new_customer_info():
    create_home_dir()
    max_customer_id = 0
    all_customers = os.listdir(customers_dir())
    for customer_id in all_customers:
        if int(customer_id) > max_customer_id:
            max_customer_id = int(customer_id)
    new_customer_id = str(max_customer_id + 1)
    os.mkdir(customer_dir(new_customer_id))
    return str(new_customer_id)

#------------------------------------------------------------------------------

def make_customers_ui_data(customers_list):
    return [{
            'customer_id': str(i['customer_id']),
            'person_name': i.get('person_name', ''),
            'known_wallets': '{} BTC addresses'.format(len(i.get('known_wallets', '').split(','))),
    } for i in customers_list]

#------------------------------------------------------------------------------

def WriteBinaryFile(filename, data):
    """
    A smart way to write data to binary file. Return True if success.
    This should be atomic operation - data is written to another temporary file and than renamed.
    """
    try:
        tmpfilename = filename + ".new"
        f = open(tmpfilename, 'wb')
        bin_data = strng.to_bin(data)
        f.write(bin_data)
        f.flush()
        # from http://docs.python.org/library/os.html on os.fsync
        os.fsync(f.fileno())
        f.close()
        # in Unix the rename will overwrite an existing file,
        # but in Windows it fails, so have to remove existing file first
        if platform.uname()[0] == 'Windows' and os.path.exists(filename):
            os.remove(filename)
        os.rename(tmpfilename, filename)
    except:
        try:
            # make sure file gets closed
            f.close()
        except:
            pass
        return False
    return True


def AppendBinaryFile(filename, data, mode='a'):
    """
    Same as WriteBinaryFile but do not erase previous data in the file.
    TODO: this is not atomic right now
    """
    try:
        f = open(filename, mode)
        if 'b' in mode:
            bin_data = strng.to_bin(data)
            f.write(bin_data)
        else:
            f.write(data)
        f.flush()
        os.fsync(f.fileno())
        f.close()
    except:
        try:
            # make sure file gets closed
            f.close()
        except:
            pass
        return False
    return True


def ReadBinaryFile(filename, decode_encoding=None):
    """
    A smart way to read binary file. Return empty string in case of:

    - path not exist
    - process got no read access to the file
    - some read error happens
    - file is really empty
    """
    if not os.path.isfile(filename):
        return b''
    if not os.access(filename, os.R_OK):
        return b''
    try:
        infile = open(filename, mode='rb')
        data = infile.read()
        if decode_encoding is not None:
            data = data.decode(decode_encoding)
        infile.close()
        return data
    except:
        return b''

#------------------------------------------------------------------------------

def WriteTextFile(filepath, data):
    """
    A smart way to write data into text file. Return True if success.
    This should be atomic operation - data is written to another temporary file and than renamed.
    """
    temp_path = filepath + '.tmp'
    if os.path.exists(temp_path):
        if not os.access(temp_path, os.W_OK):
            return False
    if os.path.exists(filepath):
        if not os.access(filepath, os.W_OK):
            return False
        try:
            os.remove(filepath)
        except:
            return False
    fout = open(temp_path, 'wt', encoding="utf-8")
    text_data = strng.to_text(data)
    fout.write(text_data)
    fout.flush()
    os.fsync(fout)
    fout.close()
    try:
        os.rename(temp_path, filepath)
    except:
        return False
    return True


def ReadTextFile(filename):
    """
    Read text file and return its content.
    """
    if not os.path.isfile(filename):
        return u''
    if not os.access(filename, os.R_OK):
        return u''
    try:
        infile = open(filename, 'rt', encoding="utf-8")
        data = infile.read()
        infile.close()
        return strng.to_text(data)
    except:
        pass
    return u''
