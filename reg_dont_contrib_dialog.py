# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-10-06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtCore import Qt, QUrl, QCoreApplication
from PyQt4.QtGui import (QDialog, QDesktopServices, QApplication, QVBoxLayout, QLabel,
    QPlainTextEdit, QDialogButtonBox, QFont)

from hscommon.trans import tr as trbase, trmsg
tr = lambda s: trbase(s, "RegDontContributeDialog")

class RegDontContributeDialog(QDialog):
    def __init__(self, parent):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self._setupUi()
        
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.buttonClicked)
    
    def _setupUi(self):
        self.setWindowTitle(tr("Don't contribute"))
        self.verticalLayout = QVBoxLayout(self)
        self.boldLabel = QLabel(tr("You indicated not wanting to (or not being able to) contribute."), self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.boldLabel.setFont(font)
        self.verticalLayout.addWidget(self.boldLabel)
        self.promptLabel = QLabel(self)
        prompt = trmsg("FairwareDontContributeReasonsMsg")
        self.promptLabel.setText(prompt)
        self.promptLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.promptLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.promptLabel)
        self.msgEdit = QPlainTextEdit(self)
        self.verticalLayout.addWidget(self.msgEdit)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.sendButton = self.buttonBox.addButton(tr("Send"), QDialogButtonBox.AcceptRole)
        self.verticalLayout.addWidget(self.buttonBox)
    
    #--- Events
    def buttonClicked(self, button):
        if button is self.sendButton:
            appname = QCoreApplication.instance().applicationName()
            text = self.msgEdit.toPlainText()
            subject = "I don't want to contribute to {0}".format(appname)
            url = QUrl("mailto:hsoft@hardcoded.net?SUBJECT={0}&BODY={1}".format(subject, text))
            QDesktopServices.openUrl(url)
            self.accept()
    

if __name__ == '__main__':
    app = QApplication([])
    dialog = RegDontContributeDialog(None)
    dialog.show()
    sys.exit(app.exec_())