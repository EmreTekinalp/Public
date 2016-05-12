'''
@author:  etekinalp
@date:    Oct 4, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates the guide settings window
'''


from PySide import QtGui, QtCore
from shiboken import wrapInstance

from maya import OpenMayaUI


def get_maya_window():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QWidget)
#END get_maya_window()


guide_title  = "Guide Settings"
guide_object = "guide_settings"


class GuideSettings(QtGui.QDialog):
    """
    @DONE: add groupboxes for guide edit split into attributes
    @DONE: proper formatting and layouting.
    @DONE: slider connection with line edit and horizontal slider
    @DONE: add separator if necessary
    """
    def __init__(self, buttonName='Create', parent=get_maya_window()):
        super(GuideSettings, self).__init__(parent)

        #--- vars
        self.data = list()
        self._button_name = buttonName

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(guide_title)
        self.setObjectName(guide_object)
        self.setGeometry(600,300,500,300)
        self.setFixedSize(480, 350)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.widget = QtGui.QWidget()
    #END __setup_ui()

    def __create_menu_bar(self):
        #--- define menubar
        self.menubar = QtGui.QMenuBar(self)
        file_menu = self.menubar.addMenu('Edit')
        file_menu.addAction('Reset settings')

        help_menu = self.menubar.addMenu('Help')
        help_menu.addAction('Help on Guide Settings')
    #END __create_menu_bar()

    def __create_group_box(self):
        self.main_gb = QtGui.QGroupBox()
        self.attribute_gb = QtGui.QGroupBox('Attributes')
    #END __create_group_box()

    def __create_combo_boxes(self):
        #--- define combo boxes
        self.guide_type_box = QtGui.QComboBox()
        self.side_box = QtGui.QComboBox()
        self.mirror_axis_box = QtGui.QComboBox()

        #--- setup combo boxes
        self.guide_type_box.setFixedWidth(375)
        self.guide_type_box.addItems(['prop', 'piston', 'vehicle'])
        self.side_box.addItems(['C', 'L', 'R'])
        self.mirror_axis_box.addItems(['x', 'y', 'z'])
    #END __create_combo_boxes()

    def __create_check_boxes(self):
        #--- define check boxes
        self.as_chain_chb = QtGui.QCheckBox()
        self.mirror_chb = QtGui.QCheckBox()
        self.asym_chb = QtGui.QCheckBox()
    #END __create_check_boxes()

    def __create_labels(self):
        #--- define labels
        self.guide_type_txt = QtGui.QLabel('Guide Type:')
        self.side_txt = QtGui.QLabel('Side:')
        self.mod_txt = QtGui.QLabel('Module Name:')
        self.num_txt = QtGui.QLabel('Amount:')
        self.size_txt = QtGui.QLabel('Size:')
        self.shape_txt = QtGui.QLabel('Shape:')
        self.color_txt = QtGui.QLabel('Color:')
        self.as_chain_txt = QtGui.QLabel('As Chain:')
        self.mirror_txt = QtGui.QLabel('Mirror:')
        self.mirror_axis_txt = QtGui.QLabel('Mirror Axis:')
        self.asym_txt = QtGui.QLabel('Asymmetry:')
    #END __create_labels()

    def __create_line_edits(self):
        #--- define line edits
        self.mod_led = QtGui.QLineEdit()
        self.num_led = QtGui.QLineEdit()
        self.size_led = QtGui.QLineEdit()
        self.shape_led = QtGui.QLineEdit()
        self.color_led = QtGui.QLineEdit()

        #--- setup line edits
        self.num_led.setFixedSize(50, 20)
        self.size_led.setFixedSize(50, 20)
        self.shape_led.setFixedSize(50, 20)
        self.color_led.setFixedSize(50, 20)

        self.num_led.setText(str(1))
        self.size_led.setText(str(1))
        self.shape_led.setText(str(0))
        self.color_led.setText(str(17))

        #--- setup validators
        validatora = QtGui.QIntValidator()
        validatorb = QtGui.QIntValidator()
        validatorc = QtGui.QIntValidator()
        validatord = QtGui.QIntValidator()

        validatora.setBottom(1)
        validatorb.setBottom(0)
        validatorc.setRange(0,30)
        validatord.setRange(0,31)

        self.num_led.setValidator(validatora)
        self.size_led.setValidator(validatora)
        self.shape_led.setValidator(validatorb)
        self.color_led.setValidator(validatorb)
    #END __create_line_edits()

    def __create_buttons(self):
        #--- define buttons
        self.create_btn = QtGui.QPushButton(self._button_name)
        self.close_btn = QtGui.QPushButton("Close")
    #END __create_buttons()

    def __create_frame(self):
        #--- define frame
        self.framea = QtGui.QFrame()
        self.frameb = QtGui.QFrame()

        #--- setup frame
        self.framea.setFrameShape(QtGui.QFrame.HLine)
        self.framea.setFrameShadow(QtGui.QFrame.Sunken)
        self.frameb.setFrameShape(QtGui.QFrame.HLine)
        self.frameb.setFrameShadow(QtGui.QFrame.Sunken)
    #END __create_frame()

    def __create_sliders(self):
        #--- define sliders
        self.num_sli = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.size_sli = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.shape_sli = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.color_sli = QtGui.QSlider(QtCore.Qt.Horizontal)

        self.num_sli.setRange(1,100)
        self.size_sli.setRange(0,100)
        self.shape_sli.setRange(0,30)
        self.color_sli.setRange(0,31)

        self.num_sli.setValue(1)
        self.size_sli.setValue(1)
        self.shape_sli.setValue(0)
        self.color_sli.setValue(17)
    #END __create_sliders()

    def __setup_group_layout(self):
        #--- create layouts
        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.guide_type_txt)
        hbox.addWidget(self.guide_type_box)
        hbox.addStretch()

        attrbox = self.__setup_attribute_layout()
        self.attribute_gb.setLayout(attrbox)

        vbox.addLayout(hbox)
        vbox.addWidget(self.attribute_gb)
        self.main_gb.setLayout(vbox)
    #END __setup_group_layout()

    def __setup_attribute_layout(self):
        #--- create layouts
        vboxa = QtGui.QVBoxLayout()
        vboxb = QtGui.QVBoxLayout()
        vboxc = QtGui.QVBoxLayout()
        hboxa = QtGui.QHBoxLayout()
        hboxb = QtGui.QHBoxLayout()
        hboxc = QtGui.QHBoxLayout()
        hboxd = QtGui.QHBoxLayout()
        hboxe = QtGui.QHBoxLayout()
        hboxf = QtGui.QHBoxLayout()
        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.side_txt)
        hbox.addWidget(self.side_box)
        hbox.addWidget(self.mod_txt)
        hbox.addWidget(self.mod_led)

        vboxa.addWidget(self.num_txt)
        vboxa.addWidget(self.size_txt)
        vboxa.addWidget(self.shape_txt)
        vboxa.addWidget(self.color_txt)

        vboxb.addWidget(self.num_led)
        vboxb.addWidget(self.size_led)
        vboxb.addWidget(self.shape_led)
        vboxb.addWidget(self.color_led)

        vboxc.addWidget(self.num_sli)
        vboxc.addWidget(self.size_sli)
        vboxc.addWidget(self.shape_sli)
        vboxc.addWidget(self.color_sli)

        hboxa.addWidget(self.as_chain_txt)
        hboxa.addWidget(self.as_chain_chb)
        hboxa.addStretch()

        hboxa.addWidget(self.mirror_txt)
        hboxa.addWidget(self.mirror_chb)
        hboxa.addStretch()

        hboxa.addWidget(self.mirror_axis_txt)
        hboxa.addWidget(self.mirror_axis_box)
        hboxa.addStretch()

        hboxa.addWidget(self.asym_txt)
        hboxa.addWidget(self.asym_chb)
        hboxa.addStretch()

        hboxe.addLayout(vboxa)
        hboxe.addLayout(vboxb)
        hboxe.addLayout(vboxc)
        vbox.addLayout(hbox)
        vbox.addWidget(self.framea)
        vbox.addLayout(hboxe)
        vbox.addWidget(self.frameb)
        hboxf.addLayout(hboxa)
        hboxf.addLayout(hboxb)
        hboxf.addLayout(hboxc)
        hboxf.addLayout(hboxd)
        vbox.addLayout(hboxf)
        return vbox
    #END __setup_attribute_layout()

    def __setup_layout(self):
        #--- create layouts
        main_layout = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()

        #--- add widgets to layouts
        main_layout.addWidget(self.menubar)
        main_layout.addWidget(self.main_gb)
        hbox.addWidget(self.create_btn)
        hbox.addWidget(self.close_btn)
        main_layout.addLayout(hbox)

        #--- set layout
        self.setLayout(main_layout)
    #END __setup_layout

    def __check_module(self):
        if self.mod_led.isModified():
            if self.mod_led.text():
                self.__set_disabled(False)
            else:
                self.__set_disabled(True)
        else:
            if self.mod_led.text():
                self.__set_disabled(False)
            else:
                self.__set_disabled(True)
        self.mod_led.setModified(False)
    #END __check_module()

    def __check_mirror(self):
        if self.mirror_chb.isChecked():
            self.mirror_axis_txt.setDisabled(False)
            self.mirror_axis_box.setDisabled(False)
            self.asym_txt.setDisabled(False)
            self.asym_chb.setDisabled(False)
            return
        self.mirror_axis_txt.setDisabled(True)
        self.mirror_axis_box.setDisabled(True)
        self.asym_txt.setDisabled(True)
        self.asym_chb.setDisabled(True)
    #END __check_mirror()

    def __set_disabled(self, disable=True):
        #--- disable labels
        self.num_txt.setDisabled(disable)
        self.size_txt.setDisabled(disable)
        self.shape_txt.setDisabled(disable)
        self.color_txt.setDisabled(disable)
        self.as_chain_txt.setDisabled(disable)
        self.mirror_txt.setDisabled(disable)

        if not disable:
            if not self.mirror_chb.isChecked():
                self.mirror_axis_txt.setDisabled(True)
                self.mirror_axis_box.setDisabled(True)
                self.asym_txt.setDisabled(True)
                self.asym_chb.setDisabled(True)
            else:
                self.mirror_axis_txt.setDisabled(disable)
                self.mirror_axis_box.setDisabled(disable)
                self.asym_txt.setDisabled(disable)
                self.asym_chb.setDisabled(disable)
        else:
            self.mirror_axis_txt.setDisabled(disable)
            self.mirror_axis_box.setDisabled(disable)
            self.asym_txt.setDisabled(disable)
            self.asym_chb.setDisabled(disable)

        #--- disable check boxes
        self.as_chain_chb.setDisabled(disable)
        self.mirror_chb.setDisabled(disable)

        #--- disable line edits
        self.num_led.setDisabled(disable)
        self.size_led.setDisabled(disable)
        self.shape_led.setDisabled(disable)
        self.color_led.setDisabled(disable)

        #--- disable sliders
        self.num_sli.setDisabled(disable)
        self.size_sli.setDisabled(disable)
        self.shape_sli.setDisabled(disable)
        self.color_sli.setDisabled(disable)
    #END __set_disabled()

    def __setup_line_edit(self):
        if self.num_led.isModified():
            self.num_sli.setValue(int(self.num_led.text()))
        if self.size_led.isModified():
            self.size_sli.setValue(float(self.size_led.text()))
        if self.shape_led.isModified():
            self.shape_sli.setValue(int(self.shape_led.text()))
        if self.color_led.isModified():
            self.color_sli.setValue(int(self.color_led.text()))
    #END __setup_line_edit()

    def __setup_slider(self):
        if self.num_sli.valueChanged:
            self.num_led.setText(str(self.num_sli.value()))
        if self.size_sli.valueChanged:
            self.size_led.setText(str(self.size_sli.value()))
        if self.shape_sli.valueChanged:
            self.shape_led.setText(str(self.shape_sli.value()))
        if self.color_sli.valueChanged:
            self.color_led.setText(str(self.color_sli.value()))
    #END __setup_slider()

    def __close_window(self):
        self.data = []
        self.close()
    #END __close_window()

    def __get_data(self):
        #--- get the info
        gtype = self.guide_type_box.currentText()
        side = self.side_box.currentText()
        mod = self.mod_led.text()
        if not mod:
            self.data = []
            self.close()
            return
        name = gtype + 'Cmds: ' + side + '_' + mod.upper() + '_MOD'
        gtype = self.guide_type_box.currentIndex()
        side = self.side_box.currentIndex()
        amount = self.num_led.text()
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
        maxis = self.mirror_axis_box.currentIndex()
        asym = self.asym_chb.isChecked()
        if asym == True:
            asym = 1
        elif asym == False:
            asym = 0
        self.data = [str(name), int(gtype), int(side), str(mod), int(amount), 
                     float(size), int(shape), int(color), int(chain), int(mirror), 
                     int(maxis), int(asym)]
        self.close()
    #END __get_data()

    def apply_data(self, data):
        if not data:
            return
        #--- guideType
        self.guide_type_box.setCurrentIndex(data[1])

        #--- side
        self.side_box.setCurrentIndex(data[2])

        #--- moduleName
        self.mod_led.setText(str(data[3]))

        #--- amount
        self.num_led.setText(str(data[4]))
        self.num_sli.setValue(data[4])

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
        self.mirror_axis_box.setCurrentIndex(data[10])

        #--- asymmetry
        self.asym_chb.setChecked(data[11])

        #--- enable attributes
        self.__set_disabled(False)
#END apply_data()

    def __connect_signals(self):
        self.mod_led.editingFinished.connect(self.__check_module)
        self.num_led.editingFinished.connect(self.__setup_line_edit)
        self.size_led.editingFinished.connect(self.__setup_line_edit)
        self.shape_led.editingFinished.connect(self.__setup_line_edit)
        self.color_led.editingFinished.connect(self.__setup_line_edit)
        self.connect(self.num_sli, QtCore.SIGNAL('valueChanged(int)'), self.__setup_slider)
        self.connect(self.size_sli, QtCore.SIGNAL('valueChanged(int)'), self.__setup_slider)
        self.connect(self.shape_sli, QtCore.SIGNAL('valueChanged(int)'), self.__setup_slider)
        self.connect(self.color_sli, QtCore.SIGNAL('valueChanged(int)'), self.__setup_slider)
        self.connect(self.mirror_chb, QtCore.SIGNAL("toggled(bool)"), self.__check_mirror)
        self.close_btn.clicked.connect(self.__close_window)
        self.create_btn.clicked.connect(self.__get_data)
    #END __connect_signals()

    def __create(self):
        #--- setup ui specifics
        self.__setup_ui()

        #--- create menu bar
        self.__create_menu_bar()

        #--- create group box
        self.__create_group_box()

        #--- create combo boxes
        self.__create_combo_boxes()

        #--- create check boxes
        self.__create_check_boxes()

        #--- create labels
        self.__create_labels()

        #--- create line edits
        self.__create_line_edits()

        #--- create buttons
        self.__create_buttons()

        #--- create frame
        self.__create_frame()

        #--- create sliders
        self.__create_sliders()

        #--- setup group layout
        self.__setup_group_layout()

        #--- setup layout
        self.__setup_layout()

        #--- set disabled
        self.__set_disabled()

        #--- connect signals
        self.__connect_signals()
    #END __create()
#END GuideSettings()