# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from Products.CMFDiffTool.FieldDiff import FieldDiff
from six.moves import range


def chk_hashable(value):
    try:
        hash(value)
    except TypeError as e:
        value = repr(e) + ": " + repr(value)
    return value


class ListDiff(FieldDiff):
    """Text difference"""

    meta_type = 'List Diff'

    def _parseField(self, value, filename=None):
        """Parse a field value in preparation for diffing"""
        if type(value) is list or type(value) is tuple:
            values = []
            for v in value:
                values.append(chk_hashable(v))
            return values
        else:
            if type(value) is set:
                return list(value)
            else:
                return [chk_hashable(value)]


class RelationListDiff(FieldDiff):

    meta_type = 'Related List Diff'

    same_fmt = """<div class="%s"><a target="_blank" href="%s">%s</a></div>"""
    inlinediff_fmt = """<div class="%s">
        <div class="%s"><a target="_blank" href="%s">%s</a></div>
    </div>"""

    def _parseField(self, value, filename=None):
        """Take RelationValues and just return the target UID so we can compare"""

        if filename is None:
            # Since we only want to compare a single field, make a
            # one-item list out of it
            return ['/'.join(val.getPhysicalPath()) for val in value]
        else:
            return [
                self.filenameTitle(filename),
                ['/'.join(val.getPhysicalPath()) for val in value]
            ]

    def inline_diff(self):
        css_class = 'InlineDiff'
        inlinediff_fmt = self.inlinediff_fmt
        same_fmt = self.same_fmt
        r = []
        for tag, alo, ahi, blo, bhi in self.getLineDiffs():
            if tag == 'replace':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_title = obj.Title()
                    obj_url = obj.absolute_url()
                    r.append(inlinediff_fmt %
                             (css_class, "diff_sub", obj_url, obj_title))
                for i in range(blo, bhi):
                    obj = self.newValue[i]
                    obj_title = obj.Title()
                    obj_url = obj.absolute_url()
                    r.append(inlinediff_fmt %
                             (css_class, "diff_add", obj_url, obj_title))
            elif tag == 'delete':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_title = obj.Title()
                    obj_url = obj.absolute_url()
                    r.append(inlinediff_fmt %
                             (css_class, "diff_sub", obj_url, obj_title))
            elif tag == 'insert':
                for i in range(blo, bhi):
                    obj = self.newValue[i]
                    obj_title = obj.Title()
                    obj_url = obj.absolute_url()
                    r.append(inlinediff_fmt %
                             (css_class, "diff_add", obj_url, obj_title))
            elif tag == 'equal':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_title = obj.Title()
                    obj_url = obj.absolute_url()
                    r.append(same_fmt % (css_class, obj_url, obj_title))
            else:
                raise ValueError('unknown tag %s' % tag)
        return '\n'.join(r)

    def ndiff(self):
        """Return a textual diff"""
        r = []
        for tag, alo, ahi, blo, bhi in self.getLineDiffs():
            if tag == 'replace':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_url = obj.absolute_url()
                    r.append("- %s" % obj_url)
                for i in range(blo, bhi):
                    obj = self.newValue[i]
                    obj_url = obj.absolute_url()
                    r.append("+ %s" % obj_url)
            elif tag == 'delete':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_url = obj.absolute_url()
                    r.append("- %s" % obj_url)
            elif tag == 'insert':
                for i in range(blo, bhi):
                    obj = self.newValue[i]
                    obj_url = obj.absolute_url()
                    r.append("+ %s" % obj_url)
            elif tag == 'equal':
                for i in range(alo, ahi):
                    obj = self.oldValue[i]
                    obj_url = obj.absolute_url()
                    r.append("  %s" % obj_url)
            else:
                raise ValueError('unknown tag %r', tag)
        return '\n'.join(r)


InitializeClass(ListDiff)
InitializeClass(RelationListDiff)
