# -*- coding: utf-8 -*-

import six


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
