# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-10-16
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import SIGNAL, QTimer, QObject

class Application(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__launchTimer = QTimer()
        self.connect(self.__launchTimer, SIGNAL('timeout()'), self.__launchTimerTimedOut)
        self.__launchTimer.start(0)
    
    def __launchTimerTimedOut(self):
        self.__launchTimer.stop()
        del self.__launchTimer
        self.emit(SIGNAL('applicationFinishedLaunching()'))
    