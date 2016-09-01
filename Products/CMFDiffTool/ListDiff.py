# -*- coding: utf-8 -*-
from App.class_init import InitializeClass
from Products.CMFDiffTool.FieldDiff import FieldDiff


class ListDiff(FieldDiff):
    """Text difference"""

    meta_type = 'List Diff'

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""
        # Return the list as is for diffing
        if type(value) is set:
            # A set cannot be indexed, so return a list of a set
            return list(value)
        else:
            return value

InitializeClass(ListDiff)
