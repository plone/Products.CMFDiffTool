Changelog
=========

2.1.3 (unreleased)
------------------

- Nothing changed yet.


2.1.2 (2015-09-28)
------------------

- Added collective.testcaselayer to test requirements.
  [maurits]


2.1.1 (2015-08-13)
------------------

- Fixed UnicodeDecodeError in dump/ndiff.
  Issue https://github.com/plone/Products.CMFPlone/issues/820
  [maurits]

- Fix: Make ``test_dexteritydiff.py`` tests works with Python 2.6.
  [jensens]

- Provide diff for dexterity behaviors' fields.
  [cedricmessiant]

- Fix bug with encoding in TextDiff.
  [cedricmessiant]


2.1 (2013-05-26)
----------------

- Nothing changed yet.


2.0.2 (2013-03-05)
------------------

- Merge Rafael Oliveira's (@rafaelbco) Dexterity support from
  collective.dexteritydiff.
  [rpatterson]


2.0.1 (2012-09-01)
------------------

- Adjust test assertions to match new diff output in Python 2.7.
  [hannosch]

2.0 - 2010-07-15
----------------

- Make TextDiff more defensive in parsing. This fixes
  http://dev.plone.org/plone/ticket/10716 and
  http://dev.plone.org/plone/ticket/10737.
  [davidblewett]

2.0b3 - 2010-05-20
------------------

- Added filename to BinaryDiff, TextDiff and CMFDTHtmlDiff.
  [davidblewett]

- Added i18n support for filename.
  [davidblewett]

- Updated code + test cases to use os.linesep instead of hard-coding them.
  [davidblewett]

- Updated TextDiff to use the splitlines string method instead of
  splitting on a hard-coded value.
  [davidblewett]

- Fix test failure as a result of string field diff assignment change.
  [alecm]

2.0b2 - 2010-04-28
------------------

- Added inline diff view for simple text fields.
  [alecm]

- Added blob support to ATCompoundDiff.
  [davidblewett]


2.0b1 - 2009-12-27
------------------

- Added missing test dependency.
  [hannosch]

2.0a1 - 2009-11-14
------------------

- Use unicode in diff generation, now that Python's difflib supports it.
  [alecm]

- Adjusted interface test to zope.interface-style interfaces.
  [hannosch]

- Use new-style utility setup for portal_diff instead of the toolset handling.
  [hannosch]

- Added the z3c.autoinclude entry point so this package is automatically loaded
  on Plone 3.3 and above.
  [hannosch]

- Add encoding declaration in python files
  [encolpe]

- Removed the persistent version of the changeset type.
  [hannosch]

- Declare package dependencies and fixed deprecation warnings for use
  of Globals.
  [hannosch]

- Added GS import step registration to the product. It was only registered
  as part of the CMFPlone base profile.
  [hannosch]

- Use the real BadRequest exception instead of relying on a string exception.
  [hannosch]

- Purged old Zope 2 Interface interfaces for Zope 2.12 compatibility.
  [elro]

0.5.2 - 2009-07-08
------------------
- Fix #9355: Support generalized schema extension for AT fields.
  [alecm]

0.5.1 - 2009-06-19
------------------
- Fix #9092: Support archetypes schema extension for ATCompoundDiff.
  [alecm]

0.5 - 2009-05-16
----------------

- Fix #9108: EncodingDecodeError in TextDiff.html_diff
  [encolpe]

0.5b1 - 2009-03-07
------------------

- Move CMF skin layer registration to zcml.
  [wichert]

- Move GenericSetup step registration to zcml.
  [wichert]

0.4 - 2008-10-06
----------------

- Switch to egg-based releases.
  [hannosch]

- Added GS import step registration to the product. It was only registered
  as part of the CMFPlone base profile.
  [hannosch]

0.3.6 - 2008-04-20
------------------

- Added protection against missing diff_tool in the exportimport handler.
  [hannosch]

- Added metadata.xml file to the profile.
  [hannosch]

0.3.5 - 2007-12-02
------------------

- Don't assume there's a portal_type for objects.
  Fixes http://dev.plone.org/plone/ticket/7295
  [alecm]

- Fixed issue causing diffs to break for folders that switched between
  inside and outside ref modifiers.
  [alecm]

- Make ChangeSet compatible with CMF trunk.
  [wiggy]

- Updated componentregisty.xml to new style.
  [hannosch]

0.3.4 - 2007-06-08
------------------

- Fixed i18n markup in at_changeset.pt.
  [hannosch]

0.3.3 - 2007-03-05
------------------

- Removed default config for ATCT types, it goes in Plone now
  [alecm]

0.3.2 - 2007-03-05
------------------

- Added default config for ATCT types
  [alecm]

0.3.1 - 2007-02-09
------------------

- Removed useless status message.
  [hannosch]

- Added ZCML layer setup for tests
  [alecm]

0.3 - 2006-10-02
----------------

- Product installation is now based on a GenericSetup extension profile.
  [hannosch]

- Code modernization for Python 2.4 / CMF 1.6.
  [hannosch]

- Initial version.
  [brentmh]

