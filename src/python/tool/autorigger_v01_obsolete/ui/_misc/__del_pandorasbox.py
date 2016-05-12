#! C:\Program Files\Autodesk\Maya2014\bin\mayapy

"""
Created on 17.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The UI for the AutoRigger system.
"""
from maya import cmds
from maya import OpenMayaUI
import os
import sys
from functools import partial
from PySide import QtCore, QtGui

from ui.manager import attributemanager
from ui.manager import nodefactory

from ui.qtcustom import background
from ui.qtcustom import nodegraphicsview
from ui.qtcustom import qtutils

from utility import path

reload(attributemanager)
reload(nodefactory)

reload(nodegraphicsview)
reload(qtutils)

reload(path)

form_class, base_class = qtutils.load_ui_type(os.path.join(path.Path().resource(),
                                              'pandorasbox.ui'))

class PandorasBox(base_class, form_class):
    """The main ui for Pandora's Box.
    - data mapping ui - rigbuilder
    - put arm module value into .json file for ui

    """
    def __init__(self, parent=None):
        super(PandorasBox, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(760, 50, 400, 500)
        self.setup_ui()
        self.setup_css()
        self.setup_graphicsscene()
        self.attr_manager = attributemanager.AttributeManager(self)
        self.nf = nodefactory.NodeFactory()
        self.setup_right_attributes()
        #self.dothetest()
    # end def __init__

    def dothetest(self):
        """@todo: insert doc for dothetest"""

        # wid = QtGui.QWidget()
        # wid.setLayout(QtGui.QVBoxLayout())

        # self.panel = cmds.modelPanel(cam='persp', label='Test')
        # ptr_panel = OpenMayaUI.MQtUtil.findControl(self.panel)
        # self.modelPanelObject = qtutils.wrapinstance(ptr_panel)

        # wid.layout().addWidget(self.modelPanelObject.widget(0))
        # wid.resize(500, 500)

        # self.graphics_view.scene().addWidget(wid)

    # end def dothetest

    def setup_css(self):
        """Sets up the css for Pandora's Box"""
        css_file = os.path.join(path.Path().resource(), 'pandorasbox.css')
        with open(css_file, 'r') as f:
            css = f.read()
            f.close()
        self.setStyleSheet(css)
    # end def setup_css

    def setup_ui(self):
        """Sets up the ui:
            * Loads buttons for all available modules
            @todo: get all modules
        """
        # Add buttons for the rigging modules
        for module in self.get_rigging_modules():
            btn = QtGui.QPushButton()#dbutton.DraggableButton()
            btn.setText(module)
            self.tools_left_wrapper.insertWidget(0, btn)
            btn.clicked.connect(partial(self.add_rigging_module, module))
        # end for module in self.get_rigging_modules()
    # end def setup_ui

    def setup_graphicsscene(self):
        """Sets up the custom graphics scene."""
        self.graphics_view = nodegraphicsview.NodeGraphicsView()
        self.navigation_glay.addWidget(self.graphics_view)
        self.graphics_view.show()
        #self.graphics_view.scene().addItem(background.Background())
    # end def setup_graphicsscene



    def clicked(self, index):
        """"""

        print index.model().itemData(index)


        model = index.model()
        new_index = index
        hierarchy = list()
        while new_index.row()>-1:
            hierarchy.append(new_index)
            new_index = new_index.parent()
        # end while new_index.row()>-1
        parentitem = model
        for step in reversed(hierarchy):
            parentitem = parentitem.child(step.row(), step.column())
        # end for step in reversed(hierarchy)
        print parentitem.data(QtCore.Qt.UserRole)
    # end def clicked




    def setup_right_attributes(self):
        """Sets up the attribute pane on the right side."""
        self.attributes_right_treeview.doubleClicked.connect(self.clicked)
        self.tab_attributes.setLayout(QtGui.QVBoxLayout())
        self.tab_attributes.layout().addWidget(self.attributes_right_treeview)
        self.tab_module.setLayout(QtGui.QVBoxLayout())
        self.tab_module.layout().addWidget(self.nodegroup_right_treeview)
    # end def setup_right_attributes

    def get_rigging_modules(self):
        """Retrieves a list of all available rigging modules."""
        # modules_path = os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commands'))
        # modules = list()
        # for module in sorted(modules_path, reverse=True):
        #     if '__init__' in module or '.pyc' in module:
        #         continue
        #     modules.append(module[:-3])
        # # end for module in modules_path
        modules = ['arm']
        return modules
    # end def get_rigging_modules

    def add_rigging_module(self, module):
        """Adds a rigging module to the navigator."""
        self.graphics_view.scene().add_items(self.nf.create_module(module, self))
    # end def add_rigging_module

    def update_scene(self):
        """Updates the complete graphics scene."""
        self.graphics_view.updateScene([self.graphics_view.sceneRect()])
    # end def update_scene
# end class PandorasBox


def main():
    global pandorasbox
    try:
        pandorasbox.close()
    except:
        pass
    pandorasbox = PandorasBox(qtutils.get_maya_window())
    pandorasbox.show()
# end def main

#main()

def main_standalone():
    app = QtGui.QApplication(sys.argv)
    pandorasbox = PandorasBox()
    pandorasbox.show()
    sys.exit(app.exec_())
# end def main_standalone

#main_standalone()
