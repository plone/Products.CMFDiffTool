# -*- coding: utf-8 -*-
# BaseTestCase

from plone.app.testing.bbb import PloneTestCase
from Products.CMFDiffTool.testing import CMFDiffToolLayer
from Products.CMFDiffTool.testing import CMFDiffToolATLayer
from Products.CMFDiffTool.testing import CMFDiffToolDXLayer


class BaseTestCase(PloneTestCase):
    """ A base testing class for CMFDiffTool

        It includes a layer which installes the product
        and some testing dependencies in a Plone site.
    """
    layer = CMFDiffToolLayer


class BaseATTestCase(PloneTestCase):
    """ A base testing class for CMFDiffTool

        It includes a layer which installes the product
        and some testing dependencies in a Plone site.
    """
    layer = CMFDiffToolATLayer


class BaseDXTestCase(PloneTestCase):
    """ A base testing class for CMFDiffTool

        It includes a layer which installes the product
        and some testing dependencies in a Plone site.
    """
    layer = CMFDiffToolDXLayer
