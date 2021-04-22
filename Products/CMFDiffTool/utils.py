# -*- coding: utf-8 -*-

import six


try:
    from html import escape
except ImportError:
    from cgi import escape


def safe_unicode(value):
    if isinstance(value, six.text_type):
        return value
    try:
        value = six.text_type(value)
    except UnicodeDecodeError:
        value = value.decode('utf-8', 'replace')
    return value


def safe_utf8(value):
    return safe_unicode(value).encode('utf-8')


# In both Python 2 and 3, the escape function cannot handle a non string-like value,
# for example an integer.  Seems good to always return a string-like value though.
# But should that be bytes or string or unicode?
if six.PY2:
    # We use this in places where the result gets inserted in a string/bytes,
    # so we should use a string (utf-8) here.
    def html_encode(value):
        value = safe_utf8(value)
        return escape(value, 1)
else:
    # In Python 3 this gets inserted in a string/text,
    # and escape cannot handle a bytes value.
    def html_encode(value):
        value = safe_unicode(value)
        return escape(value, 1)
