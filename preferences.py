# Created By: Virgil Dupras
# Created On: 2009-05-03
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
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
    if not ok:
        raise TypeError(u"Can't convert {0} of type {1}".format(repr(v), v.type()))
    return value    

def py_to_variant(v):
    if isinstance(v, (list, tuple)):
        return QVariant(map(py_to_variant, v))
    return QVariant(v)

class Preferences(object):
    def __init__(self):
        self.reset()
    
    def _load_values(self, settings, get):
        pass
    
    def load(self):
        self.reset()
        settings = QSettings()
        def get(name, default):
            if settings.contains(name):
                return variant_to_py(settings.value(name))
            else:
                return default
        # self.registration_code = get('RegistrationCode', self.registration_code)
        # self.registration_email = get('RegistrationEmail', self.registration_email)
        self._load_values(settings, get)
    
    def reset(self):
        pass
    
    def _save_values(self, settings, set_):
        pass
    
    def save(self):
        settings = QSettings()
        def set_(name, value):
            settings.setValue(name, py_to_variant(value))
        
        # set_('RegistrationCode', self.registration_code)
        # set_('RegistrationEmail', self.registration_email)
        self._save_values(settings, set_)
    
