# Created By: Virgil Dupras
# Created On: 2011-02-01
# Copyright 2012 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.util import first

from PyQt4.QtGui import (QDesktopWidget, QSpacerItem, QSizePolicy, QPixmap, QIcon, QAction,
    QHBoxLayout)

def moveToScreenCenter(widget):
    frame = widget.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    widget.move(frame.topLeft())

def verticalSpacer(size=None):
    if size:
        return QSpacerItem(1, size, QSizePolicy.Fixed, QSizePolicy.Fixed)
    else:
        return QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

def horizontalSpacer(size=None):
    if size:
        return QSpacerItem(size, 1, QSizePolicy.Fixed, QSizePolicy.Fixed)
    else:
        return QSpacerItem(1, 1, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

def horizontalWrap(widgets):
    layout = QHBoxLayout()
    for widget in widgets:
        if widget is None:
            layout.addItem(horizontalSpacer())
        else:
            layout.addWidget(widget)
    return layout

def createActions(actions, target):
    # actions = [(name, shortcut, icon, desc, func)]
    for name, shortcut, icon, desc, func in actions:
        action = QAction(target)
        if icon:
            action.setIcon(QIcon(QPixmap(':/' + icon)))
        if shortcut:
            action.setShortcut(shortcut)
        action.setText(desc)
        action.triggered.connect(func)
        setattr(target, name, action)

def setAccelKeys(menu):
    actions = menu.actions()
    titles = [a.text() for a in actions]
    available_characters = {c.lower() for s in titles for c in s if c.isalpha()}
    for action in actions:
        text = action.text()
        c = first(c for c in text if c.lower() in available_characters)
        if c is None:
            continue
        i = text.index(c)
        newtext = text[:i] + '&' + text[i:]
        available_characters.remove(c.lower())
        action.setText(newtext)
