# Created By: Virgil Dupras
# Created On: 2009-05-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QCoreApplication
from PyQt4.QtGui import (QDialog, QDialogButtonBox, QPixmap, QSizePolicy, QHBoxLayout, QVBoxLayout,
    QLabel, QFont, QApplication)

class AboutBox(QDialog):
    def __init__(self, parent, app):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.MSWindowsFixedSizeDialogHint
        QDialog.__init__(self, parent, flags)
        self.app = app
        self._setupUi()
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.buttonClicked)
    
    def _setupUi(self):
        def tr(s):
            return QApplication.translate("AboutBox", s, None, QApplication.UnicodeUTF8)
        
        self.setWindowTitle("About {0}".format(QCoreApplication.instance().applicationName()))
        self.resize(400, 190)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self)
        self.logoLabel = QLabel(self)
        self.logoLabel.setPixmap(QPixmap(':/%s_big' % self.app.LOGO_NAME))
        self.horizontalLayout.addWidget(self.logoLabel)
        self.verticalLayout = QVBoxLayout()
        self.nameLabel = QLabel(self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.nameLabel.setFont(font)
        self.nameLabel.setText(QCoreApplication.instance().applicationName())
        self.verticalLayout.addWidget(self.nameLabel)
        self.versionLabel = QLabel(self)
        self.versionLabel.setText('Version {0}'.format(QCoreApplication.instance().applicationVersion()))
        self.verticalLayout.addWidget(self.versionLabel)
        self.label_3 = QLabel(self)
        self.verticalLayout.addWidget(self.label_3)
        self.label_3.setText(tr("Copyright Hardcoded Software 2010"))
        self.label = QLabel(self)
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.verticalLayout.addWidget(self.label)
        self.registeredEmailLabel = QLabel(self)
        self.registeredEmailLabel.setText(tr("UNREGISTERED"))
        self.verticalLayout.addWidget(self.registeredEmailLabel)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.registerButton = self.buttonBox.addButton("Register", QDialogButtonBox.ActionRole)
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
    
    #--- Events
    def buttonClicked(self, button):
        if button is self.registerButton:
            self.app.askForRegCode()
    

if __name__ == '__main__':
    import sys
    app = QApplication([])
    QCoreApplication.setOrganizationName('Hardcoded Software')
    QCoreApplication.setApplicationName('FooApp')
    QCoreApplication.setApplicationVersion('1.2.3')
    app.LOGO_NAME = ''
    dialog = AboutBox(None, app)
    dialog.show()
    sys.exit(app.exec_())
