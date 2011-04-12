# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-25
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt

DATE_EDIT = 'date_edit'
DESCRIPTION_EDIT = 'description_edit'
PAYEE_EDIT = 'payee_edit'
ACCOUNT_EDIT = 'account_edit'

class Column(object):
    def __init__(self, attrname, title, defaultWidth, editor=None, alignment=Qt.AlignLeft,
            cantTruncate=False):
        self.index = None # Is set when the column list is read
        self.attrname = attrname
        self.title = title
        self.defaultWidth = defaultWidth
        self.editor = editor
        self.alignment = alignment
        # This is to indicate, during printing, that a column can't have its data truncated.
        self.cantTruncate = cantTruncate
    

class ColumnBearer(object):
    COLUMNS = []
    
    def __init__(self, headerView):
        self._headerView = headerView
        for index, col in enumerate(self.COLUMNS):
            col.index = index
        # A map attrname:column is useful sometimes, so we create it here
        self.ATTR2COLUMN = dict((col.attrname, col) for col in self.COLUMNS)
        self._headerView.setDefaultAlignment(Qt.AlignLeft)
    
    #--- Public
    def setColumnsWidth(self, widths):
        #`widths` can be None. If it is, then default widths are set.
        if not widths:
            widths = [column.defaultWidth for column in self.COLUMNS]
        for column, width in zip(self.COLUMNS, widths):
            if width == 0: # column was hidden before.
                width = column.defaultWidth
            self._headerView.resizeSection(column.index, width)
    
    def setColumnsOrder(self, columnIndexes):
        if not columnIndexes:
            return
        for destIndex, columnIndex in enumerate(columnIndexes):
            # moveSection takes 2 visual index arguments, so we have to get our visual index first
            visualIndex = self._headerView.visualIndex(columnIndex)
            self._headerView.moveSection(visualIndex, destIndex)
    
    def setHiddenColumns(self, hiddenColumns):
        for column in self.COLUMNS:
            isHidden = column.attrname in hiddenColumns
            self._headerView.setSectionHidden(column.index, isHidden)
    
    def visibleRowAttrs(self):
        """Returns a list of row attrs in visual order"""
        h = self._headerView
        visibleColumns = [column for column in self.COLUMNS if not h.isSectionHidden(column.index)]
        orderedColumns = sorted(visibleColumns, key=lambda col: h.visualIndex(col.index))
        return [column.attrname for column in orderedColumns]
    
