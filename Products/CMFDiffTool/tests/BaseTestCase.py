# -*- coding: utf-8 -*-
# BaseTestCase

from Products.CMFTestCase.ctc import CMFTestCase
from Products.CMFTestCase.ctc import setupCMFSite
from Products.CMFTestCase.ctc import installProduct

installProduct('CMFDiffTool')

setupCMFSite(extension_profiles=['Products.CMFDiffTool:CMFDiffTool'])

class BaseTestCase(CMFTestCase):
    """This is a stub now, but in case you want to try
       something fancy on Your Branch (tm), put it here.
    """
