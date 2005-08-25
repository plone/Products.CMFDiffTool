#
# CMFDiffTool tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import BaseTestCase
from Products.CMFDiffTool.CMFDiffTool import registerDiffType

class DummyDiff:
    meta_type = "Dummy Diff Type"

class DummyDiff2:
    meta_type = "Second Dummy Diff Type"

class TestDiffTool(BaseTestCase.BaseTestCase):
    """Test the portal_diff tool"""

    def afterSetUp(self):
        self.p_diff = self.portal.portal_diff

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import portal_diff
        self.failUnless(portal_diff.isImplementedBy(self.p_diff))

    def testRegisterDiffType(self):
        """Test registration of Diff types"""
        self.failIf('Dummy Diff Type' in self.p_diff.listDiffTypes())
        registerDiffType(DummyDiff)
        self.failUnless('Dummy Diff Type' in self.p_diff.listDiffTypes())

    def testSetDiff(self):
        """Test setDiffForPortalType() method"""
        registerDiffType(DummyDiff)
        d = {'field1':'TestDiff', 'field2':'Dummy Diff Type'}
        self.p_diff.setDiffForPortalType('Document', d)
        self.failUnless(self.p_diff.getDiffForPortalType('Document') == d)

    def testSetDiffReplaces(self):
        """Test that setDiffForPortalType() replaces old data"""
        registerDiffType(DummyDiff)
        d1 = {'field1':'TestDiff', 'field2':'Dummy Diff Type'}
        d2 = {'field3':'Dummy Diff Type'}
        self.p_diff.setDiffForPortalType('Document', d1)
        self.p_diff.setDiffForPortalType('Document', d2)
        self.failUnless(self.p_diff.getDiffForPortalType('Document') == d2)

    def testSingleSetDiffField(self):
        """Test setDiffField method"""
        registerDiffType(DummyDiff)
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.failUnless(self.p_diff.getDiffForPortalType('Document') == {'title':'Dummy Diff Type'})

    def testMultipleSetDiffField(self):
        """Test setDiffField method adding a second field to one content type"""
        registerDiffType(DummyDiff)
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.p_diff.setDiffField('Document', 'description', 'Dummy Diff Type')
        d = {'title':'Dummy Diff Type', 'description':'Dummy Diff Type'}
        self.failUnless(self.p_diff.getDiffForPortalType('Document') == d)
        
    def testReplaceSetDiffField(self):
        """Test that setDiffField does a replace for existing fields"""
        registerDiffType(DummyDiff)
        registerDiffType(DummyDiff2)        
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.p_diff.setDiffField('Document', 'title', 'Second Dummy Diff Type')
        d = {'title':'Second Dummy Diff Type'}
        self.failUnless(self.p_diff.getDiffForPortalType('Document') == d)
        
    def testSetDiffFieldNameFailure(self):
        self.assertRaises('BadRequest', self.p_diff.setDiffField, 'Bob', 'title', 'Dummy Diff Type')

    def testSetDiffFieldBlankFieldFailure(self):
        self.assertRaises('BadRequest', self.p_diff.setDiffField, 'Document', '', 'Dummy Diff Type')

    def testSetDiffFieldInvalidDiffFailure(self):
        self.assertRaises('BadRequest', self.p_diff.setDiffField, 'Document', 'title', 'NoDiff')


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestDiffTool))
        return suite

