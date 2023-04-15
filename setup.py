from setuptools import find_packages
from setuptools import setup


version = "4.0.1"

setup(
    name="Products.CMFDiffTool",
    version=version,
    description="Diff tool for Plone",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="Diff Plone",
    author="Brent Hendricks",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/Products.CMFDiffTool",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["Products"],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            "zope.component",
            "plone.app.testing",
            "plone.namedfile",
            "plone.app.contenttypes[test]",
            "zope.intid",
        ]
    ),
    python_requires=">=3.8",
    install_requires=[
        "ExtensionClass",
        "Products.GenericSetup",
        "Products.PortalTransforms",
        "Zope",
        "setuptools",
        "plone.base",
        "z3c.relationfield",
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
