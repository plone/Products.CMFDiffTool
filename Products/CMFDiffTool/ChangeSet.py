#
# ChangeSet.py - Zope object representing the differences between
# objects
#
# Code by Brent Hendricks
#
# (C) 2003 Brent Hendricks - licensed under the terms of the
# GNU General Public License (GPL).  See LICENSE.txt for details

from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import getSecurityManager, ClassSecurityInfo
from ComputedAttribute import ComputedAttribute
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CMFDefault.SkinnedFolder import SkinnedFolder
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from ListDiff import ListDiff
from interfaces.IChangeSet import IChangeSet
import zLOG


### Contructors for Collaboration Request objects
manage_addChangeSetForm = PageTemplateFile('zpt/manage_addChangeSetForm', globals())
                                               
                                               
def manage_addChangeSet(self, id, title='', REQUEST=None):
    """Creates a new ChangeSet object """
    
    id=str(id)
    if not id:
        raise "Bad Request", "Please specify an ID."
     
    self=self.this()
    cs = ChangeSet(id, title)
    self._setObject(id, cs)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')


factory_type_information = (
    {'id': 'ChangeSet',
     'content_icon': 'changeset.png',
     'meta_type': 'Change Set',
     'description': ('A collection of changes between two objects'),
     'product': 'CMFDiffTool',
     'factory': 'manage_addChangeSet',
     'filter_content_types' : 0,
     'immediate_view': 'changeset_edit_form',
     'actions': ({'id': 'view',
                  'name': 'View Changes',
                  'action': 'changeset_view',
                  'permissions': (View,),
                  'visible':1},
                 {'id': 'edit',
                  'name': 'Edit Change set',
                  'action': 'changeset_edit_form',
                  'permissions': (ModifyPortalContent,),
                  'visible':1},
                 )
     },
    )

class ChangeSet(SkinnedFolder, DefaultDublinCoreImpl):
    """A ChangeSet represents the set of differences between two objects"""

    meta_type = "Change Set"
    portal_type = "ChangeSet"
    security = ClassSecurityInfo()

    __implements__ = (IChangeSet)
    
    def __init__(self, id, title=''):
        """ChangeSet constructor"""
        DefaultDublinCoreImpl.__init__(self)
        self.id = id
        self.title = title
        self._diffs = []
        self._added = []
        self._removed = []
        self.ob1_path = []
        self.ob2_path = []
        self.recursive = 0

    def _isSame(self):
        """Returns true if there are no differences between the two objects"""
        return reduce(lambda x, y: x and y, [d.same for d in self._diffs], 1)

    security.declarePublic('same')
    same = ComputedAttribute(_isSame)

    security.declarePublic('computeDiff')
    def computeDiff(self, ob1, ob2, recursive=1, exclude=[], id1=None, id2=None):
        """Compute the differences from ob1 to ob2 (ie. ob2 - ob1).

        The results can be accessed through getDiffs()"""

        # Reset state
        self._diffs = []
        self._added = []
        self._removed = []
        self._changed = []
        self.manage_delObjects(self.objectIds())

        self.ob1_path = self.portal_url.getRelativeContentPath(ob1)
        self.ob2_path = self.portal_url.getRelativeContentPath(ob2)
        
        diff_tool = getToolByName(self, "portal_diff")
        self._diffs = diff_tool.computeDiff(ob1, ob2, id1=id1, id2=id2)

        if recursive and ob1.isPrincipiaFolderish:
            self.recursive = 1
            ld = ListDiff(ob1, ob2, 'objectIds')
            a = ld.oldValue
            b = ld.newValue
            for tag, alo, ahi, blo, bhi in ld.getLineDiffs():
                if tag in ('delete', 'replace'):
                    self._removed.extend(a[alo:ahi])
                if tag in ('insert', 'replace'):
                    self._added.extend(b[blo:bhi])
                if tag == 'equal':
                    self._changed.extend(a[alo:ahi])

            # Ignore any excluded items
            for id in exclude:
                try:
                    self._added.remove(id)
                except ValueError:
                    pass
                try:
                    self._removed.remove(id)
                except ValueError:
                    pass
                try:
                    self._changed.remove(id)
                except ValueError:
                    pass

            # Calculate a ChangeSet for every subobject that has changed
            for id in self._changed:
                self.manage_addProduct['CMFDiffTool'].manage_addChangeSet(id, title='Changes to: %s' % id)
                get_transaction().commit(1)
                self[id].computeDiff(ob1[id], ob2[id], exclude=exclude, id1=id1, id2=id2)

            # Clone any added subobjects
            for id in self._added:
                ob = ob2[id]
                zLOG.LOG("ChangeSet", zLOG.BLATHER, "cloning %s (%s)" % (id, ob))
                self.manage_clone(ob, id)

        self._p_changed = 1


    security.declarePublic('testChanges')
    def testChanges(self, ob):
        """Test the specified object to determine if the change set will apply without errors"""
        for d in self._diffs:
            d.testChanges(ob)

        for id in self._changed:
            cs = self[id]
            child = ob[id]
            cs.testChanges(child)
        
    security.declarePublic('applyChanges')
    def applyChanges(self, ob):
        """Apply the change set to the specified object"""
        for d in self._diffs:
            d.applyChanges(ob)

        if self._removed:
            ob.manage_delObjects(self._removed)

        for id in self._added:
            child = self[id]
            ob.manage_clone(child, id)
        
        for id in self._changed:
            cs = self[id]
            child = ob[id]
            cs.applyChanges(child)

    security.declarePublic('getDiffs')
    def getDiffs(self):
        """Returns the list differences between the two objects.

        Each difference is a single object implementing the IDifference interface"""
        return self._diffs

    security.declarePublic('getSubDiffs')
    def getSubDiffs(self):
        """If the ChangeSet was computed recursively, returns a list
           of ChangeSet objects representing subjects differences

           Each ChangeSet will have the same ID as the objects whose
           difference it represents.
           """
        return [self[id] for id in self._changed]

    security.declarePublic('getAddedItems')
    def getAddedItems(self):
        """If the ChangeSet was computed recursively, returns the list
        of IDs of items that were added.

        A copy of these items is available as a cubject of the ChangeSet
        """
        return self._added

    security.declarePublic('getRemovedItems')
    def getRemovedItems(self):
        """If the ChangeSet was computed recursively, returns the list
        of IDs of items that were removed"""
        return self._removed

InitializeClass(ChangeSet)
