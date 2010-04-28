# -*- coding: utf-8 -*-
import difflib
from App.class_init import InitializeClass

from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.utils import safe_unicode, safe_utf8


class TextDiff(FieldDiff):
    """Text difference"""

    meta_type = "Lines Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Split the text into a list for diffs
        return value.split('\n')

    def unified_diff(self):
        """Return a unified diff"""
        a = [safe_utf8(i) for i in self._parseField(self.oldValue)]
        b = [safe_utf8(i) for i in self._parseField(self.newValue)]
        return '\n'.join(difflib.unified_diff(a, b, self.id1, self.id2))

    def html_diff(self, context=True, wrapcolumn=40):
        """Return an HTML table showing differences"""
        # difflib is not Unicode-aware, so we need to force everything to
        # utf-8 manually
        a = [safe_unicode(i) for i in self._parseField(self.oldValue)]
        b = [safe_unicode(i) for i in self._parseField(self.newValue)]
        vis_diff = difflib.HtmlDiff(wrapcolumn=wrapcolumn)
        diff = safe_utf8(vis_diff.make_table(a, b,
                                             safe_unicode(self.id1),
                                             safe_unicode(self.id2),
                                             context=context))
        return diff

    def inline_diff(self):
        """Simple inline diff that just assumes that the text has been
        completely replaced."""
        if self.oldValue != self.newValue:
            return '<div class="InlineDiff"><del>%s</del><ins>%s</ins></div>'%(
                self.newValue, self.oldValue)


InitializeClass(TextDiff)
