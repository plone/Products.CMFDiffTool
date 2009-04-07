# -*- coding: utf-8 -*-
"""Initialize CMFDiffTool Product"""

from Products.CMFCore.utils import ContentInit
from Products.CMFCore.utils import ToolInit
from Products.CMFCore.permissions import AddPortalContent

from Products.CMFDiffTool import CMFDiffTool
from Products.CMFDiffTool import FieldDiff
from Products.CMFDiffTool import TextDiff
from Products.CMFDiffTool import ListDiff
from Products.CMFDiffTool import BinaryDiff
from  Products.CMFDiffTool import ChangeSet
from Products.CMFDiffTool import CMFDTHtmlDiff
from Products.CMFDiffTool import ATCompoundDiff

tools = ( CMFDiffTool.CMFDiffTool,)

contentConstructors = (ChangeSet.manage_addChangeSet,)
contentClasses = (ChangeSet.ChangeSet,)

CMFDiffTool.registerDiffType(BinaryDiff.BinaryDiff)
CMFDiffTool.registerDiffType(FieldDiff.FieldDiff)
CMFDiffTool.registerDiffType(ListDiff.ListDiff)
CMFDiffTool.registerDiffType(TextDiff.TextDiff)
CMFDiffTool.registerDiffType(CMFDTHtmlDiff.CMFDTHtmlDiff)
CMFDiffTool.registerDiffType(ATCompoundDiff.ATCompoundDiff)

def initialize(context):
    ToolInit('CMF Diff Tool',
             tools = tools,
             icon='tool.gif' 
             ).initialize( context )

    ContentInit(ChangeSet.ChangeSet.meta_type,
                content_types = contentClasses,
                extra_constructors = contentConstructors,
                permission = AddPortalContent).initialize(context)
