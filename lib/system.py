import os
import platform
import subprocess

#------------------------------------------------------------------------------

def open_system_explorer(path, as_folder=True):
    """
    Simple and portable way to show location or file on local disk to the user.
    """
    try:
        if as_folder:
            if platform.system() == "Windows":
                if os.path.isfile(path):
                    subprocess.Popen(['explorer', '/select,', '%s' % (path.replace('/', '\\'))])
                else:
                    subprocess.Popen(['explorer', '%s' % (path.replace('/', '\\'))])
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", path])
            else:
                subprocess.Popen(['sh', '-c', 'nautilus %s' % path])
        else:
            if platform.system() == "Windows":
                os.startfile(path)  # @UndefinedVariable
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", path])
            else:
                subprocess.Popen(["xdg-open", path])
    except:
        try:
            import webbrowser
            webbrowser.open(path)
        except:
            pass
    return

#------------------------------------------------------------------------------

def open_webbrowser(url):
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        pass

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
