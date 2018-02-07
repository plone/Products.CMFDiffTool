# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#
from os import linesep
from plone.app.testing import PLONE_INTEGRATION_TESTING
from Products.CMFDiffTool.ListDiff import ListDiff
from unittest import TestCase


_marker = []


class A:
    attribute = [1, 2, 3]


class B:
    attribute = [1, 2, 3, 4]


class C:
    attribute = {"a": 1, "b": 2}


class D:
    attribute = {"a": 1, "b": 2, "c": 3}


class TestListDiff(TestCase):
    """Test the ListDiff class"""

    layer = PLONE_INTEGRATION_TESTING

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import IDifference
        self.assertTrue(IDifference.implementedBy(ListDiff))

    def testInvalidValue(self):
        """ Test if no error with invalid values """
        a = A()
        a.attribute = []
        b = A()

        b.attribute = None
        diff = ListDiff(a, b, 'attribute')
        self.assertEqual([('insert', 0, 0, 0, 1)], diff.getLineDiffs())

        b.attribute = 0
        diff = ListDiff(a, b, 'attribute')
        self.assertEqual([('insert', 0, 0, 0, 1)], diff.getLineDiffs())

        b.attribute = ""
        diff = ListDiff(a, b, 'attribute')
        self.assertEqual([('insert', 0, 0, 0, 1)], diff.getLineDiffs())

    def testAttributeSame(self):
        """Test attribute with same value"""
        a = A()
        diff = ListDiff(a, a, 'attribute')
        self.assertTrue(diff.same)

    def testAttributeDiff(self):
        """Test attribute with different value"""
        a = A()
        b = B()
        diff = ListDiff(a, b, 'attribute')
        self.assertFalse(diff.same)

    def testGetLineDiffsSame(self):
        """test getLineDiffs() method with same value"""
        a = A()
        diff = ListDiff(a, a, 'attribute')
        expected = [('equal', 0, 3, 0, 3)]
        self.assertEqual(diff.getLineDiffs(), expected)

    def testGetLineDiffsDifferent(self):
        """test getLineDiffs() method with different value"""
        a = A()
        b = B()
        diff = ListDiff(a, b, 'attribute')
        expected = [('equal', 0, 3, 0, 3), ('insert', 3, 3, 3, 4)]
        self.assertEqual(diff.getLineDiffs(), expected)

    def testSameText(self):
        """Test text diff output with no diff"""
        a = A()
        diff = ListDiff(a, a, 'attribute')
        expected = '  1%(linesep)s  2%(linesep)s  3' % {'linesep': linesep}
        self.assertEqual(diff.ndiff(), expected)

    def testDiffText(self):
        """Test text diff output with no diff"""
        a = A()
        b = B()
        expected = '  1%(linesep)s  2%(linesep)s  3%(linesep)s+ 4' % \
                   {'linesep': linesep}
        diff = ListDiff(a, b, 'attribute')
        self.assertEqual(diff.ndiff(), expected)

    def test_inline_diff(self):
        a = A()
        b = B()
        expected = """<div class="InlineDiff">1</div>
<div class="InlineDiff">2</div>
<div class="InlineDiff">3</div>
<div class="InlineDiff">
    <div class="diff_sub"></div>
    <div class="diff_add">4</div>
</div>"""
        diff = ListDiff(a, b, 'attribute')
        self.assertEqual(diff.inline_diff(), expected)

    def testGetLineDictDiffsSame(self):
        """test getLineDiffs() method with dict same value"""
        c = C()
        diff = ListDiff(c, c, 'attribute')
        expected = [('equal', 0, 1, 0, 1)]
        self.assertEqual(diff.getLineDiffs(), expected)

    def testGetLineDictDiffsDifferent(self):
        """test getLineDiffs() method with dict different value"""
        c = C()
        d = D()
        diff = ListDiff(c, d, 'attribute')
        expected = [('replace', 0, 1, 0, 1)]
        self.assertEqual(diff.getLineDiffs(), expected)