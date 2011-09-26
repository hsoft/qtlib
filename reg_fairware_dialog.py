# Created By: Virgil Dupras
# Created On: 2009-05-10
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtCore import Qt, QCoreApplication, QSize
from PyQt4.QtGui import (QDialog, QApplication, QVBoxLayout, QHBoxLayout, QLabel,
    QFont, QSpacerItem, QSizePolicy, QPushButton)

from hscommon.plat import ISLINUX
from hscommon.trans import tr as trbase
tr = lambda s: trbase(s, "RegDemoDialog")

class RegFairwareDialog(QDialog):
    def __init__(self, parent, reg, prompt):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self.reg = reg
        self._setupUi()
        self.descLabel.setText(prompt)
        
        self.enterCodeButton.clicked.connect(self.enterCodeClicked)
        self.contributeButton.clicked.connect(self.contributeClicked)
        self.tryButton.clicked.connect(self.accept)
        self.moreInfoButton.clicked.connect(self.moreInfoClicked)
    
    def _setupUi(self):
        appname = QCoreApplication.instance().applicationName()
        title = tr("$appname is Fairware")
        title = title.replace('$appname', appname)
        self.setWindowTitle(title)
        # Workaround for bug at http://bugreports.qt.nokia.com/browse/QTBUG-8212
        dlg_height = 430 if ISLINUX else 290
        self.resize(397, dlg_height)
        self.verticalLayout = QVBoxLayout(self)
        self.titleLabel = QLabel(self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setText(tr("Please contribute"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.descLabel = QLabel(self)        
        self.descLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.descLabel)
        self.unpaidHLayout = QHBoxLayout()
        self.unpaidHoursLabel = QLabel(self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.unpaidHoursLabel.setFont(font)
        unpaid_hours = "%0.1f" % self.reg.app.unpaid_hours
        unpaid = tr("Unpaid hours: $unpaid")
        unpaid = unpaid.replace('$unpaid', unpaid_hours)
        self.unpaidHoursLabel.setText(unpaid)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.unpaidHoursLabel.setSizePolicy(sizePolicy)
        self.unpaidHLayout.addWidget(self.unpaidHoursLabel)
        self.moreInfoButton = QPushButton(tr("More Info"), self)
        self.unpaidHLayout.addWidget(self.moreInfoButton)
        self.verticalLayout.addLayout(self.unpaidHLayout)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QHBoxLayout()
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.tryButton = QPushButton(self)
        self.tryButton.setText(tr("Continue"))
        self.tryButton.setMinimumSize(QSize(110, 0))
        self.horizontalLayout.addWidget(self.tryButton)
        self.enterCodeButton = QPushButton(self)
        self.enterCodeButton.setText(tr("Enter Key"))
        self.enterCodeButton.setMinimumSize(QSize(110, 0))
        self.horizontalLayout.addWidget(self.enterCodeButton)
        self.contributeButton = QPushButton(self)
        self.contributeButton.setText(tr("Contribute"))
        self.contributeButton.setMinimumSize(QSize(110, 0))
        self.horizontalLayout.addWidget(self.contributeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
    
    #--- Events
    def enterCodeClicked(self):
        if self.reg.ask_for_code():
            self.accept()
    
    def contributeClicked(self):
        self.reg.app.contribute()
    
    def moreInfoClicked(self):
        self.reg.app.about_fairware()
    

if __name__ == '__main__':
    app = QApplication([])
    app.unpaid_hours = 42.4
    class FakeReg:
        app = app
    dialog = RegFairwareDialog(None, FakeReg(), "foo bar baz")
    dialog.show()
    sys.exit(app.exec_())
