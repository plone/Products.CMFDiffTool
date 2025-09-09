from Products.CMFDiffTool.testing import CMFDiffToolDXLayer

import unittest


class BaseDXTestCase(unittest.TestCase):
    """A base testing class for CMFDiffTool

    It includes a layer which installs the product
    and some testing dependencies in a Plone site.
    """

    layer = CMFDiffToolDXLayer

    def setUp(self):
        self.portal = self.layer["portal"]
