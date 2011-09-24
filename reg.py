# Created By: Virgil Dupras
# Created On: 2009-05-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtGui import QDialog

from .reg_submit_dialog import RegSubmitDialog
from .reg_demo_dialog import RegDemoDialog

class Registration:
    def __init__(self, app):
        self.app = app
    
    def ask_for_code(self):
        dialog = RegSubmitDialog(None, self.app.validate_code)
        result = dialog.exec_()
        code = str(dialog.codeEdit.text())
        email = str(dialog.emailEdit.text())
        if result == QDialog.Accepted:
            self.app.set_registration(code, email)
            if dialog.registerOSCheckBox.isChecked():
                self.app.register_os()
            self.app.write_registration_to_defaults()
            return True
        return False
    
    def show_nag(self):
        dialog = RegDemoDialog(None, self)
        dialog.exec_()
    
