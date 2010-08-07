# Created By: Virgil Dupras
# Created On: 2009-05-09
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license



from PyQt4.QtCore import Qt, QCoreApplication
from PyQt4.QtGui import QDialog, QDialogButtonBox, QPixmap

from .ui.about_box_ui import Ui_AboutBox

class AboutBox(QDialog, Ui_AboutBox):
    def __init__(self, parent, app):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.MSWindowsFixedSizeDialogHint
        QDialog.__init__(self, parent, flags)
        self.app = app
        self._setupUi()
        
        self.buttonBox.clicked.connect(self.buttonClicked)
    
    def _setupUi(self):
        self.setupUi(self)
        # Stuff that can't be done in the Designer
        self.setWindowTitle("About {0}".format(QCoreApplication.instance().applicationName()))
        self.nameLabel.setText(QCoreApplication.instance().applicationName())
        self.versionLabel.setText('Version {0}'.format(QCoreApplication.instance().applicationVersion()))
        self.logoLabel.setPixmap(QPixmap(':/%s_big' % self.app.LOGO_NAME))
        self.registerButton = self.buttonBox.addButton("Register", QDialogButtonBox.ActionRole)
    
    #--- Events
    def buttonClicked(self, button):
        if button is self.registerButton:
            self.app.askForRegCode()
    
