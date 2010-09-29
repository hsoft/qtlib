# Created By: Virgil Dupras
# Created On: 2009-05-10
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import SIGNAL, Qt, QUrl, QCoreApplication
from PyQt4.QtGui import QDialog, QDesktopServices

from .ui.reg_demo_dialog_ui import Ui_RegDemoDialog

class RegDemoDialog(QDialog, Ui_RegDemoDialog):
    def __init__(self, parent, reg):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self.reg = reg
        self._setupUi()
        
        self.connect(self.enterCodeButton, SIGNAL('clicked()'), self.enterCodeClicked)
        self.connect(self.contributeButton, SIGNAL('clicked()'), self.contributeClicked)
    
    def _setupUi(self):
        self.setupUi(self)
        # Stuff that can't be setup in the Designer
        appname = QCoreApplication.instance().applicationName()
        unpaid_hours = "%0.1f" % self.reg.app.unpaid_hours
        title = str(self.windowTitle())
        title = title.replace('$appname', appname)
        self.setWindowTitle(title)
        desc = str(self.descLabel.text())
        desc = desc.replace('$appname', appname)
        self.descLabel.setText(desc)
        unpaid = str(self.unpaidHoursLabel.text())
        unpaid = unpaid.replace('$unpaid', unpaid_hours)
        self.unpaidHoursLabel.setText(unpaid)
    
    #--- Events
    def enterCodeClicked(self):
        if self.reg.ask_for_code():
            self.accept()
    
    def contributeClicked(self):
        url = QUrl('http://open.hardcoded.net/contribute/')
        QDesktopServices.openUrl(url)
    
