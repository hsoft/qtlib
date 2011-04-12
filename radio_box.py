# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-06-02
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget, QHBoxLayout, QRadioButton

class RadioBox(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self._buttons = []
        self._labels = []
        self._selected_index = 0
        self._layout = QHBoxLayout(self)
    
    #--- Private
    def _update_buttons(self):
        to_remove = self._buttons[len(self._labels):]
        for button in to_remove:
            self._layout.removeWidget(button)
            button.setParent(None)
        del self._buttons[len(self._labels):]
        to_add = self._labels[len(self._buttons):]
        for _ in to_add:
            button = QRadioButton(self)
            self._buttons.append(button)
            self._layout.addWidget(button)
            button.toggled.connect(self.buttonToggled)
        if not self._buttons:
            return
        for button, label in zip(self._buttons, self._labels):
            button.setText(label)
        self._update_selection()
    
    def _update_selection(self):
        self._selected_index = max(0, min(self._selected_index, len(self._buttons)-1))
        selected = self._buttons[self._selected_index]
        selected.setChecked(True)
    
    #--- Event Handlers
    def buttonToggled(self):
        for i, button in enumerate(self._buttons):
            if button.isChecked():
                self._selected_index = i
                self.itemSelected.emit(i)
                break
    
    #--- Signals
    itemSelected = pyqtSignal(int)
    
    #--- Properties
    @property
    def buttons(self):
        return self._buttons[:]
    
    @property
    def items(self):
        return self._labels[:]
    
    @items.setter
    def items(self, value):
        self._labels = value
        self._update_buttons()
    
    @property
    def selected_index(self):
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value
        self._update_selection()
    
