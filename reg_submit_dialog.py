# Created By: Virgil Dupras
# Created On: 2009-05-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtCore import Qt, QUrl, QCoreApplication
from PyQt4.QtGui import (QDialog, QMessageBox, QDesktopServices, QApplication, QVBoxLayout,
    QHBoxLayout, QLabel, QFormLayout, QLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy,
    QCheckBox)

from hscommon.plat import ISLINUX
from hscommon.reg import InvalidCodeError
from hscommon.trans import tr as trbase, trmsg
tr = lambda s: trbase(s, "RegSubmitDialog")

class RegSubmitDialog(QDialog):
    def __init__(self, parent, validate_func):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self._setupUi()
        self.validate_func = validate_func
        
        self.submitButton.clicked.connect(self.submitClicked)
        self.contributeButton.clicked.connect(self.contributeClicked)
        self.cancelButton.clicked.connect(self.reject)
    
    def _setupUi(self):
        self.setWindowTitle(tr("Enter your registration key"))
        # Workaround for bug at http://bugreports.qt.nokia.com/browse/QTBUG-8212
        if ISLINUX:
            self.resize(450, 210)
        else:
            self.resize(365, 146)
        self.verticalLayout = QVBoxLayout(self)
        self.promptLabel = QLabel(self)
        appname = str(QCoreApplication.instance().applicationName())
        prompt = trmsg("FairwareTypeKeyMsg")
        prompt = prompt.replace('$appname', appname)
        self.promptLabel.setText(prompt)
        self.promptLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.promptLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.promptLabel)
        self.formLayout = QFormLayout()
        self.formLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label2 = QLabel(self)
        self.label2.setText(tr("Registration key:"))
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label2)
        self.label3 = QLabel(self)
        self.label3.setText(tr("Registered e-mail:"))
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label3)
        self.codeEdit = QLineEdit(self)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.codeEdit)
        self.emailEdit = QLineEdit(self)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.emailEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.registerOSCheckBox = QCheckBox(self)
        self.registerOSCheckBox.setText(tr("Tell Hardcoded Software which operating system I'm using."))
        self.registerOSCheckBox.setChecked(True)
        self.verticalLayout.addWidget(self.registerOSCheckBox)
        self.label4 = QLabel(self)
        self.label4.setText(tr("(to have some contribution statistics based on OSes)"))
        self.verticalLayout.addWidget(self.label4)
        self.horizontalLayout = QHBoxLayout()
        self.contributeButton = QPushButton(self)
        self.contributeButton.setText(tr("Contribute"))
        self.contributeButton.setAutoDefault(False)
        self.horizontalLayout.addWidget(self.contributeButton)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setText(tr("Cancel"))
        self.cancelButton.setAutoDefault(False)
        self.horizontalLayout.addWidget(self.cancelButton)
        self.submitButton = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setText(tr("Submit"))
        self.submitButton.setAutoDefault(False)
        self.submitButton.setDefault(True)
        self.horizontalLayout.addWidget(self.submitButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
    
    #--- Events
    def contributeClicked(self):
        url = QUrl('http://open.hardcoded.net/contribute/')
        QDesktopServices.openUrl(url)
    
    def submitClicked(self):
        code = str(self.codeEdit.text())
        email = str(self.emailEdit.text())
        title = tr("Registration")
        try:
            self.validate_func(code, email)
            msg = tr("This code is valid. Thanks!")
            QMessageBox.information(self, title, msg)
            self.accept()
        except InvalidCodeError as e:
            msg = str(e)
            QMessageBox.warning(self, title, msg)
    

if __name__ == '__main__':
    app = QApplication([])
    validate = lambda *args: True
    dialog = RegSubmitDialog(None, validate)
    dialog.show()
    sys.exit(app.exec_())
