'''
@author:  etekinalp
@date:    Oct 9, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates and setups the rig settings ui
'''


import os
from goe_ui.pandoras_box.contents import utils, attributedelegate
from PySide import QtGui, QtCore
reload(attributedelegate)

path = os.path.join(os.path.dirname(__file__),'ui', 'modelView.ui')
assert os.path.exists(path), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(path)


class ModelViewUI(base_class, form_class):
    def __init__(self, parent=None):
        super(ModelViewUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600,300,200,400)
        self.setWindowModality(QtCore.Qt.NonModal)

        #--- args
        self.parent = parent

#         self.attribute_tv.setModel(self.parent.model)

        self.type_cb.setModel(self.parent.model)

        self.__connect_signals()
        
        delegate = attributedelegate.AttributeDelegate(self.attribute_tv)
        self.attribute_tv.setItemDelegate(delegate)
        
        #--- methods
        # self.__create()
    #END __init__()




###############################################################################


    def add_type_data(self):
        self.type_cb.addItems(['propCmds', 'pistonCmds'])
    #END add_type_data()

    def add_model_data(self):
        hheader = self.attribute_tv.horizontalHeader()
        hheader.setStretchLastSection(True)

        arg = QtGui.QStandardItem('value')
        self.model.setHorizontalHeaderItem(0, arg)

        side = QtGui.QStandardItem('side')
        mod = QtGui.QStandardItem('mod')
        name = QtGui.QStandardItem('name')
        amount = QtGui.QStandardItem('amount')
        self.model.setVerticalHeaderItem(0, side)
        self.model.setVerticalHeaderItem(1, mod)
        self.model.setVerticalHeaderItem(2, name)
        self.model.setVerticalHeaderItem(3, amount)

        itema = QtGui.QStandardItem('asdasd')
        itemb = QtGui.QStandardItem('gdfhjzujki')
        self.model.setItem(0, itema)
        self.model.setItem(1, itemb)
        self.parent.data['itema'] = 'asdasd'
        self.parent.data['itemb'] = 'gdfhjzujki'

        self.attribute_tv.setModel(self.model)
    #END add_type_data()

    def get_data(self):
        print self.parent.data
        self.close()
    #END get_data()

    def __connect_signals(self):
#         self.create_btn.clicked.connect(self.get_data)
        self.type_cb.currentIndexChanged.connect(self.set_rigCmds_index)
    #END __connect_signals()


    def set_rigCmds_index(self, index):
        self.attribute_tv.setModel(self.parent.model)
        model = self.parent.model
        item_index = model.indexFromItem(model.item(index, 0))
        self.attribute_tv.setRootIndex(item_index)
        
        for row in range(model.item(index, 0).rowCount()):
            item = model.item(index, 0).child(row, 0)
            data = item.data(QtCore.Qt.DisplayRole)
            display_item = QtGui.QStandardItem(data)
            self.parent.model.setVerticalHeaderItem(row, display_item)


    def __create(self):
        #--- add type data
        self.add_type_data()

        #--- add type data
        self.add_model_data()

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

    win = ModelViewUI()
    win.show()
#END main()
