# Created By: Virgil Dupras
# Created On: 2011-09-06
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QAbstractListModel
from PyQt4.QtGui import QItemSelection

class SelectableList(QAbstractListModel):
    def __init__(self, model, view):
        QAbstractListModel.__init__(self)
        self.model = model
        self.model.view = self
        self.view = view
        self.view.setModel(self)
    
    #--- Override
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.model[index.row()]
        return None
    
    def rowCount(self, index):
        if index.isValid():
            return 0
        return len(self.model)
    
    #--- Virtual
    def _updateSelection(self):
        raise NotImplementedError()
    
    def _restoreSelection(self):
        raise NotImplementedError()
    
    #--- model --> view
    def refresh(self):
        self.reset()
        self._restoreSelection()
    
    def update_selection(self):
        self._restoreSelection()

class ComboboxModel(SelectableList):
    def __init__(self, model, view):
        SelectableList.__init__(self, model, view)
        self.view.currentIndexChanged[int].connect(self.selectionChanged)
    
    #--- Override
    def _updateSelection(self):
        index = self.view.currentIndex()
        if index != self.model.selected_index:
            self.model.select(index)
    
    def _restoreSelection(self):
        self.view.setCurrentIndex(self.model.selected_index)
    
    #--- Events
    def selectionChanged(self, index):
        self._updateSelection()

class ListviewModel(SelectableList):
    def __init__(self, model, view):
        SelectableList.__init__(self, model, view)
        self.view.selectionModel().selectionChanged[(QItemSelection, QItemSelection)].connect(
            self.selectionChanged)
    
    #--- Override
    def _updateSelection(self):
        newIndexes = [modelIndex.row() for modelIndex in self.view.selectionModel().selectedRows()]
        if newIndexes != self.model.selected_indexes:
            self.model.select(newIndexes)
    
    # XXX Implement _restoreSelection() for dupeGuru (the only user so far of ListviewModel)

    #--- Events
    def selectionChanged(self, index):
        self._updateSelection()
    
