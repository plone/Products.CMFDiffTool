# -*- coding: utf-8 -*-
from datetime import date
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile import NamedFile
from Products.CMFDiffTool import testing
from Products.CMFDiffTool.dexteritydiff import DexterityCompoundDiff
from Products.CMFDiffTool.dexteritydiff import EXCLUDED_FIELDS
from Products.CMFDiffTool.interfaces import IDifference
from Products.CMFDiffTool.tests.BaseTestCase import BaseDXTestCase
from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds



class DexterityDiffTestCase(BaseDXTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_should_diff(self):
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            title=u'Object 1',
            description=u'Desc 1',
            text=u'Text 1'
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            title=u'Object 2',
            text=u'Text 2'
        )
        obj2 = self.portal['obj2']

        diffs = DexterityCompoundDiff(obj1, obj2, 'any')
        for d in diffs:
            self.assertTrue(IDifference.providedBy(d))
            self.assertFalse(d.field in EXCLUDED_FIELDS)
            if d.field in ['title', 'description', 'text']:
                self.assertFalse(
                    d.same, 'Field %s should be different.' % d.field)
            else:
                self.assertTrue(d.same, 'Field %s should be equal.' % d.field)

    def test_should_provide_inline_diff_for_date_field(self):
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            date=date(2001, 1, 1),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            date=date(2001, 1, 2),
        )
        obj2 = self.portal['obj2']

        diffs = DexterityCompoundDiff(obj1, obj2, 'any')
        for d in diffs:
            if d.field == 'date':
                self.assertTrue(d.inline_diff())

    def test_should_provide_inline_diff_for_file_list_field(self):
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            files=None,
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            files=[NamedFile(data='data', filename=u'a.txt')],
        )
        obj2 = self.portal['obj2']

        diffs = DexterityCompoundDiff(obj1, obj2, 'any')
        for d in diffs:
            if d.field == 'files':
                inline_diff = d.inline_diff()
                self.assertTrue(inline_diff)
                self.assertTrue(obj2.files[0].filename in inline_diff)

    def test_should_provide_diff_for_behaviors_fields(self):
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            date=date(2001, 1, 1),
        )
        obj1 = self.portal['obj1']

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            date=date(2001, 1, 2),
        )
        obj2 = self.portal['obj2']

        diffs = DexterityCompoundDiff(obj1, obj2, 'any')
        fields = [d.field for d in diffs]
        self.assertIn('title', fields)
        self.assertIn('description', fields)

    def test_should_provide_diff_for_related_fields(self):
        intids = getUtility(IIntIds)

        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj1',
            title=u'Object 1',
            description=u'Desc 1',
            text=u'Text 1'
        )
        obj1 = self.portal['obj1']

        intid = intids.register(obj1)
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj2',
            title=u'Object 2',
            relatedItems=[RelationValue(intid)],
        )
        obj2 = self.portal['obj2']

        intid = intids.register(obj2)
        self.portal.invokeFactory(
            testing.TEST_CONTENT_TYPE_ID,
            'obj3',
            title=u'Object 3',
            relatedItems=[RelationValue(intid)],
        )
        obj3 = self.portal['obj3']

        diffs = DexterityCompoundDiff(obj2, obj3, 'any')
        for d in diffs:
            if d.field == 'relatedItems':
                inline_diff = d.inline_diff()
                self.assertTrue(inline_diff)
                i_diff_sub = inline_diff.index('<div class="diff_sub">')
                i_obj1 = inline_diff.index('Object 1')
                i_diff_add = inline_diff.index('<div class="diff_add">')
                i_obj2 = inline_diff.index('Object 2')
                self.assertTrue(i_diff_sub < i_obj1 < i_diff_add < i_obj2)

                n_diff = d.ndiff()
                self.assertTrue(n_diff)
                i_rem = n_diff.index('-')
                i_obj1 = n_diff.index('obj1')
                i_add = n_diff.index('+')
                i_obj2 = n_diff.index('obj2')
                self.assertTrue(i_rem < i_obj1 < i_add < i_obj2)
