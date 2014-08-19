# -*- coding: utf-8 -*-
# BaseTestCase

from plone.app.testing.bbb import PloneTestCase
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class CMFDiffToolBaseSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setupPloneSite(self, portal):
        applyProfile(portal, 'Products.CMFDiffTool:CMFDiffTool')


CMFDiffToolBaseLayer = CMFDiffToolBaseSandboxLayer()

class BaseTestCase(PloneTestCase):
    """This is a stub now, but in case you want to try
       something fancy on Your Branch (tm), put it here.
    """

    layer = CMFDiffToolBaseLayer


class CMFDiffToolSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'CMFDiffTool')

    def setUpPloneSite(self, portal):
        """Set up additional products and ZCML required to test
        this product.
        """
        try:
            from archetypes import schemaextender
            self.loadZCML(package=schemaextender)
        except ImportError:
            pass

CMFDiffToolLayer = CMFDiffToolSandboxLayer()

class ATBaseTestCase(PloneTestCase):
    """
    For tests that need archetypes
    """
    layer = CMFDiffToolLayer
