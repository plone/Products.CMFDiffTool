# -*- coding: utf-8 -*-
from App.class_init import InitializeClass
from Products.CMFDiffTool.FieldDiff import FieldDiff


class ListDiff(FieldDiff):
    """Text difference"""

    meta_type = 'List Diff'

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""


    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""

        if type(value) is list or type(value) is tuple:
            return value
        else:
            if type(value) is set:
                return list(value)
            else:
                return [value]

InitializeClass(ListDiff)
