'''
@author:  etekinalp
@date:    Sep 16, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains a main rig setup which should be subclassed
'''

from maya import cmds, OpenMaya

from goe_functions import check, controls, attribute

reload(check)
reload(controls)


class RigCmds(object):
    def __init__(self):
        #--- vars
        self.root = None
        self.geo_grp = None
        self.rig_grp = None
        self.main_mod = None
        self.main_control = None
        self.current_asset = None

        self._project = None
        self._asset_type = None
        self._asset_res = None
        self._asset_name = None

        #--- methods
        self.__create()
    #END __init__()

    def __check_scene(self):
        #--- check GUIDE ROOT, its attributes and values
        gr = "GUIDE_ROOT"
        assert cmds.objExists(gr), check.error(self, 0, gr)
        assert cmds.objExists(gr + ".project"), check.error(self, 0, gr + ".project")
        assert cmds.objExists(gr + ".assetType"), check.error(self, 0, gr + ".assetType")
        assert cmds.objExists(gr + ".assetResolution"), check.error(self, 0, gr + ".assetResolution")
        assert cmds.objExists(gr + ".assetName"), check.error(self, 0, gr + ".assetName")
        self._project = cmds.getAttr(gr + ".project")
        self._asset_type = cmds.getAttr(gr + ".assetType")
        self._asset_res = cmds.getAttr(gr + ".assetResolution")
        self._asset_name = cmds.getAttr(gr + ".assetName")
        assert self._project, check.error(self, 23, self._project)
        assert self._asset_type, check.error(self, 23, self._asset_type)
        assert self._asset_res, check.error(self, 23, self._asset_res)
        assert self._asset_name, check.error(self, 23, self._asset_name)
    #END __check_scene()

    def __create_rig_structure(self):
        self.root = self._asset_name
        self.geo_grp = 'GEO'
        self.rig_grp = 'RIG'
        self.main_mod = 'C_main_MOD'
        if not cmds.objExists(self.root):
            self.root = cmds.createNode('transform', name=self.root)
        if not cmds.objExists(self.geo_grp):
            self.geo_grp = cmds.createNode('transform', name=self.geo_grp,
                                           parent=self.root)
        if not cmds.objExists(self.rig_grp):
            self.rig_grp = cmds.createNode('transform', name=self.rig_grp,
                                           parent=self.root)
        if not cmds.objExists(self.main_mod):
            self.main_mod = cmds.createNode('transform', name=self.main_mod,
                                            parent=self.rig_grp)
    #END __create_rig_structure()

    def __setup_rig_structure(self):
        groot = 'GUIDE_ROOT'
        assert cmds.objExists(groot), check.error(self, 0, groot)
        if not cmds.objExists(self.root + '.project'):
            project = cmds.getAttr(groot + '.project')
            cmds.addAttr(self.root, longName='project', dataType='string')
            cmds.setAttr(self.root + '.project', project,
                         type='string', lock=True)
        if not cmds.objExists(self.root + '.assetType'):
            asset_type = cmds.getAttr(groot + '.assetType')
            cmds.addAttr(self.root, longName='assetType', dataType='string')
            cmds.setAttr(self.root + '.assetType', asset_type,
                         type='string', lock=True)
        if not cmds.objExists(self.root + '.assetResolution'):
            asset_res = cmds.getAttr(groot + '.assetResolution')
            cmds.addAttr(self.root, longName='assetResolution',
                         dataType='string')
            cmds.setAttr(self.root + '.assetResolution', asset_res,
                         type='string', lock=True)
        if not cmds.objExists(self.root + '.assetName'):
            asset_name = cmds.getAttr(groot + '.assetName')
            cmds.addAttr(self.root, longName='assetName', dataType='string')
            cmds.setAttr(self.root + '.assetName', asset_name,
                         type='string', lock=True)

    def __get_boundingbox_distance(self):
        meshes = cmds.ls(type='mesh')
        if not meshes:
            cmds.warning("RigCmds: No meshes in the scene!")
            return 1
        bb = cmds.exactWorldBoundingBox(meshes)
        FROM = OpenMaya.MPoint()
        TO = OpenMaya.MPoint()
        FROM.x = bb[0]
        FROM.y = bb[1]
        FROM.z = bb[2]
        TO.x = bb[3]
        TO.y = bb[4]
        TO.z = bb[5]
        distance = (FROM.distanceTo(TO) / 2)
        return distance
    #END __get_boundingbox_distance()

    def __create_controls(self):
        dist = self.__get_boundingbox_distance()
        #--- main control
        self.main_control = controls.Control(side='C',
                                             name='main',
                                             shape=12,
                                             size=dist, color=4,
                                             offsetGroups=1,
                                             withGimbal=True,
                                             parent=self.main_mod,
                                             exists=True)
        #--- current asset control
        self.current_asset = controls.Control(side='C',
                                              name='currentAsset',
                                              shape=2,
                                              size=dist / 4,
                                              color=4,
                                              orientation=42,
                                              position=[0, dist, 0],
                                              lockAttrs={'transform': ['t', 'r', 's']},
                                              parent=self.main_control.gimbal,
                                              exists=True)
    #END __create_controls()

    def __setup_controls(self):
        #--- showAll
        if not cmds.objExists(self.root + '.showAll'):
            attribute.lock_all(self.root)
            cmds.addAttr(self.root, longName='showAll', attributeType='short',
                         defaultValue=1, min=0, max=1)
            cmds.setAttr(self.root + '.showAll', edit=True, channelBox=True)
            attribute.lock_n_hide(self.root, ['v'], True)
            cmds.connectAttr(self.root + '.showAll', self.root + '.v')
            attribute.lock_n_hide(self.root, ['v'])
        #--- showGeo
        if not cmds.objExists(self.geo_grp + '.showGeo'):
            attribute.lock_all(self.geo_grp)
            cmds.addAttr(self.geo_grp, longName='showGeo',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.geo_grp + '.showGeo', edit=True, channelBox=True)
            attribute.lock_n_hide(self.geo_grp, ['v'], True)
            cmds.connectAttr(self.geo_grp + '.showGeo', self.geo_grp + '.v')
            attribute.lock_n_hide(self.geo_grp, ['v'])
        #--- showRig
        if not cmds.objExists(self.rig_grp + '.showRig'):
            attribute.lock_all(self.rig_grp)
            cmds.addAttr(self.rig_grp, longName='showRig',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.rig_grp + '.showRig', edit=True, channelBox=True)
            attribute.lock_n_hide(self.rig_grp, ['v'], True)
            cmds.connectAttr(self.rig_grp + '.showRig', self.rig_grp + '.v')
            attribute.lock_n_hide(self.rig_grp, ['v'])
        #--- showCurrent
        if not cmds.objExists(self.rig_grp + '.showCurrent'):
            cmds.addAttr(self.rig_grp, longName='showCurrent',
                         attributeType='short', defaultValue=0, min=0, max=1)
            cmds.setAttr(self.rig_grp + '.showCurrent',
                         edit=True, channelBox=True)
            attribute.lock_n_hide(self.current_asset.shape, ['v'], True)
            cmds.connectAttr(self.rig_grp + '.showCurrent',
                             self.current_asset.shape + '.v')
        #--- globalScale
        if not cmds.objExists(self.main_control.transform + '.globalScale'):
            cmds.addAttr(self.main_control.transform, longName='globalScale',
                         attributeType='float', defaultValue=1,
                         min=0, keyable=True)
            for axis in 'xyz':
                attribute.lock_n_hide(self.main_control.transform, ['s'], True)
                cmds.connectAttr(self.main_control.transform + '.globalScale',
                                 self.main_control.transform + '.s' + axis)
                attribute.lock_n_hide(self.main_control.transform, ['s'])
    #END __setup_controls()

    def __setup_meshes(self):
        if cmds.objExists(self.geo_grp):
            root = cmds.listRelatives(self.geo_grp, parent=True)
            if not root:
                cmds.parent(self.geo_grp, self.root)
            else:
                if not root[0] == self.root:
                    cmds.parent(self.geo_grp, self.root)
            return
        meshes = cmds.ls(type='mesh')
        for i in meshes:
            trn = cmds.listRelatives(i, parent=True, type='transform')
            if trn:
                geo = cmds.listRelatives(trn, parent=True)
                if geo:
                    if not geo[0] == self.geo_grp:
                        cmds.parent(trn, self.geo_grp)
                else:
                    cmds.parent(trn, self.geo_grp)
    #END __setup_meshes()

    def __cleanup(self):
        attribute.lock_all(self.main_mod)
    #END __cleanup()

    def __create(self):
        #--- check scene
        self.__check_scene()

        #--- create rig structure
        self.__create_rig_structure()

        #--- setup rig structure
        self.__setup_rig_structure()

        #--- create controls
        self.__create_controls()

        #--- setup controls
        self.__setup_controls()

        #--- setup meshes
        self.__setup_meshes()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END RigCmds()
