from Globals import InitializeClass
from FieldDiff import FieldDiff
from interfaces.portal_diff import IDifference


class TextDiff(FieldDiff):
    """Text difference"""

    __implements__ = (IDifference)

    meta_type = "Lines Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Split the text into a list for diffs
        return value.split('\n')

InitializeClass(TextDiff)
