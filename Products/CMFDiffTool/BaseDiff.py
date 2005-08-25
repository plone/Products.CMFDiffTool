"""CMFDiffTool.py

   Calculate differences between content objects
"""

from Globals import InitializeClass
from Acquisition import aq_base
import Acquisition
from interfaces.portal_diff import IDifference


class BaseDiff:
    """Basic diff type"""

    __implements__ = (IDifference)
    __allow_access_to_unprotected_subobjects__ = 1
    meta_type = "Base Diff"
    
    def __init__(self, obj1, obj2, field):
        self.field = field
        self.oldValue = _getValue(obj1, field)
        self.newValue = _getValue(obj2, field)
        self.same = (self.oldValue == self.newValue)

    def testChanges(self, ob):
        """Test the specified object to determine if the change set will apply without errors"""
        pass

    def applyChanges(self, ob):
        """Update the specified object with the difference"""
        pass
    

def _getValue(ob, field):
    # Check for the attribute without acquisition.  If it's there,
    # grab it *with* acquisition, so things like ComputedAttribute
    # will work
    if hasattr(aq_base(ob), field):
        value = getattr(ob, field)
    else:
        raise AttributeError, field

    # Handle case where the field is a method
    try:
        value = value()
    except (AttributeError, TypeError):
        pass

    # If this is some object, convert it to a string
    try:
        if isinstance(value, Acquisition.Implicit):
            value = str(value)
    except TypeError:
        pass

    return value

InitializeClass(BaseDiff)
