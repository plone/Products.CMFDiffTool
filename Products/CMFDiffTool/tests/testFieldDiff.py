# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#
from os import linesep
from plone.app.testing import PLONE_INTEGRATION_TESTING
from Products.CMFDiffTool.FieldDiff import dump
from Products.CMFDiffTool.FieldDiff import FieldDiff
from unittest import TestCase


_marker = []


class A:
    attribute = 'value'

    def method(self):
        return 'method value'


class B:
    attribute = 'different value'

    def method(self):
        return 'different method value'


class U:
    attribute = u"\xfcnicode value"

    def method(self):
        return u"different method val\xfce"


class TestFieldDiff(TestCase):
    """Test the FieldDiff class"""

    layer = PLONE_INTEGRATION_TESTING

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import IDifference
        self.assertTrue(IDifference.implementedBy(FieldDiff))

    def testAttributeSame(self):
        """Test attribute with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        self.assertTrue(fd.same)
        uu = U()
        fd = FieldDiff(uu, uu, 'attribute')
        self.assertTrue(fd.same)

    def testMethodSame(self):
        """Test method with same value"""
        a = A()
        fd = FieldDiff(a, a, 'method')
        self.assertTrue(fd.same)
        uu = U()
        fd = FieldDiff(uu, uu, 'method')
        self.assertTrue(fd.same)

    def testAttributeDiff(self):
        """Test attribute with different value"""
        a = A()
        b = B()
        uu = U()
        fd = FieldDiff(a, b, 'attribute')
        self.assertFalse(fd.same)
        fd = FieldDiff(a, uu, 'attribute')
        self.assertFalse(fd.same)

    def testMethodDiff(self):
        """Test method with different value"""
        a = A()
        b = B()
        uu = U()
        fd = FieldDiff(a, b, 'method')
        self.assertFalse(fd.same)
        fd = FieldDiff(a, uu, 'method')
        self.assertFalse(fd.same)

    def testGetLineDiffsSame(self):
        """test getLineDiffs() method with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        expected = [('equal', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)
        uu = U()
        fd = FieldDiff(uu, uu, 'attribute')
        expected = [('equal', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)

    def testGetLineDiffsDifferent(self):
        """test getLineDiffs() method with different value"""
        a = A()
        b = B()
        uu = U()
        fd = FieldDiff(a, b, 'attribute')
        expected = [('replace', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)
        fd = FieldDiff(a, uu, 'attribute')
        expected = [('replace', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)

    def testSameText(self):
        """Test text diff output with same value"""
        a = A()
        fd = FieldDiff(a, a, 'attribute')
        self.assertEqual(fd.ndiff(), '  value')
        uu = U()
        fd = FieldDiff(uu, uu, 'attribute')
        self.assertEqual(fd.ndiff(), u'  \xfcnicode value')

    def testDiffText(self):
        """Test text diff output with different value"""
        a = A()
        b = B()
        uu = U()
        expected = '- value%s+ different value' % linesep
        fd = FieldDiff(a, b, 'attribute')
        self.assertEqual(fd.ndiff(), expected)
        expected = u"- value%s+ \xfcnicode value" % linesep
        fd = FieldDiff(a, uu, 'attribute')
        self.assertEqual(fd.ndiff(), expected)

    def test_dump_text(self):
        """Test dumping a diff of text."""
        diff = []
        dump('-', ['support'], 0, 1, diff)
        self.assertEqual(diff, ['- support'])
        # Try unicode, a 'u' with an umlaut.
        diff = []
        dump('+', [u's\xfcpport'], 0, 1, diff)
        self.assertEqual(diff, [u'+ s\xfcpport'])
        # Combine them.
        diff = []
        dump('-', ['support'], 0, 1, diff)
        dump('+', [u's\xfcpport'], 0, 1, diff)
        self.assertEqual(diff, ['- support', u'+ s\xfcpport'])

    def test_dump_integer(self):
        """Test dumping a diff of integers."""
        diff = []
        dump('-', [4], 0, 1, diff)
        self.assertEqual(diff, ['- 4'])
        dump('+', [42], 0, 1, diff)
        self.assertEqual(diff, ['- 4', '+ 42'])

    def test_dump_float(self):
        """Test dumping a diff of floats."""
        diff = []
        dump('-', [1.1], 0, 1, diff)
        self.assertEqual(diff, ['- 1.1'])
        dump('+', [1.2], 0, 1, diff)
        self.assertEqual(diff, ['- 1.1', '+ 1.2'])

    def test_dump_boolean(self):
        """Test dumping a diff of booleans."""
        diff = []
        dump('-', [True], 0, 1, diff)
        self.assertEqual(diff, ['- True'])
        dump('+', [False], 0, 1, diff)
        self.assertEqual(diff, ['- True', '+ False'])
