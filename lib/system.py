import platform
import subprocess

#------------------------------------------------------------------------------

def open_system_explorer(path):
    """
    Simple and portable way to show location or file on local disk to the user.
    """
    if platform.system() == "Windows":
        os.startfile(path)  # @UndefinedVariable
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", "-R", path])
    else:
        subprocess.Popen(["xdg-open", path])

#------------------------------------------------------------------------------

def copy_xclip(text, primary=False):
    DEFAULT_SELECTION='c'
    PRIMARY_SELECTION='p'
    ENCODING = 'utf-8'
    selection=DEFAULT_SELECTION
    if primary:
        selection=PRIMARY_SELECTION
    p = subprocess.Popen(['xclip', '-selection', selection], stdin=subprocess.PIPE, close_fds=True)
    return p.communicate(input=text.encode(ENCODING))


def paste_xclip(primary=False):
    DEFAULT_SELECTION='c'
    PRIMARY_SELECTION='p'
    ENCODING = 'utf-8'
    selection=DEFAULT_SELECTION
    if primary:
        selection=PRIMARY_SELECTION
    p = subprocess.Popen(['xclip', '-selection', selection, '-o'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         close_fds=True)
    stdout, stderr = p.communicate()
    # Intentionally ignore extraneous output on stderr when clipboard is empty
    return stdout.decode(ENCODING)
