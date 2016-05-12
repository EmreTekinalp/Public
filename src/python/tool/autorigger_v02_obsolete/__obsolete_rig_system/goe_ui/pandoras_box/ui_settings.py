'''
@author:  etekinalp
@date:    Oct 9, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates and setups the rig settings ui
'''


import os

from maya import cmds
from PySide import QtGui, QtCore

from goe_functions import data
from goe_ui.pandoras_box.contents import utils

reload(data)

path = os.path.join(os.path.dirname(__file__), 'ui', 'settings.ui')
assert os.path.exists(path), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(path)


class SettingsUI(base_class, form_class):
    """ This class creates the SettingsUI to define setting attributes. """
    def __init__(self,
                 parent=None,
                 button='Create',
                 lock=False,
                 mirror=False):
        """ Initialize the class and subclass and setup Settings UI
        @type  parent: class instance (self)
        @param parent: specify the class instance which is the parent

        @type  button: string
        @param button: specify the button name, by default it is Create

        @type  lock: bool
        @param lock: define if lock_ui method should be called or not

        @type  mirror: bool
        @param mirror: define if lock_mirror method should be called or not
        """
        super(SettingsUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600, 300, 300, 500)
        self.setWindowModality(QtCore.Qt.NonModal)
        self.create_btn.setText(button)

        #--- args
        self.parent = parent
        self.data = dict()
        self.lock = lock
        self.mirror = mirror

        #--- methods
        self.__create()
    #END __init__()

    def add_type_data(self):
        """ Get the data and add the items to the moduleType combobox """
        d = data.load_cmds_data()
        self.type_cb.addItems(d[0])
    #END add_type_data()

    def add_data(self):
        """ Fill attributes and values when first called this UI """
        d = data.load_cmds_data()
        for i in d[1]:
            for k in i.items():
                if self.type_cb.currentText() == k[0]:
                    #--- clear the rows
                    self.main_tw.clear()
                    self.main_tw.setRowCount(len(k[1]))
                    for num, j in enumerate(k[1]):
                        #--- add the keys(verticalHeader) and values(rowItems)
                        keys = j.keys()[0]
                        value = j.values()[0]
                        item = QtGui.QTableWidgetItem(keys)
                        self.main_tw.setVerticalHeaderItem(num, item)

                        #--- check the widgets
                        if value['widget'] == 'combobox':
                            cb = ComboBox(self, value['value'])
                            itemindex = cb.findText(str(value['default']))
                            cb.setCurrentIndex(itemindex)
                            self.main_tw.setCellWidget(num, 0, cb)
                        elif value['widget'] == 'lineEdit':
                            led = LineEdit(self, value['default'])
                            self.main_tw.setCellWidget(num, 0, led)
                        elif value['widget'] == 'int':
                            led = IntLineEdit(self, value['default'])
                            self.main_tw.setCellWidget(num, 0, led)
                        elif value['widget'] == 'double':
                            led = DoubleLineEdit(self, value['default'])
                            self.main_tw.setCellWidget(num, 0, led)
        #--- check if modulename has value, otherwise disable all items
        self.check_modulename()
        self.check_completer()
        for row in range(self.main_tw.rowCount()):
            item = self.main_tw.cellWidget(row, 0)
            key = self.main_tw.verticalHeaderItem(row).text()
            if (key == 'moduleName'):
                item.editingFinished.connect(self.check_modulename)
            if (key == 'side'):
                item.currentIndexChanged.connect(self.check_side)
            if (key == 'parentFirst' or key == 'parentLast'):
                item.editingFinished.connect(self.check_completer)
    #END add_data()

    def get_data(self):
        """ Check the values of the tabWidget and add them to a dictionary """
        self.data['moduleType'] = self.type_cb.currentText()
        for row in range(self.main_tw.rowCount()):
            #--- setup keys and items from cellwidgets
            item = self.main_tw.cellWidget(row, 0)
            typ = str(type(item))
            typ = typ.split('.')[-1].split("'>")[0]
            key = self.main_tw.verticalHeaderItem(row).text()
            if key == 'moduleName':
                #--- check if moduleName has value, otherwise show Dialog
                if not item.text():
                    cmds.confirmDialog(title='Specify Asset',
                                       message="Please specify moduleName!",
                                       button=['Ok'],
                                       defaultButton='Ok',
                                       dismissString='Ok')
                    return
            #--- check the widgets, get the values and add to data dictionary
            if typ == 'ComboBox':
                value = item.currentText()
                key = self.main_tw.verticalHeaderItem(row).text()
                if value == 'True':
                    value = True
                elif value == 'False':
                    value = False
                self.data[key] = value
            if typ == 'LineEdit':
                value = str(item.text())
                key = self.main_tw.verticalHeaderItem(row).text()
                self.data[key] = value
            if typ == 'IntLineEdit':
                value = int(item.text())
                key = self.main_tw.verticalHeaderItem(row).text()
                self.data[key] = value
            if typ == 'DoubleLineEdit':
                value = float(item.text())
                key = self.main_tw.verticalHeaderItem(row).text()
                self.data[key] = value
        #--- take care of the proper side and mirrorside
        if self.data['side'] == 'L':
            self.data['mirrorside'] = 'R'
        elif self.data['side'] == 'R':
            self.data['mirrorside'] = 'L'

        #--- close the UI and return its data
        self.close()
        return self.data
    #END get_data()

    def apply_data(self, data):
        """ Apply the given data to the tabWidgetItems of the tabWidget
        @type  data: dictionary
        @param data: store all the data for the tabWidgetItems in a dictionary
        """
        if not data:
            return
        #--- add the proper moduleType
        modtype = self.type_cb.findText(data['moduleType'])
        self.type_cb.setCurrentIndex(modtype)
        for row in range(self.main_tw.rowCount()):
            item = self.main_tw.cellWidget(row, 0)
            typ = str(type(item))
            typ = typ.split('.')[-1].split("'>")[0]
            #--- go through the widgets and change its values by the given data
            if typ == 'ComboBox':
                key = self.main_tw.verticalHeaderItem(row).text()
                itemindex = item.findText(str(data[key]))
                item.setCurrentIndex(itemindex)
            if typ == 'LineEdit':
                key = self.main_tw.verticalHeaderItem(row).text()
                item.setText(str(data[key]))
            if typ == 'IntLineEdit':
                key = self.main_tw.verticalHeaderItem(row).text()
                item.setText(str(data[key]))
            if typ == 'DoubleLineEdit':
                key = self.main_tw.verticalHeaderItem(row).text()
                item.setText(str(data[key]))
        #--- if specified lock specific tabWidgetItems
        if self.lock:
            self.lock_ui()
        if self.mirror:
            self.lock_mirror()
    #END apply_data()

    def lock_ui(self):
        """ Lock specific TabWidgetItems if flag has been set """
        #--- disable side and module name
        self.type_cb.setDisabled(True)
        for row in range(self.main_tw.rowCount()):
            item = self.main_tw.cellWidget(row, 0)
            key = self.main_tw.verticalHeaderItem(row).text()
            if (key == 'side' or
                key == 'moduleName' or
                key == 'mirror' or
                key == 'mirrorAxis' or
                key == 'asymmetry'):  # @IgnorePep8
                item.setDisabled(True)
    #END lock_ui()

    def lock_mirror(self):
        """ Lock specific TabWidgetItems for mirroring if flag has been set """
        #--- disable amount and guideChain name
        for row in range(self.main_tw.rowCount()):
            item = self.main_tw.cellWidget(row, 0)
            typ = str(type(item))
            typ = typ.split('.')[-1].split("'>")[0]
            key = self.main_tw.verticalHeaderItem(row).text()
            if (key == 'amount' or key == 'guideChain'):
                item.setDisabled(True)
    #END lock_mirror()

    def check_modulename(self):
        """ Check if moduleName has value, otherwise disable all tabItems """
        check = 1
        if 'Edit' in self.create_btn.text():
            return
        for row in range(self.main_tw.rowCount()):
            key = self.main_tw.verticalHeaderItem(row).text()
            if key == 'moduleName':
                item = self.main_tw.cellWidget(row, 0)
                if not item.text():
                    check = 0
            if not check:
                num = row + 1
                dis = self.main_tw.cellWidget(num, 0)
                if dis:
                    dis.setDisabled(True)
            else:
                dis = self.main_tw.cellWidget(row, 0)
                dis.setDisabled(False)
        self.check_side()
    #END check_modulename()

    def check_side(self):
        """ Check if side is set to L or R, otherwise disable mirror Items """
        check = 1
        if 'Edit' in self.create_btn.text():
            return
        for row in range(self.main_tw.rowCount()):
            key = self.main_tw.verticalHeaderItem(row).text()
            item = self.main_tw.cellWidget(row, 0)
            if key == 'moduleName':
                if not item.text():
                    return
            if key == 'side':
                if item.currentText() == 'C':
                    check = 0
            if not check:
                if (key == 'mirror' or key == 'mirrorAxis' or key == 'asymmetry'):
                    item.setCurrentIndex(0)
                    item.setDisabled(True)
            else:
                if (key == 'mirror' or key == 'mirrorAxis' or key == 'asymmetry'):
                    item.setDisabled(False)
    #END check_side()

    def check_completer(self):
        """ Check and add to the lineEdits a completer functionality"""
        for row in range(self.main_tw.rowCount()):
            key = self.main_tw.verticalHeaderItem(row).text()
            if (key == 'parentFirst' or key == 'parentLast'):
                item = self.main_tw.cellWidget(row, 0)
                comp = self.create_completer()
                item.setCompleter(comp)
    #END check_completer()

    def create_completer(self):
        """ List all the goe locators in the scene for autocompleter """
        validmod = list()
        #--- get the current moduleName
        try:
            mod = self.parent.modname
        except:
            for i in self.parent.framelist:
                rdata = i.rigdata
                if isinstance(rdata, list):
                    rdata = rdata[0]
                validmod.append(rdata['moduleName'])

        if not validmod:
            #--- get all the pevious moduleNames
            for i in self.parent.framelist:
                rdata = i.rigdata
                if isinstance(rdata, list):
                    rdata = rdata[0]
                if mod == rdata['moduleName']:
                    break
                validmod.append(rdata['moduleName'])

        #--- get only the valid control shapes
        model = QtGui.QStringListModel()
        shapes = list()
        for i in validmod:
            shape = cmds.ls('*' + i + '*', type='goe_locator')
            if not shape:
                continue
            for s in shape:
                shapes.append(s)

        #--- get the control transforms
        trn = [cmds.listRelatives(i, parent=True, type='transform')[0] for i in shapes]
        goe = list()
        for i in trn:
            if 'Guide' in i:
                res = i.split('Guide')[0] + i.split('Guide')[1]
                goe.append(res)
                continue
            goe.append(i)
        model.setStringList(goe)

        #--- create, set and return completer
        completer = QtGui.QCompleter()
        completer.setModel(model)
        completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        return completer
    #END create_completer()

    def connect_signals(self):
        """ Connect all the signals used in this UI """
        self.type_cb.currentIndexChanged.connect(self.add_data)
        if not self.create_btn.text() == 'Create':
            self.create_btn.clicked.connect(self.get_data)

        for row in range(self.main_tw.rowCount()):
            item = self.main_tw.cellWidget(row, 0)
            key = self.main_tw.verticalHeaderItem(row).text()
            if (key == 'moduleName'):
                item.editingFinished.connect(self.check_modulename)
            if (key == 'side'):
                item.currentIndexChanged.connect(self.check_side)
            if (key == 'parentFirst' or key == 'parentLast'):
                item.editingFinished.connect(self.check_completer)
    #END connect_signals()

    def __create(self):
        #--- add type data
        self.add_type_data()

        #--- get data
        self.add_data()

        #--- check module
        self.check_modulename()

        #--- check side
        self.check_side()

        #--- connect signals
        self.connect_signals()

        #--- check completer
        self.check_completer()
    #END __create()
#END CmdUI()


class ComboBox(QtGui.QComboBox):
    """ Custom ComboBox where the scrollEffect has been disabled """
    def __init__(self, parent=None, items=None):
        """
        @type  parent: class instance (self)
        @param parent: specify the class instance which is the parent

        @type  items: list
        @param items: specify a list of elements to add to the combobox
        """
        super(ComboBox, self).__init__(parent)
        self.parent = parent
        self.addItems(items)

    def wheelEvent(self, event):
        """
        @type  event: Qt event class
        @param event: specify the event to do something with that
        """
        event.ignore()
#END ComboBox()


class LineEdit(QtGui.QLineEdit):
    """ Custom LineEdit """
    def __init__(self, parent=None, text=None):
        """
        @type  parent: class instance (self)
        @param parent: specify the class instance which is the parent

        @type  text: string
        @param text: specify the text shown in the lineEdit
        """
        super(LineEdit, self).__init__(parent)
        self.parent = parent
        if not text == None:  # @IgnorePep8
            self.setText(str(text))
#END LineEdit()


class IntLineEdit(QtGui.QLineEdit):
    """ Custom LineEdit validating only integers """
    def __init__(self, parent=None, text=None):
        """
        @type  parent: class instance (self)
        @param parent: specify the class instance which is the parent

        @type  text: string
        @param text: specify the text shown in the lineEdit
        """
        super(IntLineEdit, self).__init__(parent)
        self.parent = parent
        if not text == None:  # @IgnorePep8
            self.setText(str(text))

        valid = QtGui.QIntValidator()
        self.setValidator(valid)
#END IntLineEdit()


class DoubleLineEdit(QtGui.QLineEdit):
    """ Custom LineEdit validating only doubles """
    def __init__(self, parent=None, text=None):
        """
        @type  parent: class instance (self)
        @param parent: specify the class instance which is the parent

        @type  text: string
        @param text: specify the text shown in the lineEdit
        """
        super(DoubleLineEdit, self).__init__(parent)
        self.parent = parent
        if not text == None:  # @IgnorePep8
            self.setText(str(text))

        valid = QtGui.QDoubleValidator()
        self.setValidator(valid)
#END DoubleLineEdit()
