'''
@author:  etekinalp
@date:    Oct 9, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates and setups the pandorasBox UI
'''


import os
import imp
import pymel.core

from maya import cmds
from PySide import QtGui

from goe_ui.pandoras_box.contents import content, utils
from goe_ui.pandoras_box import ui_settings
from goe_functions import guides, data

reload(ui_settings)
reload(content)
reload(data)
reload(guides)


path = os.path.join(os.path.dirname(__file__), 'ui', 'pandorasbox.ui')
assert os.path.exists(path), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(path)


class PandorasBoxUI(base_class, form_class):
    """ This class creates the PandorasBoxUI which will be docked. """
    def __init__(self):
        """ Initialize the class and subclass and setup PandorasBox UI """
        super(PandorasBoxUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600, 300, 475, 817)

        #--- vars
        self.rigdata = list()
        self.framelist = list()
        self.frameSelected = list()
        self.check = 0

        #--- methods
        self.create()

        #--- define shortcuts
        QtGui.QShortcut(QtGui.QKeySequence("Alt+3"), self, self.build_guides)
        QtGui.QShortcut(QtGui.QKeySequence("Alt+2"), self, self.build_puppets)
        QtGui.QShortcut(QtGui.QKeySequence("Alt+1"), self, self.build_all)
    #END __init__()

    def create_header(self):
        """ Create the header including the image """
        file_path = os.path.dirname(__file__)
        icons_path = os.path.join(os.path.abspath(file_path), "icons")
        msg = "Path does not exist: " + repr(icons_path)
        assert os.path.exists(icons_path), msg

        #--- header image
        header_pic = QtGui.QPixmap(os.path.join(icons_path, "header.jpg"))
        self.pandoras_box_lab.setPixmap(header_pic)
    #END create_header()

    def setup_scroll_area(self):
        """ Setup the scroll area and makes the UI scrollable """
        self.main_scroll_area_scr.setFrameShape(QtGui.QFrame.NoFrame)
    #END setup_scroll_area()

    def check_project_path(self):
        """ Check the project path """
        #--- get project info
        self.project_info = content.get_project_info()

        #--- set project info
        self.set_project_info()
    #END check_project_path()

    def set_project_info(self):
        """ Set project info and add items to the comobobox widget """
        #--- set project info
        if not self.project_info:
            return
        self.projects = [i.keys()[0] for i in self.project_info]
        self.project_name_cb.clear()
        if self.projects:
            self.projects.sort()
            self.projects.insert(0, '...')
            self.project_name_cb.addItems(self.projects)
        else:
            self.project_name_cb.addItem('...')
    #END set_project_info()

    def update_project_info(self):
        """ Update project info, the project and the asset type """
        self.status_lab.clear()
        self.current_project = self.project_name_cb.currentText()
        self.asset_type_cb.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                self.types = i[1].keys()
                if self.types:
                    self.types.sort()
                    self.asset_type_cb.addItems(self.types)
    #END update_project_info()

    def update_type_info(self):
        """ Update asset type info and the assets """
        self.status_lab.clear()
        if not self.types:
            return
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.asset_name_cb.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                for t in i[1].items():
                    if not self.current_type == t[0]:
                        continue
                    self.assets = t[1]
                    if self.assets:
                        self.assets.sort()
                        assetlist = list()
                        for a in self.assets:
                            assetlist.append(a.keys()[0])
                        self.asset_name_cb.addItems(assetlist)
    #END update_type_info()

    def update_asset_info(self):
        """ Update asset info and the asset resolution """
        self.status_lab.clear()

        if not self.asset_name_cb.currentText():
            self.asset_res_cb.clear()
            return

        #--- update the asset resolution
        self.asset_res_cb.clear()
        for i in self.assets:
            if self.asset_name_cb.currentText() == i.keys()[0]:
                vals = i.values()[0]
                if 'lo' in vals:
                    num = vals.index('lo')
                    vals.pop(num)
                    vals.insert(-1, 'lo')
                if 'mid' in vals:
                    num = vals.index('mid')
                    vals.pop(num)
                    vals.insert(-2, 'mid')
                if 'hi' in vals:
                    num = vals.index('hi')
                    vals.pop(num)
                    vals.insert(0, 'hi')
                self.asset_res_cb.addItems(vals)
    #END update_asset_info()

    def clear_layout(self, layout):
        """ Clear the QFrame widget layout and the framelist
        @type  layout: string
        @param layout: Specify the layout which should be cleared
        """
        if layout:
            if not self.framelist:
                return
            for i in self.framelist:
                index = layout.indexOf(i)
                item = layout.takeAt(index)
                item.widget().deleteLater()
            self.framelist = []
    #END clear_layout()

    def update_res_info(self):
        """ Update asset resolution info and clear the layout """
        self.status_lab.clear()
        self.clear_layout(self.rig_lay)

        if not self.asset_name_cb.currentText():
            return

        path = os.path.join(content.get_project_path(), 'goe_builds',
                            self.project_name_cb.currentText(),
                            self.asset_type_cb.currentText(),
                            self.asset_name_cb.currentText(),
                            'build_' + self.asset_res_cb.currentText(),
                            'data', 'misc', 'guides_build.json')
        guide_data = content.setup_guide_ui(path)
        if not guide_data:
            return
        for gd in guide_data:
            #--- create and setup frame
            self.frame = content.FrameGuide(self, self.framelist, gd)
            self.framelist.append(self.frame)

            index = len(self.framelist)
            self.rig_lay.insertWidget(index, self.frame)
    #END update_res_info()

    def check_asset(self):
        """ Check asset and return True or False """
        if self.project_name_cb.currentText() == '...':
            return False
        if not self.asset_type_cb.currentText():
            return False
        if not self.asset_name_cb.currentText():
            return False
        return True
    #END check_asset()

    def check_goe_cmds(self, cmd=None):
        """ Check the command type and import return the path """
        assert cmd, "No command specified to import guides and rigs"
        path = os.path.join(content.get_project_path(), 'goe_cmds', cmd + '.py')
        return path
    #END check_project_settings()

    def check_project_settings(self):
        """ Check the project settings, return the asset.py file path"""
        self.check_asset()
        path = os.path.join(content.get_project_path(),
                            'goe_builds',
                            self.project_name_cb.currentText(),
                            self.asset_type_cb.currentText(),
                            self.asset_name_cb.currentText(),
                            'build_' + self.asset_res_cb.currentText(),
                            self.asset_name_cb.currentText() + '.py')
        return path
    #END check_project_settings()

    def create_items(self):
        """ Create the QFrame widget and get data from rig settings UI """
        if not self.check_asset():
            cmds.confirmDialog(title='Specify Asset',
                               message="Please specify the asset first!",
                               button=['Ok'],
                               defaultButton='Ok',
                               dismissString='Ok')
            return

        #--- open rig settings
        global rig
        try:
            if cmds.window(rig.objectName(), query=True, exists=True):
                rig.close()
                rig.deleteLater()
        except:
            pass

        rig = ui_settings.SettingsUI(self)
        rig.show()
        rig.create_btn.clicked.connect(self.create_frame)
    #END create_items()

    def create_frame(self):
        result = rig.get_data()
        if result:
            #--- create and setup frame
            self.frame = content.FrameGuide(self, self.framelist, rig.data)
            self.framelist.append(self.frame)

            index = len(self.framelist)
            self.rig_lay.insertWidget(index, self.frame)
    #END create_frame()

    def move_up(self):
        """ Move the QFrame widget up by pressing the move up button """
        #--- locate the selected frame
        for index, i in enumerate(self.framelist):
            if i.styleSheet() == 'background-color: rgb(60,60,60)':
                self.frameSelected = [i, index]
                self.check = 1

        if not self.check:
            return

        index = self.frameSelected[1]

        if not index:
            self.rig_lay.insertWidget(0, self.frameSelected[0])
        else:
            self.rig_lay.insertWidget(index - 1, self.frameSelected[0])
            self.framelist.pop(index)
            self.framelist.insert(index - 1, self.frameSelected[0])
    #END move_up()

    def move_down(self):
        """ Move the QFrame widget down by pressing the move down button """
        self.check = 0
        for index, i in enumerate(self.framelist):
            if i.styleSheet() == 'background-color: rgb(60,60,60)':
                self.frameSelected = [i, index]
                self.check = 1

        if not self.check:
            return

        index = self.frameSelected[1]
        selected = self.frameSelected[0]
        if index == len(self.framelist):
            self.rig_lay.insertWidget(len(self.framelist), selected)
        else:
            self.rig_lay.insertWidget(index + 1, selected)
            self.framelist.pop(index)
            self.framelist.insert(index + 1, selected)
    #END move_down()

    def load_latest_asset(self):
        """ Load the latest asset from the release folder structure """
        project = self.project_name_cb.currentText()
        atype = self.asset_type_cb.currentText()
        aname = self.asset_name_cb.currentText()
        ares = self.asset_res_cb.currentText()
        asset = content.get_latest_release(project, atype, aname, ares)

        #--- open new scene
        cmds.file(new=True, force=True)
        #--- if it's empty than give warning
        if not asset:
            cmds.warning('No asset found in modeling/release folder')
            return
        #--- import the latest release
        cmds.file(asset, i=True)
        #--- turn on shaded mode
        viewport = cmds.getPanel(withFocus=True)
        if 'modelPanel' in viewport:
            cmds.modelEditor(viewport, edit=True, displayAppearance='smoothShaded')
    #END load_latest_asset()

    def build_guides(self):
        """ Build the guides of the specific cmds, here is the cmds list """
        if not self.check_asset():
            cmds.confirmDialog(title='Specify Asset',
                               message="Please specify the asset first!",
                               button=['Ok'],
                               defaultButton='Ok',
                               dismissString='Ok')
            return

        #--- load latest asset
        self.load_latest_asset()

        #--- setup guides root
        if not cmds.objExists('GUIDE_ROOT'):
            path = self.check_project_settings()
            guides.SetupRoot(path)

        #--- get guide data information and dynamically create guides
        for i in self.framelist:
            rdata = i.rigdata
            if isinstance(rdata, list):
                rdata = rdata[0]
            self.import_guides(cmd=rdata['moduleType'], data=rdata)

        #--- load the guides data
        self.load_guides(info=False)

        #--- set status line
        self.status_lab.setText('--- GUIDES ---')
    #END build_guides()

    def save_guides(self, info=True):
        """ Save the guides, guideRoot has to exist in the scene
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- save the guides data
        data.save_guides(self.framelist, info)
    #END save_guides()

    def load_guides(self, info=True):
        """ Load the guides, guideRoot has to exist in the scene
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- load the guides data
        data.load_guides(info)
    #END load_guides()

    def build_puppets(self):
        """ Build the puppets based on the saved rigdata, cmds list is here """
        #--- build guides
        self.build_guides()

        if not self.check_asset():
            return

        #--- save guides
        self.save_guides(info=False)

        #--- build puppet
        result = dict()
        for i in self.framelist:
            rdata = i.rigdata
            if isinstance(rdata, list):
                for r in rdata:
                    key, value = self.import_puppets(r['moduleType'], r)
                    result[key] = value
            else:
                key, value = self.import_puppets(rdata['moduleType'], rdata)
                result[key] = value

        #--- generate code in obj.py
        data.generate_objects(result)

        #--- set status line
        self.status_lab.setText('--- PUPPETS ---')
    #END build_puppets()

    def save_shapes(self, info=True):
        """ Save the locator shapes
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- save the shapes data
        data.save_shapes(info)
    #END save_shapes()

    def load_shapes(self, info=True):
        """ Load the locator shapes
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- load the guides data
        data.load_shapes(info)
    #END load_shapes()

    def save_weights(self, info=True):
        """ Save the weights
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- save the shapes data
        data.save_weights(info)
    #END save_weights()

    def load_weights(self, info=True):
        """ Load the weights
        @type  info: bool
        @param info: Specify if you want to print info status
        """
        if not self.check_asset():
            return
        #--- load the guides data
        data.load_weights(info)
    #END load_weights()

    def import_guides(self, cmd=None, data=None):
        """ Dynamically import the guides classes of the module """
        #--- get asset path
        path = self.check_goe_cmds(cmd)

        #--- dynamically import modules
        if os.path.exists(path):
            mod = imp.load_source(cmd, path)
            try:
                reload(mod)
            except:
                pass
            mod.main_call(callMethod='guide', data=data)
    #END import_guides()

    def import_puppets(self, cmd=None, data=None):
        """ Dynamically import the rig classes of the module """
        #--- get asset path
        path = self.check_goe_cmds(cmd)

        #--- dynamically import modules
        if os.path.exists(path):
            mod = imp.load_source(cmd, path)
            try:
                reload(mod)
            except:
                pass
            key, value = mod.main_call(callMethod='puppet', data=data)
            return key, value
    #END import_guides()

    def import_fixes(self):
        """ Dynamically import the perCharacterFixes modules """
        #--- get asset path
        path = self.check_project_settings()

        #--- dynamically import modules
        if os.path.exists(path):
            mod = imp.load_source(self.asset_name_cb.currentText(), path)
            try:
                reload(mod)
            except:
                pass
    #END import_fixes()

    def build_all(self):
        """ Build guides, load asset, build puppet, include asset.py """
        #--- build puppets
        self.build_puppets()

        if not self.check_asset():
            return

        #--- import fixes
        self.import_fixes()

        #--- load control shapes
        self.load_shapes(info=False)

        #--- load weights
        self.load_weights(info=False)

        #--- set status line
        self.status_lab.setText('--- ALL ---')
    #END build_all()

    def connect_signals(self):
        """ Connect all the signals used in this UI """
        self.project_name_cb.currentIndexChanged['QString'].connect(self.update_project_info)
        self.asset_type_cb.currentIndexChanged['QString'].connect(self.update_type_info)
        self.asset_name_cb.currentIndexChanged['QString'].connect(self.update_asset_info)
        self.asset_res_cb.currentIndexChanged['QString'].connect(self.update_res_info)

        #--- create rig
        self.create_btn.clicked.connect(self.create_items)
        self.move_up_btn.clicked.connect(self.move_up)
        self.move_down_btn.clicked.connect(self.move_down)

        #--- setup guides
        self.build_guides_btn.clicked.connect(self.build_guides)
        self.save_guides_btn.clicked.connect(self.save_guides)
        self.load_guides_btn.clicked.connect(self.load_guides)

        #--- setup puppets
        self.build_puppets_btn.clicked.connect(self.build_puppets)
        self.save_shapes_btn.clicked.connect(self.save_shapes)
        self.load_shapes_btn.clicked.connect(self.load_shapes)

        #--- setup weights
        self.save_weights_btn.clicked.connect(self.save_weights)
        self.load_weights_btn.clicked.connect(self.load_weights)

        #--- build all
        self.build_btn.clicked.connect(self.build_all)
    #END connect_signals()

    def create(self):
        """ the main create method which will be run by first call """
        #--- create header
        self.create_header()

        #--- setup scroll area
        self.setup_scroll_area()

        #--- check project path
        self.check_project_path()

        #--- connect signals
        self.connect_signals()
    #END create()
#END PandorasBoxUI()


def main(*args, **kwargs):
    """ Call and build the UI as dockControl by using pymel """
    global win
    dock_object = "goe_pandorasBox_dock"
    #--- check if dockControl exists
    if pymel.core.dockControl(dock_object, q=1, ex=1):
        pymel.core.deleteUI(dock_object)
    #--- define allowedAreas to dock the UI
    allowedAreas = ['right', 'left']
    try:
        floatingLayout = pymel.core.paneLayout(configuration='single',
                                               width=300, height=400)
    except:
        pass

    #--- call the UI
    win = PandorasBoxUI()

    #--- add the UI to a dockControl by using pymel
    pymel.core.dockControl(dock_object, area='right', allowedArea=allowedAreas,
                           content=floatingLayout, label='PandorasBox')
    pymel.core.control(win.objectName(), e=True, p=floatingLayout)
    return True
#END main()

main()
