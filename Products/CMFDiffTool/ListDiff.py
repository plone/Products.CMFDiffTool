from Globals import InitializeClass
from FieldDiff import FieldDiff
from interfaces.portal_diff import IDifference


class ListDiff(FieldDiff):
    """Text difference"""

    __implements__ = (IDifference)

    meta_type = "List Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Return the list as is for diffing
        return value

InitializeClass(ListDiff)
