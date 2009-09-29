# Created By: Virgil Dupras
# Created On: 2009-05-23
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from __future__ import unicode_literals

from PyQt4.QtCore import Qt, QUrl, QCoreApplication
from PyQt4.QtGui import QDialog, QDesktopServices

from ui.error_report_dialog_ui import Ui_ErrorReportDialog

class ErrorReportDialog(QDialog, Ui_ErrorReportDialog):
    def __init__(self, parent, error):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)
        name = QCoreApplication.applicationName()
        version = QCoreApplication.applicationVersion()
        errorText = "Application Name: {0}\nVersion: {1}\n\n{2}".format(name, version, error)
        self.errorTextEdit.setPlainText(errorText)
    
    def accept(self):
        text = self.errorTextEdit.toPlainText()
        url = QUrl("mailto:support@hardcoded.net?SUBJECT=Error Report&BODY=%s" % text)
        QDesktopServices.openUrl(url)
        QDialog.accept(self)
    
