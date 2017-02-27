# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.dexterity.browser.edit import DefaultEditForm
from Products.CMFDiffTool.choicediff import ChoiceDiff
from Products.CMFDiffTool.CMFDTHtmlDiff import CMFDTHtmlDiff
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.ListDiff import RelationListDiff
from Products.CMFDiffTool.namedfile import FILE_FIELD_TYPES
from Products.CMFDiffTool.namedfile import NamedFileBinaryDiff
from Products.CMFDiffTool.namedfile import NamedFileListDiff
from Products.CMFDiffTool.TextDiff import AsTextDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from z3c.relationfield.schema import RelationList
from zope.globalrequest import getRequest
from zope.schema import Bool
from zope.schema import Bytes
from zope.schema import Choice
from zope.schema import Container
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import Iterable
from zope.schema import Text
from zope.schema import Time


# TODO: Perhaps this can be replaced with some kind of Zope 3 style
# adaptation, in order to provide better extensibility.
FIELDS_AND_DIFF_TYPES_RELATION = [
    (FILE_FIELD_TYPES, NamedFileBinaryDiff),
    ((RelationList,), RelationListDiff),
    ((Iterable, Container), ListDiff),
    ((Date, Datetime, Time), AsTextDiff),
    ((Bool, ), AsTextDiff),
    ((Choice, ), ChoiceDiff),
    ((Text, Bytes), TextDiff),
    ((RichText, ), CMFDTHtmlDiff),
]

"""
Relates field types (`zope.schema.Field` subclasses) and "diff types"
(`Products.CMFEditions.BaseDiff.BaseDiff` subclasses).

To find the best diff type for a field type this list will be searched until
a match is found.
If a match is not found then `FALL_BACK_DIFF_TYPE` is used.
"""

FALL_BACK_DIFF_TYPE = FieldDiff

# TODO: Perhaps this is not the best approach. Instead we should write a diff
# type which can handle lists of any kind of elements, providing extensibility
# mechanisms if we want to specialize the handling of certain value types.
# (rafaelbco)
VALUE_TYPES_AND_DIFF_TYPES_RELATION = [
    (FILE_FIELD_TYPES, NamedFileListDiff),
]

"""
When a field is detected to be a list-like field we use this list in the same
fashion as `FIELDS_AND_DIFF_TYPES_RELATION` to try to find the best "diff type
" according to the "value type" of the field, i.e the type of the elements in
the list. If a match is not found then a fall back is used.
"""

# TODO: provide an easier way to exclude fields.
EXCLUDED_FIELDS = ('modification_date', 'IVersionable.changeNote')
"""Names of fields not to compare."""


class DexterityCompoundDiff(object):
    """Same as `Products.CMFDiffTool.ATCompoundDiff.ATCompoundDiff` but for
    Dexterity.
    """

    meta_type = 'Compound Diff for Dexterity types'

    def __init__(self, obj1, obj2, field, id1=None, id2=None):
        self.id1 = id1 or obj1.getId()
        self.id2 = id2 or obj2.getId()
        self.obj1 = obj1
        self._diffs = self._diff(obj1, obj2)

    def __getitem__(self, index):
        return self._diffs[index]

    def __len__(self):
        return len(self._diffs)

    def __iter__(self):
        return iter(self._diffs)

    def _diff(self, obj1, obj2):
        """
        Compute the differences between 2 objects.

        Return: a sequence of `IDifference` objects.
        """

        diffs = []
        for field, field_name in self._compute_fields_order(obj1):
            if field_name not in EXCLUDED_FIELDS:
                schema_name = '.' in field_name and \
                    field_name.split('.')[0] or 'default'
                diffs.append(self._diff_field(obj1, obj2, field, schema_name))

        return diffs

    def _diff_field(self, obj1, obj2, field, schema_name):
        """
        Compute the differences between 2 objects in respect to the given
        field (`zope.schema.Field` instance).

        Return: an `IDifference` object.
        """
        diff_type = self._get_diff_type(field)
        return diff_type(
            obj1,
            obj2,
            field.getName(),
            id1=self.id1,
            id2=self.id2,
            field_name=field.getName(),
            field_label=field.title,
            schemata=schema_name
        )

    def _get_diff_type(self, field):
        """
        Return a subclass of `Products.CMFEditions.BaseDiff.BaseDiff` suitable
        for the given `zope.schema.Field` instance.
        """
        diff_type = self._compute_diff_type(
            field, FIELDS_AND_DIFF_TYPES_RELATION)

        if diff_type is ListDiff:
            return (
                self._compute_diff_type(
                    field.value_type, VALUE_TYPES_AND_DIFF_TYPES_RELATION) or
                diff_type
            )

        return diff_type or FALL_BACK_DIFF_TYPE

    def _compute_diff_type(self, field, relation):
        """
        Return the best "diff type" (subclass of
        `Products.CMFEditions.BaseDiff.BaseDiff`) suitable for the given
        `zope.schema.Field` instance according to `relation`. The `relation`
        is searched until a match is found. Return `None` otherwise.

        Parameters:
        field -- `zope.schema.Field` instance.
        relation -- Sequence of tuples (field_types, diff_type) where
            field_types is a tuple of `zope.schema.Field` subclasses
            and diff_type is a `Products.CMFEditions.BaseDiff.BaseDiff`
            subclass.
        """

        for (field_types, diff_type) in relation:
            if isinstance(field, field_types):
                return diff_type

        return None

    def _compute_fields_order(self, obj):
        """
        Given a content, compute the field ordering the way the edit form does.

        Return: a list of tuples (field, field name) in order.
        """
        form = DefaultEditForm(obj, getRequest())
        form.portal_type = obj.portal_type
        form.updateFields()
        all_fields = list()
        all_fields += [(form.fields[name].field, name) for name in form.fields]
        if form.groups:
            for group in form.groups:
                all_fields += [(group.fields[name].field, name) for name in group.fields]

        return all_fields
