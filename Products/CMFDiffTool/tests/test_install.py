from .BaseTestCase import BaseTestCase
from Products.CMFCore.utils import getToolByName

from Products.CMFDiffTool.dexteritydiff import DexterityCompoundDiff


class InstallTestCase(BaseTestCase):

    def test_compound_diff_type_should_be_registered(self):
        diff_tool = getToolByName(self.portal, 'portal_diff')
        self.assertTrue(
            DexterityCompoundDiff.meta_type in diff_tool.listDiffTypes())
        self.assertTrue(
            diff_tool.getDiffType(DexterityCompoundDiff.meta_type))
