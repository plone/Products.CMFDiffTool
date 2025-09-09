from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


TEST_CONTENT_TYPE_ID = "TestContentType"

VOCABULARY_TUPLES = [
    ("first_value", "First Title"),
    ("second_value", None),
    ("third_value", "Third Title"),
]

VOCABULARY = SimpleVocabulary(
    [SimpleTerm(value=v, title=t) for (v, t) in VOCABULARY_TUPLES]
)


def vocabulary_factory(context):
    return VOCABULARY


class DXLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpPloneSite(self, portal):
        """Set up additional products and ZCML required to test
        this product.
        """
        # setup dexterity
        types_tool = getToolByName(portal, "portal_types")

        sm = getSiteManager(portal)
        sm.registerUtility(
            component=vocabulary_factory,
            provided=IVocabularyFactory,
            name="Products.CMFDiffTool.testing.VOCABULARY",
        )

        fti = DexterityFTI(
            TEST_CONTENT_TYPE_ID,
            factory=TEST_CONTENT_TYPE_ID,
            global_allow=True,
            behaviors=(
                "plone.app.versioningbehavior.behaviors.IVersionable",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.relationfield.behavior.IRelatedItems",
                "plone.app.contenttypes.behaviors.collection.ICollection",
            ),
            model_source="""
            <model xmlns='http://namespaces.plone.org/supermodel/schema'>
                <schema>
                    <field name='text' type='zope.schema.Text'>
                        <title>Text</title>
                        <required>False</required>
                    </field>
                    <field name='file' type='plone.namedfile.field.NamedFile'>
                        <title>File</title>
                        <required>False</required>
                    </field>
                    <field name='date' type='zope.schema.Date'>
                        <title>Date</title>
                        <required>False</required>
                    </field>
                    <field name='files' type='zope.schema.List'>
                        <title>Date</title>
                        <required>False</required>
                        <value_type type='plone.namedfile.field.NamedFile'>
                            <title>Val</title>
                        </value_type>
                    </field>
                    <field name='choice' type='zope.schema.Choice'>
                        <title>Choice</title>
                        <required>False</required>
                        <vocabulary>Products.CMFDiffTool.testing.VOCABULARY</vocabulary>
                    </field>
                    <field name="choices" type="zope.schema.List">
                        <title>Choices</title>
                        <required>False</required>
                        <value_type type="zope.schema.Choice">
                            <vocabulary>Products.CMFDiffTool.testing.VOCABULARY</vocabulary>
                        </value_type>
                    </field>
                </schema>
            </model>
            """,
        )
        types_tool._setObject(TEST_CONTENT_TYPE_ID, fti)


PACKAGE_DX_FIXTURE = DXLayer()

CMFDiffToolDXLayer = FunctionalTesting(
    bases=(PACKAGE_DX_FIXTURE,), name="Products.CMFDiffTool.DX:functional"
)
