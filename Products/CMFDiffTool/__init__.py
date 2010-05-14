# -*- coding: utf-8 -*-
"""Initialize CMFDiffTool Product"""
# Set up a MessageFactory for the cmfdifftool domain
from zope.i18nmessageid import MessageFactory
CMFDiffToolMessageFactory = MessageFactory('cmfdifftool')

from Products.CMFCore.utils import ToolInit

from Products.CMFDiffTool import CMFDiffTool
from Products.CMFDiffTool import FieldDiff
from Products.CMFDiffTool import TextDiff
from Products.CMFDiffTool import ListDiff
from Products.CMFDiffTool import BinaryDiff
from Products.CMFDiffTool import CMFDTHtmlDiff
from Products.CMFDiffTool import ATCompoundDiff

tools = ( CMFDiffTool.CMFDiffTool,)

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
