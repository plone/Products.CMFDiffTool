# -*- coding: utf-8 -*-
from Products.CMFDiffTool.testing import CMFDiffToolDXLayer

import six
import unittest


class BaseDXTestCase(unittest.TestCase):
    """ A base testing class for CMFDiffTool

        It includes a layer which installes the product
        and some testing dependencies in a Plone site.
    """
    layer = CMFDiffToolDXLayer

    def setUp(self):
        self.portal = self.layer['portal']


if six.PY2:
    from plone.app.testing.bbb import PloneTestCase
    from Products.CMFDiffTool.testing import CMFDiffToolATLayer

    class BaseATTestCase(PloneTestCase):
        """ A base testing class for CMFDiffTool

            It includes a layer which installes the product
            and some testing dependencies in a Plone site.
        """
        layer = CMFDiffToolATLayer
