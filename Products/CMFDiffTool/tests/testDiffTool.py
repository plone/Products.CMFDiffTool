# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#

from plone.app.testing import PLONE_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.CMFDiffTool import registerDiffType
from Products.CMFDiffTool.CMFDiffTool import unregisterDiffType
from unittest import TestCase
from zExceptions import BadRequest


class DummyDiff:
    meta_type = 'Dummy Diff Type'


class DummyDiff2:
    meta_type = 'Second Dummy Diff Type'


class TestDiffTool(TestCase):
    """Test the portal_diff tool"""

    layer = PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.p_diff = getToolByName(self.layer['portal'], 'portal_diff')
        # clear pt_diff registry
        self.p_diff._pt_diffs = {}

        # patch portal_types to list `Document` in the listContentTypes
        # a plausability check is done in the `setDiffForPortalType` method
        # but we have no content registry
        portal_types = getToolByName(self.layer['portal'], 'portal_types')
        self._old_listContentTypes = portal_types.listContentTypes
        portal_types.listContentTypes = lambda: ['Document']
        registerDiffType(DummyDiff)

    def tearDown(self):
        portal_types = getToolByName(self.layer['portal'], 'portal_types')
        portal_types.listContentTypes = self._old_listContentTypes

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import portal_diff
        self.assertTrue(portal_diff.providedBy(self.p_diff))

    def testRegisterDiffType(self):
        """Test registration of Diff types"""
        unregisterDiffType(DummyDiff)
        self.assertNotIn('Dummy Diff Type', self.p_diff.listDiffTypes())
        registerDiffType(DummyDiff)
        self.assertIn('Dummy Diff Type', self.p_diff.listDiffTypes())

    def testSetDiff(self):
        """Test setDiffForPortalType() method"""
        d = {'field1': 'TestDiff', 'field2': 'Dummy Diff Type'}
        self.p_diff.setDiffForPortalType('Document', d)
        self.assertEqual(self.p_diff.getDiffForPortalType('Document'), d)

    def testSetDiffReplaces(self):
        """Test that setDiffForPortalType() replaces old data"""
        d1 = {'field1': 'TestDiff', 'field2': 'Dummy Diff Type'}
        d2 = {'field3': 'Dummy Diff Type'}
        self.p_diff.setDiffForPortalType('Document', d1)
        self.p_diff.setDiffForPortalType('Document', d2)
        self.assertEqual(self.p_diff.getDiffForPortalType('Document'), d2)

    def testSingleSetDiffField(self):
        """Test setDiffField method"""
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.assertEqual(self.p_diff.getDiffForPortalType('Document'),
                         {'title': 'Dummy Diff Type'})

    def testMultipleSetDiffField(self):
        """
        Test setDiffField method adding a second field to one content type
        """
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.p_diff.setDiffField('Document', 'description', 'Dummy Diff Type')
        d = {'title': 'Dummy Diff Type', 'description': 'Dummy Diff Type'}
        self.assertEqual(self.p_diff.getDiffForPortalType('Document'), d)

    def testReplaceSetDiffField(self):
        """Test that setDiffField does a replace for existing fields"""
        registerDiffType(DummyDiff2)
        self.p_diff.setDiffField('Document', 'title', 'Dummy Diff Type')
        self.p_diff.setDiffField('Document', 'title', 'Second Dummy Diff Type')
        d = {'title': 'Second Dummy Diff Type'}
        self.assertEqual(self.p_diff.getDiffForPortalType('Document'), d)
        unregisterDiffType(DummyDiff2)

    def testSetDiffFieldNameFailure(self):
        self.assertRaises(BadRequest, self.p_diff.setDiffField,
                          'Bob', 'title', 'Dummy Diff Type')

    def testSetDiffFieldBlankFieldFailure(self):
        self.assertRaises(BadRequest, self.p_diff.setDiffField,
                          'Document', '', 'Dummy Diff Type')

    def testSetDiffFieldInvalidDiffFailure(self):
        self.assertRaises(BadRequest, self.p_diff.setDiffField,
                          'Document', 'title', 'NoDiff')

    def beforeTearDown(self):
        # Undo changes that don't get rolled back (i.e. module level changes)
        unregisterDiffType(DummyDiff)
