from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.CMFDiffTool.config import PROJECTNAME, GLOBALS

def install(self):
    out = StringIO()

    portal_setup = getToolByName(self, 'portal_setup')
    portal_setup.setImportContext('profile-Products.CMFDiffTool:CMFDiffTool')
    portal_setup.runAllImportSteps()

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
