# -*- coding: utf-8 -*-
from plone.namedfile import NamedFile
from Products.CMFDiffTool import namedfile
from Products.CMFDiffTool.interfaces import IDifference

import unittest


class DummyType(object):
    def __init__(self, files):
        """`files` is a sequence of (data, filename) tuples."""
        self.files = files and [
            NamedFile(data=d, filename=fn) for (d, fn) in files]


class AsTextDiffTestCase(unittest.TestCase):

    def test_should_diff_file_lists_correctly(self):
        self._test_diff_files(
            [('data1', u'filename1')],
            [('data2', u'filename2')],
            False,
        )
        self._test_diff_files(
            [('data1', u'filename1'), ('datax', u'filenamex')],
            [('data1', u'filename1'), ('datay', u'filenamey')],
            False,
        )
        self._test_diff_files(
            [('data1', u'filename1'), ('datax', u'filenamex')],
            [('datax', u'filenamex'), ('data1', u'filename1')],
            False,
        )
        self._test_diff_files(
            [('data1', u'filename1')],
            [('data1', u'filename1'), ('datax', u'filenamex')],
            False,
        )
        self._test_diff_files(
            [('data1', u'filename1')],
            [('data1', u'filename1')],
            True,
        )
        self._test_diff_files(
            [('data1', u'filename1'), ('datax', u'filenamex')],
            [('data1', u'filename1'), ('datax', u'filenamex')],
            True,
        )
        self._test_diff_files(
            [('data1', u'filename1'), ('datax', u'filenamex')],
            None,
            False,
        )
        self._test_diff_files(
            [('data1', u'filename1'), ('datax', u'filenamex')],
            [],
            False,
        )
        self._test_diff_files(
            [
                ('<script>alert("Hacker data 1")</script>', u'filename1'),
                ('<script>alert("Hacker data 2")</script>', u'filename2'),
            ],
            [
                ('data1', u'<script>alert("Hacker data")</script>.txt'),
                ('<script>alert("Hacker data 2")</script>', u'filename2'),
            ],
            False,
        )
        self._test_diff_files(None, None, True)
        self._test_diff_files([], [], True)
        self._test_diff_files([], None, True)

    def _test_diff_files(self, files1, files2, same):
        diff = namedfile.NamedFileListDiff(
            DummyType(files1), DummyType(files2), 'files')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, same)
        inline = diff.inline_diff()
        self.assertNotEqual(bool(inline), same)
        if inline:
            # No hacker can catch us unawares.
            self.assertNotIn("<script", inline)
