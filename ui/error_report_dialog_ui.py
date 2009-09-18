# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtlib/ui/error_report_dialog.ui'
#
# Created: Fri Sep 18 16:39:28 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ErrorReportDialog(object):
    def setupUi(self, ErrorReportDialog):
        ErrorReportDialog.setObjectName("ErrorReportDialog")
        ErrorReportDialog.resize(553, 349)
        self.verticalLayout = QtGui.QVBoxLayout(ErrorReportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ErrorReportDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.errorTextEdit = QtGui.QPlainTextEdit(ErrorReportDialog)
        self.errorTextEdit.setReadOnly(True)
        self.errorTextEdit.setObjectName("errorTextEdit")
        self.verticalLayout.addWidget(self.errorTextEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dontSendButton = QtGui.QPushButton(ErrorReportDialog)
        self.dontSendButton.setMinimumSize(QtCore.QSize(110, 0))
        self.dontSendButton.setObjectName("dontSendButton")
        self.horizontalLayout.addWidget(self.dontSendButton)
        self.sendButton = QtGui.QPushButton(ErrorReportDialog)
        self.sendButton.setMinimumSize(QtCore.QSize(110, 0))
        self.sendButton.setDefault(True)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ErrorReportDialog)
        QtCore.QObject.connect(self.sendButton, QtCore.SIGNAL("clicked()"), ErrorReportDialog.accept)
        QtCore.QObject.connect(self.dontSendButton, QtCore.SIGNAL("clicked()"), ErrorReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ErrorReportDialog)

    def retranslateUi(self, ErrorReportDialog):
        ErrorReportDialog.setWindowTitle(QtGui.QApplication.translate("ErrorReportDialog", "Error Report", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ErrorReportDialog", "Something went wrong. Would you like to send the error report to Hardcoded Software?", None, QtGui.QApplication.UnicodeUTF8))
        self.dontSendButton.setText(QtGui.QApplication.translate("ErrorReportDialog", "Don\'t Send", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("ErrorReportDialog", "Send", None, QtGui.QApplication.UnicodeUTF8))

