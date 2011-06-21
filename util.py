# Created By: Virgil Dupras
# Created On: 2011-02-01
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtGui import QDesktopWidget, QSpacerItem, QSizePolicy, QPixmap, QIcon, QAction

def moveToScreenCenter(widget):
    frame = widget.frameGeometry()
    frame.moveCenter(QDesktopWidget().availableGeometry().center())
    widget.move(frame.topLeft())

def verticalSpacer():
    return QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

def horizontalSpacer():
    return QSpacerItem(1, 1, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

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