from unittest import TestCase
from Products.CMFCore.utils import getToolByName

from Products.CMFDiffTool.dexteritydiff import DexterityCompoundDiff
from Products.CMFDiffTool import testing


class InstallTestCase(TestCase):

    layer = testing.package_layer

    def test_compound_diff_type_should_be_registered(self):
        diff_tool = getToolByName(self.layer['portal'], 'portal_diff')
        self.assertTrue(
            DexterityCompoundDiff.meta_type in diff_tool.listDiffTypes())
        self.assertTrue(
            diff_tool.getDiffType(DexterityCompoundDiff.meta_type))
