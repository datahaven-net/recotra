import sys

#------------------------------------------------------------------------------

if sys.version_info[0] == 3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode  # @UndefinedVariable
    binary_type = str

#------------------------------------------------------------------------------

def is_text(s):
    """
    Return `True` if `s` is a text value:
    + `unicode()` in Python2
    + `str()` in Python3
    """
    return isinstance(s, text_type)


def is_bin(s):
    """
    Return `True` if `s` is a binary value:
    + `str()` in Python2
    + `bytes()` in Python3
    """
    return isinstance(s, binary_type)


def is_string(s):
    """
    Return `True` if `s` is text or binary type (not integer, class, list, etc...)
    """
    return is_text(s) or is_bin(s)

#------------------------------------------------------------------------------

def to_text(s, encoding='utf-8', errors='strict'):
    """
    If ``s`` is binary type - decode it to unicode - "text" type in Python3 terms.
    If ``s`` is not binary and not text calls `str(s)` to build text representation.
    """
    if s is None:
        return s
    if not is_string(s):
        s = '{0}'.format(s)
    if is_text(s):
        return s
    return s.decode(encoding=encoding, errors=errors)


def to_bin(s, encoding='utf-8', errors='strict'):
    """
    If ``s`` is unicode ("text" type in Python3 terms) - encode it to utf-8, otherwise return ``s``.
    If ``s`` is not binary and not text calls `str(s)` to build text representation,
    then encode to binary and return.
    """
    if s is None:
        return s
    if not is_string(s):
        s = '{0}'.format(s)
    if is_bin(s):
        return s
    return s.encode(encoding=encoding, errors=errors)
