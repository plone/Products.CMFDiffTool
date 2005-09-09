#
# CMFDiffTool tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFDiffTool.ChangeSet import ChangeSet
from Products.CMFDiffTool.ChangeSet import BaseChangeSet

class TestChangeSet(ZopeTestCase.ZopeTestCase):
    """Test the portal_diff tool"""

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.IChangeSet import IChangeSet
        self.failUnless(IChangeSet.isImplementedByInstancesOf(ChangeSet))
        self.failUnless(IChangeSet.isImplementedByInstancesOf(BaseChangeSet))


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestChangeSet))
        return suite

