from zope.component import getUtility
from zope.component import queryUtility

from Products.CMFCore.interfaces import ITypesTool
from Products.CMFDiffTool.interfaces import IDiffTool
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import exportObjects

from zope.interface import implements

class DiffToolXMLAdapter(XMLAdapterBase):
    """In- and exporter for DiffTool.
    """
    implements(IDiffTool)

    name = 'diff_tool'

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node=self._doc.createElement("object")
        node.appendChild(self._extractDiffToolSettings())

        self._logger.info("DiffTool settings exported.")
        return node

    def _importNode(self, node):
        if self.environ.shouldPurge():
            self._purgeDiffToolSettings()

        self._initDiffToolSettings(node)
        self._logger.info("DiffTool settings imported.")

    def _purgeDiffToolSettings(self):
        self.context.manage_editDiffFields({})

    def _initDiffToolSettings(self, node):
        for child in node.childNodes:
            if child.nodeName == "difftypes":
                for type_entry in child.getElementsByTagName("type"):
                    ptype = type_entry.getAttribute("portal_type")
                    fields = {}
                    for field in type_entry.getElementsByTagName("field"):
                        name = field.getAttribute("name")
                        diff = field.getAttribute("difftype")
                        fields[name] = diff
                        self.context.setDiffForPortalType(ptype, fields)


    def _extractDiffToolSettings(self):
        node=self._doc.createElement("difftypes")
        ttool = getUtility(ITypesTool)
        for ptype in ttool.listContentTypes():
            diffs = self.context.getDiffForPortalType(ptype)
            if diffs:
                child=self._doc.createElement("type")
                child.setAttribute("portal_type", ptype)
                node.appendChild(child)
            for field_name, diff in diffs.items():
                field=self._doc.createElement("field")
                field.setAttribute("name", field_name)
                field.setAttribute("difftype", diff)
                child.appendChild(field)
        return node


def importDiffTool(context):
    """Import Factory Tool configuration.
    """
    site = context.getSite()
    tool = getUtility(IDiffTool)

    importObjects(tool, '', context)


def exportDiffTool(context):
    """Export Factory Tool configuration.
    """
    site = context.getSite()
    tool = queryUtility(IDiffTool)
    if tool is None:
        logger = context.getLogger("difftool")
        logger.info("Nothing to export.")
        return

    exportObjects(tool, '', context)
