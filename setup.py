# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '3.2.1'

setup(
    name='Products.CMFDiffTool',
    version=version,
    description="Diff tool for Plone",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords='Diff Plone',
    author='Brent Hendricks',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/Products.CMFDiffTool',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'zope.component',
            'plone.app.testing',
            'plone.namedfile',
            'plone.app.dexterity',
            'plone.app.contenttypes',
            'plone.app.robotframework',  # Only because plone.app.event fails
            ]
    ),
    install_requires=[
        'setuptools',
        'six',
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
