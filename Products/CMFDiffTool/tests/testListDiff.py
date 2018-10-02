# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#
from os import linesep
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFDiffTool import testing
from Products.CMFDiffTool.interfaces import IDifference
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.tests.BaseTestCase import BaseDXTestCase


_marker = []


class A:
    attribute = [1, 2, 3]


class B:
    attribute = [1, 2, 3, 4]


class C:
    attribute = {'a': 1, 'b': 2}


class D:
    attribute = {'a': 1, 'b': 2, 'c': 3}


class TestListDiff(BaseDXTestCase):
    """Test the ListDiff class"""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
        )
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
        )

        self.obj1 = self.portal['obj1']
        self.obj2 = self.portal['obj2']

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
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

        b.attribute = ''
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

    def test_inline_diff_vocabulary(self):
        # unchanged, with vocabulary title
        expected = u'<div class="InlineDiff">First Title</div>'
        self._test_diff_list([testing.VOCABULARY_TUPLES[0][0]],
                             [testing.VOCABULARY_TUPLES[0][0]], True, expected)
        # unchanged, without vocabulary title
        expected = u'<div class="InlineDiff">second_value</div>'
        self._test_diff_list([testing.VOCABULARY_TUPLES[1][0]],
                             [testing.VOCABULARY_TUPLES[1][0]], True, expected)
        # changed: add value, with vocabulary title
        expected = u'''<div class="InlineDiff">
    <div class="diff_sub"></div>
    <div class="diff_add">First Title</div>
</div>'''
        self._test_diff_list([],
                             [testing.VOCABULARY_TUPLES[0][0]],
                             False, expected)
        # changed: replaced unique value by another one, displaying titles
        expected = u'''<div class="InlineDiff">
    <div class="diff_sub">First Title</div>
    <div class="diff_add"></div>
</div>
<div class="InlineDiff">
    <div class="diff_sub"></div>
    <div class="diff_add">Third Title</div>
</div>'''
        self._test_diff_list([testing.VOCABULARY_TUPLES[0][0]],
                             [testing.VOCABULARY_TUPLES[2][0]],
                             False, expected)
        # changed: replaced multiple values by others, displaying titles
        expected = u'''<div class="InlineDiff">
    <div class="diff_sub">First Title</div>
    <div class="diff_add"></div>
</div>
<div class="InlineDiff">second_value</div>
<div class="InlineDiff">
    <div class="diff_sub"></div>
    <div class="diff_add">Third Title</div>
</div>'''
        self._test_diff_list([testing.VOCABULARY_TUPLES[0][0],
                              testing.VOCABULARY_TUPLES[1][0]],
                             [testing.VOCABULARY_TUPLES[1][0],
                              testing.VOCABULARY_TUPLES[2][0]],
                             False, expected)
        # changed: replaced multiple values by others, displaying titles
        expected = u'''<div class="InlineDiff">
    <div class="diff_sub"></div>
    <div class="diff_add">Third Title</div>
</div>
<div class="InlineDiff">First Title</div>
<div class="InlineDiff">
    <div class="diff_sub">second_value</div>
    <div class="diff_add"></div>
</div>'''
        self._test_diff_list([testing.VOCABULARY_TUPLES[0][0],
                              testing.VOCABULARY_TUPLES[1][0]],
                             [testing.VOCABULARY_TUPLES[2][0],
                              testing.VOCABULARY_TUPLES[0][0]],
                             False, expected)
        # changed: removed values, displaying titles
        expected = u'''<div class="InlineDiff">
    <div class="diff_sub">First Title</div>
    <div class="diff_add"></div>
</div>
<div class="InlineDiff">
    <div class="diff_sub">second_value</div>
    <div class="diff_add"></div>
</div>'''
        self._test_diff_list([testing.VOCABULARY_TUPLES[0][0],
                              testing.VOCABULARY_TUPLES[1][0]],
                             [], False, expected)

    def _test_diff_list(self, value1, value2, same, expected):
        self.obj1.choices = value1
        self.obj2.choices = value2
        diff = ListDiff(self.obj1, self.obj2, 'choices')
        self.assertEqual(diff.same, same)
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
