# Copyright (c) 2003 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks

"""Interface for computing object differences"""

from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Base as Interface

class portal_diff(Interface):
    """An interface to compute object differences via pluggable
       difference engine"""

    id = Attribute('id','Must be set to "portal_diff"')


    def listDiffTypes():
        """List the names of the available difference types"""

    def setDiffForPortalType(pt_name, mapping):
        """Set the difference type(s) for the specific portal type

        mapping is a dictionary where each key is an attribute or
        method on the given portal type, and the value is the name of
        a difference type."""

    def getDiffForPortalType(pt_name):
        """Returns a dictionary where each key is an attribute or
        method on the given portal type, and the value is the name of
        a difference type."""
    
    def computeDiff(ob1, ob2):
        """Compute the differences from ob1 to ob2 (ie. ob2 - ob1).

        The result will be a list of objects that implements the
        IDifference interface and represent the differences between
        ob1 and ob2."""

    def createChangeSet(ob1, ob2):
        """Returns a ChangeSet object that represents the differences
        between ob1 and ob2 (ie. ob2 - ob1) ."""
    


class IDifference(Interface):
    """An interface for interacting with the difference between two
    objects"""

    meta_type = Attribute('title', 'A human readable name for the diff type')
    field = Attribute('field', 'The name of the field being compared')
    same = Attribute('same', 'True if the fields are the "same" (whatever that means for this difference)')
    oldValue = Attribute('oldValue', 'The old field value being compared')
    newValue = Attribute('newValue', 'The new field value being compared')

    def testChanges(ob):
        """Test the specified object to determine if the change set will apply cleanly.

        Returns None if there would be no erros
        """

    def applyChanges(ob):
        """Update the specified object with the difference"""


class IStringDifference(IDifference):
    """An anterface for interacting with the difference between two
    string (text) objects"""

    def getLineDiffs():
        """Return a list of differences between the two objects on a
        line-by-line basis

        Each difference is a 5-tuple as described here:
        http://www.python.org/doc/2.1.3/lib/sequence-matcher.html#l2h-721

        The interpretation of these tuples depends on the difference class"""

##     def getCharDiffs():
##         """Return a list of character differences on a line-by-line basis.
        
##         For every line in the field being compared, return a list of
##         character differences """

