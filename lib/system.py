import os
import platform
import subprocess

#------------------------------------------------------------------------------

from kivy import utils  # @UnresolvedImport

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

_LatestState = None

#------------------------------------------------------------------------------

def current_platform():
    global _LatestState
    if _LatestState:
        return _LatestState
    _LatestState = str('' + utils.platform)
    return _LatestState

#------------------------------------------------------------------------------

def is_linux():
    return current_platform() == 'linux'


def is_windows():
    return current_platform() == 'win'


def is_android():
    return current_platform() == 'android'


def is_ios():
    return current_platform() == 'ios'


def is_osx():
    return current_platform() == 'macosx'


def is_mobile():
    return is_android() or is_ios()

#------------------------------------------------------------------------------


def open_path_in_os(filepath):
    """
    A portable way to open location or file on local disk with a default OS method.
    """
    try:
        if is_windows():
            if os.path.isfile(filepath):
                subprocess.Popen(['explorer', '/select,', '%s' % (filepath.replace('/', '\\'))])
                return True
            subprocess.Popen(['explorer', '%s' % (filepath.replace('/', '\\'))])
            return True
        elif is_linux():
            subprocess.Popen(['xdg-open', '%s' % filepath])
            return True
        elif is_osx():
            subprocess.Popen(['open', '-R', '%s' % filepath])
            return True
    except Exception as exc:
        if _Debug:
            print('system.open_path_in_os %r : %r' % (filepath, exc, ))
        return False
    try:
        import webbrowser
        webbrowser.open(filepath)
        return True
    except Exception as e:
        if _Debug:
            print('file %r failed to open with default OS method: %r' % (filepath, e, ))
    return False

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
                subprocess.Popen(['sh', '-c', 'nautilus', '%s' % path])
        else:
            if platform.system() == "Windows":
                os.startfile(path)  # @UndefinedVariable
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", '%s' % path])
            else:
                subprocess.Popen(["xdg-open", '%s' % path])
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
