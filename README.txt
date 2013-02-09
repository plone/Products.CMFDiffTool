Overview
========

Diff tool for Plone.

Dexterity
---------

To enable versioning for a Dexterity content type you need to:

1. Install `plone.app.versioningbehavior`_ and use it on your content type.
2. Enable versioning for the type in the types control panel.
3. Install this package.
4. Go to the ``portal_diff`` tool ZMI page.
5. Add ``Compound Diff for Dexterity types`` for your content type. ``Field name`` can be anything,
   e.g: "any".

You can enable versioning on Dexterity content types without these
steps, but then you'll have to add the correct "diff type" for each
field of your content type.

.. References
.. _`Products.CMFDiffTool`: http://pypi.python.org/pypi/Products.CMFDiffTool
.. _Dexterity: http://pypi.python.org/pypi/plone.app.dexterity
.. _`plone.app.versioningbehavior`: http://pypi.python.org/pypi/plone.app.versioningbehavior
