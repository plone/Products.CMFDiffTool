from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='Products.CMFDiffTool',
      version=version,
      description="Diff tool for Plone",
      long_description="""\
""",
      classifiers=[
        'Framework :: Plone',
        'Framework :: Zope2',
      ],
      keywords='Diff Plone',
      author='Brent Hendricks',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.i18n',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      )