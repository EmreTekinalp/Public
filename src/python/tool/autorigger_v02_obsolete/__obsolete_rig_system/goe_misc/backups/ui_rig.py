'''
@author:  etekinalp
@date:    Oct 9, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates and setups the rig settings ui
'''


import os
from goe_ui.pandoras_box.contents import utils

from PySide import QtGui, QtCore


path = os.path.join(os.path.dirname(__file__),'ui', 'rigSettings.ui')
assert os.path.exists(path), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(path)


class RigSettingsUI(base_class, form_class):
    """
    @DONE: setup ik disabled
    @DONE: setup float slider for size
    @DONE: check side and mirror checkbox
    @DONE: fix menubar
    @DONE: setup the data handling for the UI
    """
    def __init__(self, button='Create', lock=False, mirror=False):
        super(RigSettingsUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600,300,100,100)
        self.setWindowModality(QtCore.Qt.NonModal)
        self.create_btn.setText(button)

        #--- args
        self.lock   = lock
        self.mirror = mirror

        #--- vars
        self.data = dict()

        #--- methods
        if self.mirror:
            self.__lock_mirror()
        if self.lock:
            self.__lock_ui()
        self.__create()
    #END __init__()

    def __create_menu_bar(self):
        #--- create frame as offset
        frame = QtGui.QFrame()
        frame.setFixedHeight(10)

        #--- define menubar
        menubar = QtGui.QMenuBar(self)
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Reset settings')
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('Help on Rig Settings')

        self.main_layout.insertWidget(0, frame)
    #END __create_menu_bar()

    def __check_module(self):
        if not self.module_name_led.text():
            self.main_gb.setDisabled(True)
        if self.module_name_led.isModified():
            if self.module_name_led.text():
                self.main_gb.setDisabled(False)
            else:
                self.main_gb.setDisabled(True)
        else:
            if self.module_name_led.text():
                self.main_gb.setDisabled(False)
        self.module_name_led.setModified(False)
    #END __check_module()

    def __check_side(self):
        if not self.module_side_cb.currentIndex():
            self.mirror_chb.setDisabled(True)
            self.mirror_axis_lab.setDisabled(True)
            self.mirror_axis_cb.setDisabled(True)
            self.asymmetry_chb.setDisabled(True)
            self.color_sli.setValue(17)
        else:
            if self.module_side_cb.currentIndex() == 1:
                self.color_sli.setValue(6)
            else:
                self.color_sli.setValue(13)
            self.mirror_chb.setDisabled(False)
            if self.mirror_chb.isChecked():
                self.mirror_axis_lab.setDisabled(False)
                self.mirror_axis_cb.setDisabled(False)
                self.asymmetry_chb.setDisabled(False)
    #END __check_side()

    def __check_mirror(self):
        if self.mirror_chb.isChecked():
            self.mirror_axis_lab.setDisabled(False)
            self.mirror_axis_cb.setDisabled(False)
            self.asymmetry_chb.setDisabled(False)
            return
        self.asymmetry_chb.setChecked(False)
        self.mirror_axis_lab.setDisabled(True)
        self.mirror_axis_cb.setDisabled(True)
        self.asymmetry_chb.setDisabled(True)
    #END __check_mirror()

    def __check_line_edit(self):
        if self.amount_led.isModified():
            self.amount_sli.setValue(int(self.amount_led.text()))
        if self.size_led.isModified():
            self.size_sli.setValue(float(self.size_led.text()))
        if self.shape_led.isModified():
            self.shape_sli.setValue(int(self.shape_led.text()))
        if self.color_led.isModified():
            self.color_sli.setValue(int(self.color_led.text()))
        if self.mirror:
            self.amount_lab.setDisabled(True)
            self.amount_led.setDisabled(True)
    #END __check_line_edit()

    def __setup_line_edit(self):
        self.amount_led.setText(str(1))
        self.shape_led.setText(str(0))
        self.size_led.setText(str(1.0))
        self.color_led.setText(str(17))
        self.buffer_led.setText(str(0))

        #--- setup validators
        validatora = QtGui.QIntValidator()
        validatorb = QtGui.QIntValidator()
        validatorc = QtGui.QIntValidator()
        validatord = QtGui.QIntValidator()
        validatore = QtGui.QIntValidator()

        validatora.setBottom(1)
        validatorb.setBottom(0.0)
        validatorc.setRange(0,30)
        validatord.setRange(0,31)
        validatore.setRange(0,10)

        self.amount_led.setValidator(validatora)
        self.size_led.setValidator(validatorb)
        self.shape_led.setValidator(validatorc)
        self.color_led.setValidator(validatord)
        self.buffer_led.setValidator(validatore)
    #END __setup_line_edit()

    def __check_slider(self):
        if self.amount_sli.valueChanged:
            self.amount_led.setText(str(self.amount_sli.value()))
        if self.size_sli.valueChanged:
            scaledValue = float(self.size_sli.value()) / 10
            self.size_led.setText(str(scaledValue))
        if self.shape_sli.valueChanged:
            self.shape_led.setText(str(self.shape_sli.value()))
        if self.color_sli.valueChanged:
            self.color_led.setText(str(self.color_sli.value()))
        if self.buffer_sli.valueChanged:
            self.buffer_led.setText(str(self.buffer_sli.value()))
        if self.mirror:
            self.amount_sli.setDisabled(True)
    #END __check_slider()

    def __setup_slider(self):
        self.amount_sli.setRange(1,30)
        self.size_sli.setRange(0.0,100.0)
        self.size_sli.setSingleStep(1)
        self.shape_sli.setRange(0,30)
        self.color_sli.setRange(0,31)
        self.buffer_sli.setRange(0,10)

        self.amount_sli.setValue(1)
        self.size_sli.setValue(10)
        self.shape_sli.setValue(0)
        self.color_sli.setValue(17)
        self.buffer_sli.setValue(0)
    #END __setup_slider()

    def get_data(self):
        #--- get data
        self.data['modtype'] = str(self.module_type_cb.currentText())
        self.data['modside'] = str(self.module_side_cb.currentText())
        self.data['modname'] = str(self.module_name_led.text())
        if not self.data['modname']:
            self.data = dict()
            self.close()
            return
        #--- general data
        self.data['amount'] = int(self.amount_led.text())
        self.data['size'] = float(self.size_led.text())
        self.data['shape'] = int(self.shape_led.text())
        self.data['color'] = int(self.color_led.text())
        self.data['buffer'] = int(self.buffer_led.text())
        self.data['mirror'] = self.mirror_chb.isChecked()
        self.data['asymmetry'] = self.asymmetry_chb.isChecked()
        self.data['mirroraxis'] = str(self.mirror_axis_cb.currentText())
        self.data['guidechain'] = self.guide_chain_chb.isChecked()
        self.data['chain'] = self.control_chain_chb.isChecked()
        self.data['gimbal'] = self.gimbal_control_chb.isChecked()
        self.data['rotateorder'] = str(self.rotate_order_cb.currentText())
        self.data['joint'] = self.use_joints_chb.isChecked()
        self.data['parent'] = str(self.parent_type_cb.currentText())

        guides = list()
        for i in range(self.data['amount']):
            guides.append(self.data['modname'] + str(i))
        self.data['guides'] = guides

        mirrorside = None
        if self.data['mirror']:
            if self.data['modside'] == 'L':
                mirrorside = 'R'
            elif self.data['modside'] == 'R':
                mirrorside = 'L'
        self.data['mirrorside'] = mirrorside

        self.close()
        return self.data
    #END get_data()

    def apply_data(self, data):
        if not data:
            return
        modtype = self.module_type_cb.findText(data['modtype'])
        modside = self.module_side_cb.findText(data['modside'])
        maxis = self.mirror_axis_cb.findText(data['mirroraxis'])
        rotord = self.rotate_order_cb.findText(data['rotateorder'])
        parent = self.parent_type_cb.findText(data['parent'])

        self.module_type_cb.setCurrentIndex(modtype)
        self.module_side_cb.setCurrentIndex(modside)
        self.module_name_led.setText(data['modname'])

        #--- general data
        self.amount_led.setText(str(data['amount']))
        self.amount_sli.setValue(data['amount'])
        self.size_led.setText(str(data['size']))
        self.size_sli.setValue(data['size'] * 10)
        self.shape_led.setText(str(data['shape']))
        self.shape_sli.setValue(data['shape'])
        self.color_led.setText(str(data['color']))
        self.color_sli.setValue(data['color'])
        self.buffer_led.setText(str(data['buffer']))
        self.buffer_sli.setValue(data['buffer'])
        self.mirror_chb.setChecked(data['mirror'])
        self.asymmetry_chb.setChecked(data['asymmetry'])
        self.mirror_axis_cb.setCurrentIndex(maxis)
        self.guide_chain_chb.setChecked(data['guidechain'])
        self.control_chain_chb.setChecked(data['chain'])
        self.gimbal_control_chb.setChecked(data['gimbal'])
        self.rotate_order_cb.setCurrentIndex(rotord)
        self.use_joints_chb.setChecked(data['joint'])
        self.parent_type_cb.setCurrentIndex(parent)

        self.__check_module()
    #END apply_data()

    def __lock_ui(self):
        #--- disable side and module name
        self.module_type_lab.setDisabled(True)
        self.module_type_cb.setDisabled(True)
        self.module_side_lab.setDisabled(True)
        self.module_side_cb.setDisabled(True)
        self.module_name_lab.setDisabled(True)
        self.module_name_led.setDisabled(True)
        self.mirror_chb.setEnabled(False)
        self.mirror_axis_lab.setEnabled(False)
        self.mirror_axis_cb.setEnabled(False)
        self.asymmetry_chb.setEnabled(False)
    #END __lock_ui()

    def __lock_mirror(self):
        #--- disable side and module name
        self.amount_lab.setDisabled(True)
        self.amount_led.setDisabled(True)
        self.amount_sli.setDisabled(True)
        self.guide_chain_chb.setDisabled(True)
    #END __lock_mirror()

    def __connect_signals(self):
        if not self.lock:
            self.module_name_led.editingFinished.connect(self.__check_module)
            self.module_side_cb.currentIndexChanged.connect(self.__check_side)
            self.connect(self.mirror_chb, QtCore.SIGNAL("toggled(bool)"), self.__check_mirror)

        self.amount_led.editingFinished.connect(self.__check_line_edit)
        self.size_led.editingFinished.connect(self.__check_line_edit)
        self.shape_led.editingFinished.connect(self.__check_line_edit)
        self.color_led.editingFinished.connect(self.__check_line_edit)

        self.connect(self.amount_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.size_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.shape_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.color_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.buffer_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)

        self.create_btn.clicked.connect(self.get_data)
    #END __connect_signals()

    def __create(self):
        #--- create menu bar
        self.__create_menu_bar()

        #--- check module
        self.__check_module()

        #--- check side
        self.__check_side()

        #--- setup line edit
        self.__setup_line_edit()

        #--- setup slider
        self.__setup_slider()

        #--- check slider
        self.__check_slider()

        #--- connect signals
        self.__connect_signals()
    #END __create()
#END RigSettingsUI()


def main(*args, **kwargs):
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = RigSettingsUI()
    win.show()
#END main()

