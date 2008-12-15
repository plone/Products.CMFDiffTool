import os
from setuptools import setup, find_packages

version = '1.0dev'

setup(name='Products.CMFDiffTool',
      version=version,
      description="Diff tool for Plone",
      long_description=open(os.path.join("docs", "HISTORY.txt")).read(),
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
        'Products.CMFTestCase',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.GenericSetup',
        'zope.interface',
      ],
      )
