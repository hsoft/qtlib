# Created By: Virgil Dupras
# Created On: 2009-05-10
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtCore import SIGNAL, Qt, QUrl, QCoreApplication, QSize
from PyQt4.QtGui import (QDialog, QDesktopServices, QApplication, QVBoxLayout, QHBoxLayout, QLabel,
    QFont, QSpacerItem, QSizePolicy, QPushButton, QCheckBox)

class RegDemoDialog(QDialog):
    def __init__(self, parent, reg):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self.reg = reg
        self._setupUi()
        
        self.connect(self.enterCodeButton, SIGNAL('clicked()'), self.enterCodeClicked)
        self.connect(self.contributeButton, SIGNAL('clicked()'), self.contributeClicked)
        self.tryButton.clicked.connect(self.accept)
    
    def _setupUi(self):
        def tr(s):
            return QApplication.translate("RegDemoDialog", s, None, QApplication.UnicodeUTF8)
        
        appname = QCoreApplication.instance().applicationName()
        title = tr("$appname is Fairware")
        title = title.replace('$appname', appname)
        self.setWindowTitle(title)
        # Workaround for bug at http://bugreports.qt.nokia.com/browse/QTBUG-8212
        dlg_height = 350 if sys.platform == 'linux2' else 270
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
        desc = tr("""$appname is Fairware, which means "open source software developed with expectation of fair contributions from users". Hours invested in this software have been logged with the expectation that users will be fair enough to compensate them. The \"Unpaid hours\" figure you see below is the hours that have yet to be compensated for this project.

If you like this application, please make a contribution that you consider fair. Thanks!

This dialog doesn't show when there are no unpaid hours or when you have a valid contribution key.""")
        desc = desc.replace('$appname', appname)
        self.descLabel.setText(desc)
        self.descLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.descLabel)
        self.unpaidHoursLabel = QLabel(self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.unpaidHoursLabel.setFont(font)
        unpaid_hours = "%0.1f" % self.reg.app.unpaid_hours
        unpaid = tr("Unpaid hours: $unpaid")
        unpaid = unpaid.replace('$unpaid', unpaid_hours)
        self.unpaidHoursLabel.setText(unpaid)
        self.verticalLayout.addWidget(self.unpaidHoursLabel)
        self.dontContributeBox = QCheckBox(self)
        self.dontContributeBox.setText("I don't want to contribute, stop bugging me")
        self.verticalLayout.addWidget(self.dontContributeBox)
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
        url = QUrl('http://open.hardcoded.net/contribute/')
        QDesktopServices.openUrl(url)
    

if __name__ == '__main__':
    app = QApplication([])
    app.unpaid_hours = 42.4
    class FakeReg:
        app = app
    dialog = RegDemoDialog(None, FakeReg())
    dialog.show()
    sys.exit(app.exec_())