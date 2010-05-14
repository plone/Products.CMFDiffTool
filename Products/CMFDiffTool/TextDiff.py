# -*- coding: utf-8 -*-
import difflib
from os import linesep
from App.class_init import InitializeClass

from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.utils import safe_unicode, safe_utf8


class TextDiff(FieldDiff):
    """Text difference"""

    meta_type = "Lines Diff"
    inlinediff_fmt = """
<div class="%s">
    <del>%s</del>
    <ins>%s</ins>
</div>
"""

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""
        if filename is None:
            # Split the text into a list for diffs
            return value.splitlines()
        else:
            return [self.filenameTitle(filename)] + value.splitlines()

    def unified_diff(self):
        """Return a unified diff"""
        a = [safe_utf8(i) for i in
             self._parseField(self.oldValue, filename=self.oldFilename)]
        b = [safe_utf8(i) for i in
             self._parseField(self.newValue, filename=self.newFilename)]
        return linesep.join(difflib.unified_diff(a, b, self.id1, self.id2))

    def html_diff(self, context=True, wrapcolumn=40):
        """Return an HTML table showing differences"""
        # difflib is not Unicode-aware, so we need to force everything to
        # utf-8 manually
        a = [safe_unicode(i) for i in
             self._parseField(self.oldValue, filename=self.oldFilename)]
        b = [safe_unicode(i) for i in
             self._parseField(self.newValue, filename=self.newFilename)]
        vis_diff = difflib.HtmlDiff(wrapcolumn=wrapcolumn)
        diff = safe_utf8(vis_diff.make_table(a, b,
                                             safe_unicode(self.id1),
                                             safe_unicode(self.id2),
                                             context=context))
        return diff

    def inline_diff(self):
        """Simple inline diff that just assumes that either the filename
        has changed, or the text has been completely replaced."""
        css_class = 'InlineDiff'
        old_attr = self._parseField(self.oldValue,
                                    filename=self.oldFilename)
        new_attr = self._parseField(self.newValue,
                                    filename=self.newFilename)
        old_fname = old_attr.pop(0)
        new_fname = new_attr.pop(0)
        a = linesep.join(old_attr)
        b = linesep.join(new_attr)
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
