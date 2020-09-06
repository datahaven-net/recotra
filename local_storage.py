from io import open
import os
import platform

import jsn
import strng


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

#------------------------------------------------------------------------------

def home_dir():
    return os.path.expanduser('~/.btc_contracts')


def contracts_dir():
    return os.path.join(home_dir(), 'contracts')

#------------------------------------------------------------------------------

def transactions_filepath():
    return os.path.join(home_dir(), 'transactions')


def contacts_filepath():
    return os.path.join(home_dir(), 'contacts')

#------------------------------------------------------------------------------

def create_home_dir():
    if not os.path.isdir(home_dir()):
        os.mkdir(home_dir())
    if not os.path.isdir(contracts_dir()):
        os.mkdir(contracts_dir())

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

def load_contacts_list():
    create_home_dir()
    src = ReadTextFile(contacts_filepath())
    src = src or '{"items":[]}'
    json_data = jsn.loads_text(src)
    return json_data['items']


def save_contacts_list(contacts_list):
    create_home_dir()
    json_data = {'items': contacts_list, }
    return WriteTextFile(contacts_filepath(), jsn.dumps(json_data, indent=2))

#------------------------------------------------------------------------------

def make_contacts_ui_data(contacts_list):
    return [{
            'contact_id': str(i['contact_id']),
            'person_name': i['person_name'],
            'known_wallets': '{} BTC addresses'.format(len(i['known_wallets'].split(','))),
    } for i in contacts_list]
