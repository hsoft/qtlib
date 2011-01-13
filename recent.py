# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-12
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import pyqtSignal, QObject, QSettings
from PyQt4.QtGui import QAction

from hscommon.util import dedupe
from .preferences import variant_to_py

class Recent(QObject):
    def __init__(self, app, menu, prefName, maxItemCount=10):
        QObject.__init__(self)
        self._app = app
        self._menu = menu
        self._prefName = prefName
        self._maxItemCount = maxItemCount
        self._items = []
        self._loadFromPrefs()
        self._refreshMenu()
        
        self._app.willSavePrefs.connect(self._saveToPrefs)
    
    #--- Private
    def _loadFromPrefs(self):
        items = getattr(self._app.prefs, self._prefName)
        assert isinstance(items, list)
        self._items = items
    
    def _insertItem(self, item):
        self._items = dedupe([item] + self._items)[:self._maxItemCount]
    
    def _refreshMenu(self):
        menu = self._menu
        menu.clear()
        for item in self._items:
            action = QAction(item, menu)
            action.setData(item)
            action.triggered.connect(self.menuItemWasClicked)
            menu.addAction(action)
    
    def _saveToPrefs(self):
        setattr(self._app.prefs, self._prefName, self._items)
    
    #--- Public
    def insertItem(self, item):
        self._insertItem(str(item))
        self._refreshMenu()
    
    #--- Event Handlers
    def menuItemWasClicked(self):
        action = self.sender()
        if action is not None:
            item = action.data().toString()
            self.mustOpenItem.emit(item)
            self._refreshMenu()
    
    #--- Signals
    mustOpenItem = pyqtSignal(str)

    