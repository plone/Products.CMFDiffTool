# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedFile
from Products.CMFDiffTool import namedfile
from Products.CMFDiffTool import testing
from Products.CMFDiffTool.interfaces import IDifference
from Products.CMFDiffTool.tests.BaseTestCase import BaseDXTestCase


class BinaryDiffTestCase(BaseDXTestCase):

    def test_should_detect_different_filename(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            file=NamedFile(data='contents', filename=u'blah.txt')
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='contents', filename=u'bleh.txt')
        )
        obj2 = self.portal['obj2']

        diff = namedfile.NamedFileBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)

    def test_should_detect_different_data(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='different contents', filename=u'f.txt')
        )
        obj2 = self.portal['obj2']

        diff = namedfile.NamedFileBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)

    def test_should_detect_same_data_and_filename(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj2 = self.portal['obj2']

        diff = namedfile.NamedFileBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertTrue(diff.same)
