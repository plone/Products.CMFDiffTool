"""Initialize CMFDiffTool Product"""

import sys
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils
from Products.CMFCore import CMFCorePermissions
import CMFDiffTool
import FieldDiff
import TextDiff
import ListDiff
import BinaryDiff
import ChangeSet
import CMFDTHtmlDiff
import ATCompoundDiff

this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( CMFDiffTool.CMFDiffTool,)

contentConstructors = (ChangeSet.manage_addChangeSet,)
contentClasses = (ChangeSet.ChangeSet,)
z_bases = utils.initializeBasesPhase1(contentClasses, this_module)

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())
registerDirectory('skins/ChangeSet', globals())

CMFDiffTool.registerDiffType(BinaryDiff.BinaryDiff)
CMFDiffTool.registerDiffType(FieldDiff.FieldDiff)
CMFDiffTool.registerDiffType(ListDiff.ListDiff)
CMFDiffTool.registerDiffType(TextDiff.TextDiff)
CMFDiffTool.registerDiffType(CMFDTHtmlDiff.CMFDTHtmlDiff)
CMFDiffTool.registerDiffType(ATCompoundDiff.ATCompoundDiff)

def initialize(context):
    utils.ToolInit('CMF Diff Tool',
                    tools = tools,
                    icon='tool.gif' 
                    ).initialize( context )

    utils.initializeBasesPhase2( z_bases, context )
    utils.ContentInit(ChangeSet.ChangeSet.meta_type,
                      content_types = contentClasses,
                      permission = CMFCorePermissions.AddPortalContent,
                      extra_constructors = contentConstructors,
                      fti = ChangeSet.factory_type_information).initialize(context)
