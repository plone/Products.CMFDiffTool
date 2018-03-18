# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#
from Acquisition import aq_base
from os import linesep
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING  # NOQA
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.ChangeSet import BaseChangeSet
from Products.CMFDiffTool.dexteritydiff import DexterityCompoundDiff
from Products.CMFPlone.utils import safe_hasattr
from unittest import TestCase


class TestChangeSet(TestCase):
    """Tests for ChangeSet objects"""

    layer = PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.folder = self.portal
        self.p_diff = getToolByName(self.portal, 'portal_diff')
        cs = BaseChangeSet('my_changeset')
        # ChangeSet needs an acquisition wrapper
        self.cs = cs.__of__(self.portal)
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces import IChangeSet
        self.assertTrue(IChangeSet.implementedBy(BaseChangeSet))

    def setupTestObjects(self):
        self.folder.invokeFactory('Document', 'doc1', title='My Title')
        self.folder.manage_pasteObjects(
            self.folder.manage_copyObjects(['doc1']))
        cdd = DexterityCompoundDiff(self.folder['doc1'], self.folder['doc1'], '')
        self.len_diff = len(cdd._diffs)

    def setupTestFolders(self):
        self.folder.invokeFactory('Folder', 'folder1', title='My Folder Title')
        self.folder.folder1.invokeFactory('Document', 'doc1',
                                          title='My Title1')
        self.folder.folder1.invokeFactory('Document', 'doc2',
                                          title='My Title2')
        self.folder.folder1.invokeFactory('Document', 'doc3',
                                          title='My Title3')
        self.folder.manage_pasteObjects(
            self.folder.manage_copyObjects(['folder1']))
        cdd = DexterityCompoundDiff(
            self.folder['folder1']['doc1'], self.folder['folder1']['doc1'], '')
        self.len_diff = len(cdd._diffs)

    def testChangeSetUnchanged(self):
        self.setupTestObjects()
        self.cs.computeDiff(self.folder['doc1'], self.folder['copy_of_doc1'])
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), self.len_diff)
        self.assertTrue(diffs[0].same)

    def testChangeSetChanged(self):
        self.setupTestObjects()
        self.folder.copy_of_doc1.setTitle('My New Title')
        self.cs.computeDiff(self.folder.doc1, self.folder.copy_of_doc1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), self.len_diff)
        self.assertFalse(diffs[0].same)
        self.assertEqual(diffs[0].ndiff(),
                         '- My Title%s+ My New Title' % linesep)

    def testChangeSetFolderUnchanged(self):
        self.setupTestFolders()
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertTrue(diffs[0].same)
        sub_cs = self.cs.getSubDiffs()
        self.assertEqual(len(sub_cs), 3)
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            self.assertTrue(sub_cs[0].same)
            self.assertTrue(sub_cs[1].same)
            self.assertTrue(sub_cs[2].same)

    def testChangeSetFolderChanged(self):
        self.setupTestFolders()
        self.folder.copy_of_folder1.setTitle('My New Title')
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertFalse(diffs[0].same)
        self.assertEqual(diffs[0].ndiff(),
                         '- My Folder Title%s+ My New Title' % linesep)
        self.assertFalse(self.cs._added)
        self.assertFalse(self.cs._removed)
        sub_cs = self.cs.getSubDiffs()
        self.assertEqual(len(sub_cs), 3)
        # The sub diffs should show no changes
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            self.assertTrue(sub_diffs[0].same)

    def testChangeSetFolderDocChanged(self):
        self.setupTestFolders()
        self.folder.copy_of_folder1.doc1.setTitle('My New Title')
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertTrue(diffs[0].same)
        self.assertTrue(diffs[1].same)
        self.assertFalse(self.cs._added)
        self.assertFalse(self.cs._removed)
        sub_cs = self.cs.getSubDiffs()
        self.assertEqual(len(sub_cs), 3)
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            # doc1 has changed
            if sub_cs[i].getId() == 'doc1':
                self.assertFalse(sub_diffs[0].same)
                self.assertEqual(sub_diffs[0].ndiff(),
                                 '- My Title1%s+ My New Title' % linesep)
            else:
                self.assertTrue(sub_diffs[0].same)

    def testChangeSetFolderDocRemoved(self):
        self.setupTestFolders()
        self.folder.copy_of_folder1.manage_delObjects('doc1')
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertTrue(diffs[0].same)
        self.assertTrue(diffs[1].same)
        sub_cs = self.cs.getSubDiffs()
        # We only have two potentially changed objects
        self.assertEqual(len(sub_cs), 2)
        # The sub diffs should show no changes
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            self.assertTrue(sub_diffs[0].same)
        self.assertFalse(self.cs._added)
        self.assertEqual(list(self.cs._removed), ['doc1'])

    def testChangeSetFolderDocAdded(self):
        self.setupTestFolders()
        self.folder.copy_of_folder1.invokeFactory('Document', 'doc4',
                                                  title='My Doc Title')
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertTrue(diffs[0].same)
        self.assertTrue(diffs[1].same)
        sub_cs = self.cs.getSubDiffs()
        self.assertEqual(len(sub_cs), 3)
        # The sub diffs should show no changes
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            self.assertTrue(sub_diffs[0].same)
        self.assertFalse(self.cs._removed)
        self.assertEqual(list(self.cs._added), ['doc4'])

    def testChangeSetFolderReordered(self):
        self.setupTestFolders()
        if safe_hasattr(aq_base(self.folder.copy_of_folder1),
                        'moveObjectsToTop'):
            self.folder.copy_of_folder1.moveObjectsToTop(['doc3'])
        elif safe_hasattr(aq_base(self.folder.copy_of_folder1),
                          'moveObjectsByDelta'):
            self.folder.copy_of_folder1.moveObjectsByDelta(['doc3'], -3)
        else:
            # We don't have an orderable folder give up
            return
        self.cs.computeDiff(self.folder.folder1, self.folder.copy_of_folder1)
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertTrue(diffs[0].same)
        self.assertFalse(self.cs._added)
        self.assertFalse(self.cs._removed)
        sub_cs = self.cs.getSubDiffs()
        self.assertEqual(len(sub_cs), 3)
        # The sub diffs should show no changes
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            self.assertTrue(sub_diffs[0].same)
        # XXX we need an explicit way of noting reorders

    def testChangeSetFolderComplex(self):
        self.setupTestFolders()
        # Add a new sub object
        self.folder.copy_of_folder1.invokeFactory('Document', 'doc4',
                                                  title='My Doc Title')
        # Delete a sub object
        self.folder.copy_of_folder1.manage_delObjects('doc2')
        # Change one object
        self.folder.copy_of_folder1.doc3.setTitle('My New Title')
        # Change the folder itself
        self.folder.copy_of_folder1.setTitle('My New Title')
        # Move the changed object
        if safe_hasattr(aq_base(self.folder.copy_of_folder1),
                        'moveObjectsToTop'):
            self.folder.copy_of_folder1.moveObjectsToTop(['doc3'])
        elif safe_hasattr(aq_base(self.folder.copy_of_folder1),
                          'moveObjectsByDelta'):
            self.folder.copy_of_folder1.moveObjectsByDelta(['doc3'], -3)
        else:
            # We don't have an orderable folder give up
            return

        self.cs.computeDiff(self.folder['folder1'], self.folder['copy_of_folder1'])
        diffs = self.cs.getDiffs()
        self.assertEqual(len(diffs), 14)
        self.assertFalse(diffs[0].same)
        self.assertEqual(diffs[0].ndiff(),
                         '- My Folder Title%s+ My New Title' % linesep)
        self.assertEqual(list(self.cs._added), ['doc4'])
        self.assertEqual(list(self.cs._removed), ['doc2'])
        sub_cs = self.cs.getSubDiffs()
        # We only have two potentially changed objects
        self.assertEqual(len(sub_cs), 2)
        # The sub diffs should show no changes
        for i in range(len(sub_cs)):
            self.assertTrue(isinstance(sub_cs[i], BaseChangeSet))
            sub_diffs = sub_cs[i].getDiffs()
            self.assertEqual(len(sub_diffs), self.len_diff)
            if sub_cs[i].getId() == 'doc3':
                self.assertFalse(sub_diffs[0].same)
                self.assertEqual(sub_diffs[0].ndiff(),
                                 '- My Title3%s+ My New Title' % linesep)
            else:
                self.assertTrue(sub_diffs[1].same)
        # XXX we need an explicit way of noting reorders
