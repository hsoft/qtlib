# Created By: Virgil Dupras
# Created On: 2009-05-03
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QSettings, QVariant, QRect

from hscommon.util import tryint
from hscommon.trans import trget

tr = trget('qtlib')

LANGNAMES = {
    'en': tr("English"),
    'fr': tr("French"),
    'de': tr("German"),
    'zh_CN': tr("Chinese (Simplified)"),
    'cs': tr("Czech"),
    'it': tr("Italian"),
    'hy': tr("Armenian"),
    'ru': tr("Russian"),
    'uk': tr("Ukrainian"),
}

def variant_to_py(v):
    value = None
    ok = False
    t = v.type()
    if t == QVariant.String:
        value = str(v.toString())
        ok = True # anyway
        # might be bool or int, try them
        if v == 'true':
            value = True
        elif value == 'false':
            value = False
        else:
            value = tryint(value, value)
    elif t == QVariant.Int:
        value, ok = v.toInt()
    elif t == QVariant.Bool:
        value, ok = v.toBool(), True
    elif t in (QVariant.List, QVariant.StringList):
        value, ok = list(map(variant_to_py, v.toList())), True
    elif t == QVariant.Map:
        value, ok = dict((str(key), variant_to_py(value)) for key, value in list(v.toMap().items())), True
    if not ok:
        raise TypeError("Can't convert {0} of type {1}".format(repr(v), v.type()))
    return value    

def py_to_variant(v):
    if isinstance(v, (set, tuple)): # QVariant doesn't automatically consider a set/tuple as a list for preferences
        v = list(v)
    if isinstance(v, list):
        return [py_to_variant(item) for item in v]
    return QVariant(v)

# About QRect conversion:
# I think Qt supports putting basic structures like QRect directly in QSettings, but I prefer not
# to rely on it and stay with generic structures.

class Preferences:
    def __init__(self):
        self.reset()
        self._settings = QSettings()
    
    def _load_values(self, settings, get):
        pass
    
    def get_rect(self, name, default=None):
        r = self.get_value(name, default)
        if r is not None:
            return QRect(*r)
        else:
            return None
    
    def get_value(self, name, default=None):
        if self._settings.contains(name):
            try:
                return variant_to_py(self._settings.value(name))
            except TypeError:
                return default
        else:
            return default
    
    def load(self):
        self.reset()
        self._load_values(self._settings)
    
    def reset(self):
        pass
    
    def _save_values(self, settings, set_):
        pass
    
    def save(self):
        self._save_values(self._settings)
        self._settings.sync()
    
    def set_rect(self, name, r):
        if isinstance(r, QRect):
            rectAsList = [r.x(), r.y(), r.width(), r.height()]
            self.set_value(name, rectAsList)
    
    def set_value(self, name, value):
        self._settings.setValue(name, py_to_variant(value))
    
    def saveGeometry(self, name, widget):
        # We save geometry under a 5-sized int array: first item is a flag for whether the widget
        # is maximized and the other 4 are (x, y, w, h).
        m = 1 if widget.isMaximized() else 0
        r = widget.geometry()
        rectAsList = [r.x(), r.y(), r.width(), r.height()]
        self.set_value(name, [m] + rectAsList)
    
    def restoreGeometry(self, name, widget):
        l = self.get_value(name)
        if l and len(l) == 5:
            m, x, y, w, h = l
            if m:
                widget.setWindowState(Qt.WindowMaximized)
            else:
                r = QRect(x, y, w, h)
                widget.setGeometry(r)
    
