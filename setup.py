# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '2.1.2'
long_description = open("README.rst").read()
long_description += "\n"
long_description += open("CHANGES.rst").read()

setup(name='Products.CMFDiffTool',
      version=version,
      description="Diff tool for Plone",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          ],
      keywords='Diff Plone',
      author='Brent Hendricks',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.CMFDiffTool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'zope.component',
              'Products.CMFTestCase',
              'collective.testcaselayer',
              'plone.namedfile',
              'plone.app.dexterity',
          ]
      ),
      install_requires=[
          'setuptools',
          'zope.interface',
          'Products.CMFCore',
          'Products.GenericSetup',
          'Acquisition',
          'Zope2',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
