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

def customers_dir():
    return os.path.join(home_dir(), 'customers')

def customer_dir(customer_id):
    return os.path.join(customers_dir(), str(customer_id))

def transactions_dir():
    return os.path.join(home_dir(), 'transactions')

def contracts_dir():
    return os.path.join(home_dir(), 'contracts')

def temp_dir():
    return os.path.join(home_dir(), 'temp')

#------------------------------------------------------------------------------

def customer_info_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'info.json')


def customer_photo_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'photo.jpg')


def customer_passport_filepath(customer_id):
    return os.path.join(customer_dir(customer_id), 'passport.jpg')

#------------------------------------------------------------------------------

def transaction_filepath(transaction_id):
    return os.path.join(transactions_dir(), str(transaction_id))

#------------------------------------------------------------------------------

def create_home_dir():
    if not os.path.isdir(home_dir()):
        os.mkdir(home_dir())
    if not os.path.isdir(transactions_dir()):
        os.mkdir(transactions_dir())
    if not os.path.isdir(customers_dir()):
        os.mkdir(customers_dir())
    if not os.path.isdir(contracts_dir()):
        os.mkdir(contracts_dir())
    if not os.path.isdir(temp_dir()):
        os.mkdir(temp_dir())


def create_customer_dir(customer_id):
    if not os.path.isdir(customer_dir(customer_id)):
        os.mkdir(customer_dir(customer_id))

#------------------------------------------------------------------------------

def load_transactions_list(sort_by='transaction_id'):
    create_home_dir()
    result = []
    for transaction_id in os.listdir(transactions_dir()):
        src = ReadTextFile(transaction_filepath(transaction_id))
        src = src or ('{"transaction_id": %s' % transaction_id)
        json_data = jsn.loads_text(src)
        result.append(json_data)
    if sort_by == 'transaction_id':
        result.sort(key=lambda i: str(i.get('customer_id', '')))
    return result


def create_new_transaction(details):
    create_home_dir()
    max_transaction_id = 0
    all_transactions = os.listdir(transactions_dir())
    for transaction_id in all_transactions:
        if int(transaction_id) > max_transaction_id:
            max_transaction_id = int(transaction_id)
    new_transaction_id = str(max_transaction_id + 1)
    details['transaction_id'] = new_transaction_id
    WriteTextFile(transaction_filepath(new_transaction_id), jsn.dumps(details, indent=2))
    return details


def write_transaction(transaction_id, details):
    create_home_dir()
    return WriteTextFile(transaction_filepath(transaction_id), jsn.dumps(details, indent=2))


def read_transaction(transaction_id):
    create_home_dir()
    src = ReadTextFile(transaction_filepath(transaction_id))
    if not src:
        return None
    json_data = jsn.loads_text(src)
    return json_data

#------------------------------------------------------------------------------

def load_customers_list(sort_by='customer_id'):
    create_home_dir()
    result = []
    for customer_id in os.listdir(customers_dir()):
        src = ReadTextFile(customer_info_filepath(customer_id))
        src = src or ('{"customer_id": %s}' % customer_id)
        json_data = jsn.loads_text(src)
        result.append(json_data)
    if sort_by == 'customer_id':
        result.sort(key=lambda i: str(i.get('customer_id', '')))
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


def write_customer_info(customer_info):
    create_home_dir()
    create_customer_dir(customer_info['customer_id'])
    return WriteTextFile(customer_info_filepath(customer_info['customer_id']), jsn.dumps(customer_info, indent=2))


def erase_customer_info(customer_id):
    create_home_dir()
    if not os.path.exists(customer_dir(customer_id)):
        return
    rmdir_recursive(customer_dir(customer_id))


def read_customer_info(customer_id):
    create_home_dir()
    if not os.path.exists(customer_dir(customer_id)):
        return None
    src = ReadTextFile(customer_info_filepath(customer_id))
    if not src:
        return None
    json_data = jsn.loads_text(src)
    return json_data

#------------------------------------------------------------------------------

def make_customers_ui_data(customers_list):
    return [{
        'customer_id': str(i['customer_id']),
        'first_name': i.get('first_name', ''),
        'last_name': i.get('last_name', ''),
        'phone': i.get('phone', ''),
        'email': i.get('email', ''),
        'address': i.get('address', ''),
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


def rmdir_recursive(dirpath, ignore_errors=False, pre_callback=None):
    """
    Remove a directory, and all its contents if it is not already empty.
    http://mail.python.org/pipermail/python-
    list/2000-December/060960.html If ``ignore_errors`` is True process
    will continue even if some errors happens. Method ``pre_callback``
    can be used to decide before remove the file.
    """
    counter = 0
    for name in os.listdir(dirpath):
        full_name = os.path.join(dirpath, name)
        # on Windows, if we don't have write permission we can't remove
        # the file/directory either, so turn that on
        if not os.access(full_name, os.W_OK):
            try:
                os.chmod(full_name, 0o600)
            except:
                continue
        if os.path.isdir(full_name):
            counter += rmdir_recursive(full_name, ignore_errors, pre_callback)
        else:
            if pre_callback:
                if not pre_callback(full_name):
                    continue
            if os.path.isfile(full_name):
                if not ignore_errors:
                    os.remove(full_name)
                    counter += 1
                else:
                    try:
                        os.remove(full_name)
                        counter += 1
                    except Exception as exc:
                        pass
                        continue
    if pre_callback:
        if not pre_callback(dirpath):
            return counter
    if not ignore_errors:
        os.rmdir(dirpath)
    else:
        try:
            os.rmdir(dirpath)
        except Exception as exc:
            pass
    return counter

