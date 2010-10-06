# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-10-06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import (QDialog, QDesktopServices, QApplication, QVBoxLayout, QLabel,
    QPlainTextEdit, QDialogButtonBox)

class RegDontContributeDialog(QDialog):
    def __init__(self, parent):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self._setupUi()
        
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.buttonClicked)
    
    def _setupUi(self):
        def tr(s):
            return QApplication.translate("RegDontContributeDialog", s, None, QApplication.UnicodeUTF8)
        
        self.setWindowTitle(tr("Don't contribute"))
        self.verticalLayout = QVBoxLayout(self)
        self.promptLabel = QLabel(self)
        prompt = "You won't or you can't contribute? You must have your reasons. I'd like to know "\
            "about them. You don't have enough money? My hours don't deserve to be compensated? "\
            "Please, tell me. I promise you right here right now that anything reasonable will get "\
            "you a registration key."
        self.promptLabel.setText(prompt)
        self.promptLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.promptLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.promptLabel)
        self.msgEdit = QPlainTextEdit(self)
        self.verticalLayout.addWidget(self.msgEdit)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.sendButton = self.buttonBox.addButton("Send", QDialogButtonBox.AcceptRole)
        self.verticalLayout.addWidget(self.buttonBox)
    
    #--- Events
    def buttonClicked(self, button):
        if button is self.sendButton:
            text = self.msgEdit.toPlainText()
            url = QUrl("mailto:hsoft@hardcoded.net?SUBJECT=I don't want to contribute&BODY=%s" % text)
            QDesktopServices.openUrl(url)
            self.accept()
    

if __name__ == '__main__':
    app = QApplication([])
    dialog = RegDontContributeDialog(None)
    dialog.show()
    sys.exit(app.exec_())