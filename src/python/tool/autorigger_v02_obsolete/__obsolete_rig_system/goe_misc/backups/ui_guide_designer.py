'''
Created on Oct 9, 2014

@author: Emre
'''


import os
from goe_ui.pandoras_box.contents import utils

from PySide import QtGui, QtCore


path = os.path.join(os.path.dirname(__file__),'ui', 'guideSettingsDialog.ui')
assert os.path.exists(path), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(path)


class GuideSettingsUI(base_class, form_class):
    def __init__(self, buttonName='Create'):
        super(GuideSettingsUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600,300,100,100)
        self.setWindowModality(QtCore.Qt.NonModal)

        #--- vars
        self.data = list()
        self._button_name = buttonName

        #--- methods
        self.__create()
    #END __init__()

    def __create_menu_bar(self):
        #--- define menubar
        menubar = QtGui.QMenuBar(self)
        file_menu = menubar.addMenu('Edit')
        file_menu.addAction('Reset settings')

        help_menu = menubar.addMenu('Help')
        help_menu.addAction('Help on Guide Settings')
        self.main_layout.insertWidget(0, menubar)
    #END __create_menu_bar()

    def __check_module(self):
        if self.module_name_led.isModified():
            if self.module_name_led.text():
                self.__set_disabled(False)
            else:
                self.__set_disabled(True)
        else:
            if self.module_name_led.text():
                self.__set_disabled(False)
            else:
                self.__set_disabled(True)
        self.module_name_led.setModified(False)
    #END __check_module()

    def __check_side(self):
        if not self.side_cb.currentIndex():
            self.mirror_chb.setDisabled(True)
            self.mirror_axis_lab.setDisabled(True)
            self.mirror_axis_cb.setDisabled(True)
            self.asymmetry_chb.setDisabled(True)
            self.color_sli.setValue(17)
        else:
            if self.side_cb.currentIndex() == 1:
                self.color_sli.setValue(6)
            else:
                self.color_sli.setValue(13)
            if self.module_name_led.text():
                self.mirror_chb.setDisabled(False)
    #END __check_side()

    def __check_mirror(self):
        if self.mirror_chb.isChecked():
            self.mirror_axis_lab.setDisabled(False)
            self.mirror_axis_cb.setDisabled(False)
            self.asymmetry_chb.setDisabled(False)
            return
        self.mirror_axis_lab.setDisabled(True)
        self.mirror_axis_cb.setDisabled(True)
        self.asymmetry_chb.setDisabled(True)
    #END __check_mirror()

    def __set_disabled(self, disable=True):
        #--- disable labels
        self.amount_lab.setDisabled(disable)
        self.size_lab.setDisabled(disable)
        self.shape_lab.setDisabled(disable)
        self.color_lab.setDisabled(disable)

        if not disable:
            if self.side_cb.currentIndex():
                self.mirror_chb.setDisabled(disable)
            else:
                self.mirror_chb.setDisabled(True)
            if not self.mirror_chb.isChecked():
                self.mirror_axis_lab.setDisabled(True)
                self.mirror_axis_cb.setDisabled(True)
                self.asymmetry_chb.setDisabled(True)
            else:
                if self.side_cb.currentIndex():
                    self.mirror_chb.setDisabled(disable)
                self.mirror_axis_lab.setDisabled(disable)
                self.mirror_axis_cb.setDisabled(disable)
                self.asymmetry_chb.setDisabled(disable)
        else:
            self.mirror_chb.setDisabled(disable)
            self.mirror_axis_lab.setDisabled(disable)
            self.mirror_axis_cb.setDisabled(disable)
            self.asymmetry_chb.setDisabled(disable)

        #--- disable check boxes
        self.as_chain_chb.setDisabled(disable)
#         if not self.side_cb.currentIndex():
#             self.mirror_chb.setDisabled(True)

        #--- disable line edits
        self.amount_led.setDisabled(disable)
        self.size_led.setDisabled(disable)
        self.shape_led.setDisabled(disable)
        self.color_led.setDisabled(disable)

        #--- disable sliders
        self.amount_sli.setDisabled(disable)
        self.size_sli.setDisabled(disable)
        self.shape_sli.setDisabled(disable)
        self.color_sli.setDisabled(disable)
    #END __set_disabled()

    def __check_line_edit(self):
        if self.amount_led.isModified():
            self.amount_sli.setValue(int(self.amount_led.text()))
        if self.size_led.isModified():
            self.size_sli.setValue(float(self.size_led.text()))
        if self.shape_led.isModified():
            self.shape_sli.setValue(int(self.shape_led.text()))
        if self.color_led.isModified():
            self.color_sli.setValue(int(self.color_led.text()))
    #END __check_line_edit()

    def __setup_line_edit(self):
        self.amount_led.setText(str(1))
        self.size_led.setText(str(1.0))
        self.shape_led.setText(str(0))
        self.color_led.setText(str(17))

        #--- setup validators
        validatora = QtGui.QIntValidator()
        validatorb = QtGui.QIntValidator()
        validatorc = QtGui.QIntValidator()
        validatord = QtGui.QIntValidator()

        validatora.setBottom(1.0)
        validatorb.setBottom(0)
        validatorc.setRange(0,30)
        validatord.setRange(0,31)

        self.amount_led.setValidator(validatora)
        self.size_led.setValidator(validatora)
        self.shape_led.setValidator(validatorb)
        self.color_led.setValidator(validatorb)
    #END __setup_line_edit()

    def __check_slider(self):
        if self.amount_sli.valueChanged:
            self.amount_led.setText(str(self.amount_sli.value()))
        if self.size_sli.valueChanged:
            self.size_led.setText(str(self.size_sli.value()))
        if self.shape_sli.valueChanged:
            self.shape_led.setText(str(self.shape_sli.value()))
        if self.color_sli.valueChanged:
            self.color_led.setText(str(self.color_sli.value()))
    #END __check_slider()

    def __setup_slider(self):
        self.amount_sli.setRange(1,30)
        self.size_sli.setRange(0.0,100.0)
        self.shape_sli.setRange(0,30)
        self.color_sli.setRange(0,31)

        self.amount_sli.setValue(1)
        self.size_sli.setValue(1.0)
        self.shape_sli.setValue(0)
        self.color_sli.setValue(17)
    #END __setup_slider()

    def __close_window(self):
        self.data = []
        self.close()
    #END __close_window()

    def get_data(self):
        #--- get the info
        gtype = self.guide_type_cb.currentText()
        side = self.side_cb.currentText()
        mod = self.module_name_led.text()
        if not mod:
            self.data = []
            self.close()
            return
        name = gtype + 'Cmds: ' + side + '_' + mod.upper() + '_MOD'
        gtype = self.guide_type_cb.currentIndex()
        side = self.side_cb.currentIndex()
        amount = self.amount_led.text()
        size = self.size_led.text()
        shape = self.shape_led.text()
        color = self.color_led.text()
        chain = self.as_chain_chb.isChecked()
        if chain == True:
            chain = 1
        elif chain == False:
            chain = 0
        mirror = self.mirror_chb.isChecked()
        if mirror == True:
            mirror = 1
        elif mirror == False:
            mirror = 0
        maxis = self.mirror_axis_cb.currentIndex()
        asym = self.asymmetry_chb.isChecked()
        if asym == True:
            asym = 1
        elif asym == False:
            asym = 0
        self.data = [str(name), int(gtype), int(side), str(mod), int(amount), 
                     float(size), int(shape), int(color), int(chain), int(mirror), 
                     int(maxis), int(asym)]
        self.close()
        return self.data
    #END get_data()

    def apply_data(self, data):
        if not data:
            return
        #--- guideType
        self.guide_type_cb.setCurrentIndex(data[1])

        #--- side
        self.side_cb.setCurrentIndex(data[2])

        #--- moduleName
        self.module_name_led.setText(str(data[3]))

        #--- amount
        self.amount_led.setText(str(data[4]))
        self.amount_sli.setValue(data[4])

        #--- size
        self.size_led.setText(str(data[5]))
        self.size_sli.setValue(data[5])

        #--- shape
        self.shape_led.setText(str(data[6]))
        self.shape_sli.setValue(data[6])

        #--- color
        self.color_led.setText(str(data[7]))
        self.color_sli.setValue(data[7])

        #--- asChain
        self.as_chain_chb.setChecked(data[8])

        #--- mirror
        self.mirror_chb.setChecked(data[9])

        #--- mirrorAxis
        self.mirror_axis_cb.setCurrentIndex(data[10])

        #--- asymmetry
        self.asymmetry_chb.setChecked(data[11])

        #--- enable attributes
        self.__set_disabled(False)
    #END apply_data()

    def __connect_signals(self):
        self.module_name_led.editingFinished.connect(self.__check_module)
        self.side_cb.currentIndexChanged.connect(self.__check_side)
        self.amount_led.editingFinished.connect(self.__check_line_edit)
        self.size_led.editingFinished.connect(self.__check_line_edit)
        self.shape_led.editingFinished.connect(self.__check_line_edit)
        self.color_led.editingFinished.connect(self.__check_line_edit)
        self.connect(self.amount_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.size_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.shape_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.color_sli, QtCore.SIGNAL('valueChanged(int)'), self.__check_slider)
        self.connect(self.mirror_chb, QtCore.SIGNAL("toggled(bool)"), self.__check_mirror)
        self.close_btn.clicked.connect(self.__close_window)
        self.create_btn.clicked.connect(self.get_data)
    #END __connect_signals()

    def __create(self):
        #--- create menu bar
        self.__create_menu_bar()

        #--- check module
        self.__check_module()

        #--- setup line edit
        self.__setup_line_edit()

        #--- setup slider
        self.__setup_slider()

        #--- check side
        self.__check_side()

        #--- set disabled
        self.__set_disabled()

        #--- connect signals
        self.__connect_signals()
    #END __create()
#END GuideSettingsUI()


def main(*args, **kwargs):
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = GuideSettingsUI()
    win.show()
#END main()
