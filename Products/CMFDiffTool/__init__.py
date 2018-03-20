# -*- coding: utf-8 -*-
"""Initialize CMFDiffTool Product"""
# Set up a MessageFactory for the cmfdifftool domain
from zope.i18nmessageid import MessageFactory
CMFDiffToolMessageFactory = MessageFactory('plone')

from Products.CMFCore.utils import ToolInit  # NOQA
from Products.CMFDiffTool import CMFDiffTool  # NOQA
from Products.CMFDiffTool import FieldDiff  # NOQA
from Products.CMFDiffTool import TextDiff  # NOQA
from Products.CMFDiffTool import ListDiff  # NOQA
from Products.CMFDiffTool import BinaryDiff  # NOQA
from Products.CMFDiffTool import CMFDTHtmlDiff  # NOQA
from Products.CMFDiffTool import ATCompoundDiff  # NOQA


CMFDiffTool.registerDiffType(BinaryDiff.BinaryDiff)
CMFDiffTool.registerDiffType(FieldDiff.FieldDiff)
CMFDiffTool.registerDiffType(ListDiff.ListDiff)
CMFDiffTool.registerDiffType(TextDiff.TextDiff)
CMFDiffTool.registerDiffType(TextDiff.AsTextDiff)
CMFDiffTool.registerDiffType(CMFDTHtmlDiff.CMFDTHtmlDiff)
CMFDiffTool.registerDiffType(ATCompoundDiff.ATCompoundDiff)

# Soft plone.namedfile dependency
try:
    from Products.CMFDiffTool import namedfile
except ImportError:
    pass
else:
    CMFDiffTool.registerDiffType(namedfile.NamedFileBinaryDiff)
    CMFDiffTool.registerDiffType(namedfile.NamedFileListDiff)

# Soft Dexterity dependency
try:
    from Products.CMFDiffTool import dexteritydiff
    from Products.CMFDiffTool import choicediff
except ImportError:
    pass
else:
    CMFDiffTool.registerDiffType(choicediff.ChoiceDiff)
    CMFDiffTool.registerDiffType(dexteritydiff.DexterityCompoundDiff)

tools = (CMFDiffTool.CMFDiffTool, )


def initialize(context):
    ToolInit('CMF Diff Tool',
             tools=tools,
             icon='tool.gif'
             ).initialize(context)
