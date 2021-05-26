# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedFile
from Products.CMFDiffTool import BinaryDiff
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
            file=NamedFile(data='contents', filename=u'blah.txt'),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='contents', filename=u'bleh.txt'),
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
            file=NamedFile(data='contents', filename=u'f.txt'),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='different contents', filename=u'f.txt'),
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
            file=NamedFile(data='contents', filename=u'f.txt'),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='contents', filename=u'f.txt'),
        )
        obj2 = self.portal['obj2']

        diff = namedfile.NamedFileBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertTrue(diff.same)

    def test_should_escape_html(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            file=NamedFile(data='contents', filename=u'blah.txt'),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            file=NamedFile(data='<script>alert("Hacker data")</script>', filename=u'<script>alert("Hacker filename")</script>.txt'),
        )
        obj2 = self.portal['obj2']

        diff = namedfile.NamedFileBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)
        # The script tag should be escaped.
        self.assertNotIn("<script", diff.inline_diff())
        self.assertIn("&gt;", diff.inline_diff())

        # Test the more basic BinaryDiff.
        # It only compares the file names.
        # It uses the 'getFilename' method of the file,
        # which namedfiles do not have.  So we hack it.
        obj1.file.getFilename = lambda: obj1.file.filename
        obj2.file.getFilename = lambda: obj2.file.filename
        diff = BinaryDiff.BinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)
        # The script tag should be escaped.
        self.assertNotIn("<script", diff.inline_diff())
        self.assertIn("&gt;", diff.inline_diff())
