'''
Created on Oct 9, 2014

@author: Emre
'''

import shiboken
import os
from maya import OpenMayaUI
from PySide import QtGui, QtCore
import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO


def wrapinstance(ptr, base=None):
    """Utility to convert a pointer to a Qt class instance.
    @param ptr: Pointer to QObject in memory
    @param base: (Optional) Base class to wrap with (Defaults to QObject,
                 which should handle anything)
    @type ptr: long or Swig instance
    @type base: QtGui.QWidget
    @return: QWidget or subclass instance
    """
    if ptr is None:
        return None
    ptr = long(ptr)
    if base is None:
        qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
        metaObj = qObj.metaObject()
        cls = metaObj.className()
        superCls = metaObj.superClass().className()
        if hasattr(QtGui, cls):
            base = getattr(QtGui, cls)
        elif hasattr(QtGui, superCls):
            base = getattr(QtGui, superCls)
        else:
            base = QtGui.QWidget
    return shiboken.wrapInstance(long(ptr), base)
# END def wrapinstance


def load_ui_type(ui_file):
    """Pyside lacks the "loadUiType" command, so we have to convert the ui
    file to py code in-memory first and then execute it in a special frame to
    retrieve the form_class.
    @param ui_file: the ui file
    @type ui_file: String
    @return: the classes
    """
    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = dict()
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        # Fetch the base_class and form class based on their type in the
        # xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtGui.%s' % widget_class)
    # END with open(ui_file, 'r') as f
    return form_class, base_class
# END def load_ui_type


def get_maya_window():
    """Get the maya main window as a QMainWindow instance.
    @return: the maya main window
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapinstance(long(ptr), QtGui.QWidget)
# END def get_maya_window
