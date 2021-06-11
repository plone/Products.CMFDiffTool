# -*- coding: utf-8 -*-
from Products.PortalTransforms.data import datastream
from Products.PortalTransforms.transforms.safe_html import SafeHTML

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


def scrub_html(value):
    # Strip illegal HTML tags from string text.
    transform = SafeHTML()
    # Available in Plone 5.2:
    # return transform.scrub_html(value)
    data = datastream("text/x-html-safe")
    data = transform.convert(value, data)
    return data.getData()


# We will have two functions:
# - html_escape: escape html, for example turn '<' into '&lt;'
# - html_safe: return html with dangerous tags removed, using safe html transform.
#
# In both Python 2 and 3, the convert function that we use in safe_html
# cannot handle a non string-like value, for example an integer.
# Same is true for the escape function.
# Seems good to always return a string-like value though.
# But should that be bytes or string or unicode?
if six.PY2:
    # We use this in places where the result gets inserted in a string/bytes,
    # so we should use a string (utf-8) here.
    def html_escape(value):
        value = safe_utf8(value)
        return escape(value, 1)

    def html_safe(value):
        value = safe_utf8(value)
        return scrub_html(value)
else:
    # In Python 3 this gets inserted in a string/text.
    def html_escape(value):
        value = safe_unicode(value)
        return escape(value, 1)

    def html_safe(value):
        value = safe_unicode(value)
        return scrub_html(value)
