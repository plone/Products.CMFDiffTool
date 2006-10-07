from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool import product_globals, ChangeSet
from StringIO import StringIO
import string

def install(self):
    """Register cmf diff skins and add the tool"""
    directory_name = 'ChangeSet'
    
    out = StringIO()

    # Add the tool
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();
    try:
        portal.manage_delObjects('portal_diff')
        out.write("Removed old portal_diff tool\n")
    except:
        pass  # we don't care if it fails
    portal.manage_addProduct['CMFDiffTool'].manage_addTool('CMF Diff Tool', None)
    out.write("Adding CMF Diff Tool\n")

    # Setup the types tool
    typestool = getToolByName(self, 'portal_types')
    for t in ChangeSet.factory_type_information:
        if t['id'] not in typestool.objectIds():
            cfm = apply(ContentFactoryMetadata, (), t)
            typestool._setObject(t['id'], cfm)
            out.write('Registered with the types tool\n')
        else:
            out.write('Object "%s" already existed in the types tool\n' % (
                t['id']))

    # Setup the skins
    skinstool = getToolByName(self, 'portal_skins')
    if directory_name not in skinstool.objectIds():
        # We need to add Filesystem Directory Views for any directories
        # in our skins/ directory.  These directories should already be
        # configured.
        addDirectoryViews(skinstool, 'skins', product_globals)
        out.write("Added %s directory view to portal_skins\n" % directory_name)

    # Now we need to go through the skin configurations and insert
    # directory_name into the configurations.  Preferably, this
    # should be right after where 'custom' is placed.  Otherwise, we
    # append it to the end.
    skins = skinstool.getSkinSelections()
    for skin in skins:
        path = skinstool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if directory_name not in path:
            try: path.insert(path.index('custom')+1, directory_name)
            except ValueError:
                path.append(directory_name)
             
            path = string.join(path, ', ')
            # addSkinSelection will replace existing skins as well.
            skinstool.addSkinSelection(skin, path)
            out.write("Added %s to %s skin\n" % (directory_name, skin))
        else:
            out.write("Skipping %s skin, %s is already set up\n" % (
                skin, directory_name))

    # setup defaults for plone 2.1 at content types
    migration = getToolByName(self, 'portal_migration', None)
    
    if migration is not None and migration.getInstanceVersion().strip().startswith('2.1'):
        portal_types = getToolByName( self, 'portal_types')
        portal_diff  = getToolByName( self, 'portal_diff')
        for type_info in portal_types.objectValues():
            if type_info.global_allow and type_info.product == 'ATContentTypes':
                portal_diff.manage_addDiffField( type_info.getId(),
                                                 'All', 
                                                 'Compound Diff for AT types' )    


        
    return out.getvalue()
