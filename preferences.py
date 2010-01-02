# Created By: Virgil Dupras
# Created On: 2009-05-03
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import QSettings, QVariant

from hsutil.misc import tryint

def variant_to_py(v):
    value = None
    ok = False
    t = v.type()
    if t == QVariant.String:
        value = unicode(v.toString())
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
        value, ok = map(variant_to_py, v.toList()), True
    elif t == QVariant.Map:
        value, ok = dict((unicode(key), variant_to_py(value)) for key, value in v.toMap().items()), True
    if not ok:
        raise TypeError(u"Can't convert {0} of type {1}".format(repr(v), v.type()))
    return value    

def py_to_variant(v):
    if isinstance(v, set): # QVariant doesn't automatically consider a set as a list for preferences
        return QVariant(map(py_to_variant, v))
    return QVariant(v)

class Preferences(object):
    def __init__(self):
        self.reset()
        self._settings = QSettings()
    
    def _load_values(self, settings, get):
        pass
    
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
        self._load_values(self._settings, self.get_value)
    
    def reset(self):
        pass
    
    def _save_values(self, settings, set_):
        pass
    
    def save(self):
        self._save_values(self._settings, self.set_value)
        self._settings.sync()
    
    def set_value(self, name, value):
        self._settings.setValue(name, py_to_variant(value))
    
