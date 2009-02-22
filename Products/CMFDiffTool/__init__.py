"""Initialize CMFDiffTool Product"""

import sys
from Products.CMFCore import utils

from Products.CMFDiffTool import CMFDiffTool
from Products.CMFDiffTool import FieldDiff
from Products.CMFDiffTool import TextDiff
from Products.CMFDiffTool import ListDiff
from Products.CMFDiffTool import BinaryDiff
from Products.CMFDiffTool import CMFDTHtmlDiff
from Products.CMFDiffTool import ATCompoundDiff

this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( CMFDiffTool.CMFDiffTool,)

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
