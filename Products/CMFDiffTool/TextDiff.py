# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from os import linesep
from Products.CMFDiffTool import CMFDiffToolMessageFactory as _
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.utils import safe_unicode
from Products.CMFDiffTool.utils import safe_utf8
from zope.component.hooks import getSite

import difflib
import six


class TextDiff(FieldDiff):
    """Text difference"""

    meta_type = 'Lines Diff'
    inlinediff_fmt = """
<div class="%s">
    <del>%s</del>
    <ins>%s</ins>
</div>
"""

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""
        if value is None:
            value = ''
        if filename is None:
            # Split the text into a list for diffs
            return value.splitlines()
        else:
            return [self.filenameTitle(filename)] + value.splitlines()

    def unified_diff(self):
        """Return a unified diff"""
        a = self._parseField(self.oldValue, filename=self.oldFilename)
        b = self._parseField(self.newValue, filename=self.newFilename)
        if six.PY2:
            a = [safe_utf8(i) for i in a]
            b = [safe_utf8(i) for i in b]
        # in py3 unified_diff does not accept None for ids (id1 and id2)
        # But TextDiff() sets None as default. We overwrite this here so the
        # default of unified_diff ('') can be used .
        cleanargs = [a, b, self.id1, self.id2]
        cleanargs = [i for i in cleanargs if i]
        return linesep.join(difflib.unified_diff(*cleanargs))

    def html_diff(self, context=True, wrapcolumn=40):
        """Return an HTML table showing differences"""
        # difflib is not Unicode-aware, so we need to force everything to
        # utf-8 manually
        a = [safe_unicode(i) for i in
             self._parseField(self.oldValue, filename=self.oldFilename)]
        b = [safe_unicode(i) for i in
             self._parseField(self.newValue, filename=self.newFilename)]
        vis_diff = difflib.HtmlDiff(wrapcolumn=wrapcolumn)
        diff = vis_diff.make_table(
            a,
            b,
            safe_unicode(self.id1),
            safe_unicode(self.id2),
            context=context)
        if six.PY2:
            diff = safe_utf8(diff)
        return diff

    def inline_diff(self):
        """Simple inline diff that just assumes that either the filename
        has changed, or the text has been completely replaced."""
        css_class = 'InlineDiff'
        old_attr = self._parseField(self.oldValue,
                                    filename=self.oldFilename)
        new_attr = self._parseField(self.newValue,
                                    filename=self.newFilename)
        if old_attr:
            old_fname = old_attr.pop(0)
        else:
            old_fname = None
        if new_attr:
            new_fname = new_attr.pop(0)
        else:
            new_fname = None
        a = linesep.join(old_attr or [])
        b = linesep.join(new_attr or [])
        html = []
        if old_fname != new_fname:
            html.append(
                self.inlinediff_fmt % ('%s FilenameDiff' % css_class,
                                       old_fname, new_fname)
            )
        if a != b:
            html.append(
                self.inlinediff_fmt % (css_class, a, b)
            )
        if html:
            return linesep.join(html)

InitializeClass(TextDiff)


class AsTextDiff(TextDiff):
    """
    Specialization of `TextDiff` that converts any value to text in order to
    provide an inline diff visualization. Also translated (i18n) the
    strings `True` and `False`.
    """

    def _parseField(self, value, filename=None):
        if value is None:
            value = ''

        # In tests translation is not available, so we account for this
        # case here.
        translate = getattr(getSite(), 'translate', None)
        if translate is not None:
            value = translate(_(value))

        return TextDiff._parseField(self, safe_unicode(value), filename)

InitializeClass(AsTextDiff)
