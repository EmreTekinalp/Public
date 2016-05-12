"""Created on 2014/01/15
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The new ui for Pandora's Box.
"""

import os
import sys
from functools import partial
from PySide import QtCore, QtGui

from uiutility import qtutils
reload(qtutils)

from manager import nodedatamanager
reload(nodedatamanager)

from model import nodeitemdelegate
reload(nodeitemdelegate)

from model import rigmodulefactory
reload(rigmodulefactory)

from utility import path
reload(path)

from widget import attributeview
reload(attributeview)

from widget import mvlineedit
reload(mvlineedit)

from widget import navigatorview
reload(navigatorview)

from widget import rignode
reload(rignode)

from widget import dbutton
reload(dbutton)

form_class, base_class = qtutils.load_ui_type(os.path.join(path.resource(),
                                              'pandorasbox.ui'))

class MainUI(base_class, form_class):
    """The main ui for Pandora's Box.
    @todo: data mapping ui - rigbuilder
    @todo: utilize constants everywhere, please :)
    @todo: introduce core folder for namingconvention, path and so forth
    @todo: introduce mayaname section in the model
    @todo: create graphic nodes
    @todo: draggable buttons
    @todo: cleanup the module creation

    """
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(1430, -200, 550, 500)
        self.nodedatamanager = nodedatamanager.NodeDataManager(self)
        self.rigmodulefactory = rigmodulefactory.RigModuleFactory(self)
        self.modules = dict()
        self.load_modules()
        self.setup_ui()
        self.setup_css()
    # end def __init__

    def load_modules(self):
        """Loads all available rig modules.
        @todo: remove the test setup
        @todo: create method to obtain available modules

        """
        available_modules = ['test_joint', 'joint', 'arm']
        for available_module in available_modules:
            module_ = self.rigmodulefactory.create_final_data_dict(available_module)
            self.modules[available_module] = module_
        # end for module in available_modules
    # end def load_modules

    def create_node(self, module):
        """@todo: insert doc for create_node"""
        rignodes = self.rigmodulefactory.create_rigmodule(module)
        for rignode in rignodes:
            self.navigator_view.scene().addItem(rignode)
        # end for rignode in rignodes
    # end def create_node

    def setup_css(self):
        """Sets up the css for Pandora's Box"""
        css_file = os.path.join(path.resource(), 'pandorasbox.css')
        with open(css_file, 'r') as f:
            css = f.read()
            f.close()
        self.setStyleSheet(css)
    # end def setup_css

    def setup_ui(self):
        """Sets up the ui:
        * Creates buttons for all available modules

        """
        for module in self.modules:
            btn = dbutton.DButton(rigmodule=module)
            btn.setText(module)
            btn.setToolTip(self.modules[module]['description']['data'])
            btn.clicked.connect(partial(self.create_node, module))
            self.rigmodules_wrap.insertWidget(0, btn)
        # end for module in self.modules
    # end def setup_ui
# end class MainUI


def openui():
    global pandorasbox_mainui
    try:
        pandorasbox_mainui.close()
    except:
        pass
    pandorasbox_mainui = MainUI(qtutils.get_maya_window())
    pandorasbox_mainui.show()
# end def openui


def openui_standalone():
    app = QtGui.QApplication(sys.argv)
    pandorasbox = MainUI()
    pandorasbox.show()
    sys.exit(app.exec_())
# end def openui_standalone

#openui_standalone()
