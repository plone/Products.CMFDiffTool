from html import escape
from Products.PortalTransforms.transforms.safe_html import SafeHTML


def safe_unicode(value):
    if isinstance(value, str):
        return value
    try:
        value = str(value)
    except UnicodeDecodeError:
        value = value.decode("utf-8", "replace")
    return value


def safe_utf8(value):
    return safe_unicode(value).encode("utf-8")


def scrub_html(value):
    # Strip illegal HTML tags from string text.
    transform = SafeHTML()
    return transform.scrub_html(value)


# We will have two functions:
# - html_escape: escape html, for example turn '<' into '&lt;'
# - html_safe: return html with dangerous tags removed, using safe html transform.
#
# The convert function that we use in safe_html
# cannot handle a non string-like value, for example an integer.
# Same is true for the escape function.
# Seems good to always return a string-like value though.
# This gets inserted in a string/text.


def html_escape(value):
    value = safe_unicode(value)
    return escape(value, 1)


def html_safe(value):
    value = safe_unicode(value)
    return scrub_html(value)
