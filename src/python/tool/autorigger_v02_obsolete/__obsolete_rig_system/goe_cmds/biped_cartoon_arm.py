'''
@author:  etekinalp
@date:    Nov 17, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module stores the class for an anatomical correct arm rig
'''


from maya import cmds

from goe_functions import (attribute, check, controls, data, duplicate,
                           flexiplane, joint, node, goe, goemath, rigs, tools)

reload(attribute)
reload(check)
reload(controls)
reload(data)
reload(duplicate)
reload(flexiplane)
reload(goe)
reload(goemath)
reload(joint)
reload(node)
reload(rigs)
reload(tools)


class BipedCartoonArmGuide(object):
    """ Create a biped arm guide setup """
    def __init__(self,
                 moduleName=None,
                 side=None,
                 size=1,
                 shape=30,
                 color=None,
                 mirror=False,
                 mirrorAxis='x',
                 asymmetry=False,
                 clavicle=True,
                 scapula=False):
        """
        @type  moduleName: string
        @param moduleName: specify the moduleName name which is the guides name

        @type  side: string
        @param side: specify the side. Valid sides are 'C', 'L', 'R'.

        @type  size: float
        @param size: specify the size of the guide control.

        @type  shape: string
        @param shape: specify the shape. Default shape is 30 the 3Dcross.

        @type  color: integer
        @param color: specify the color of the guide control shape.

        @type  mirror: bool
        @param mirror: turn on mirroring or not.

        @type  mirrorAxis: string
        @param mirrorAxis: valid axis are 'x', 'y', 'z'.

        @type  asymmetry: bool
        @param asymmetry: unlock selection of the right side when mirrored.

        @type  clavicle: bool
        @param clavicle: add clavicle guides

        @type  scapula: bool
        @param scapula: add scapula guides
        """

        #--- args
        self._moduleName = moduleName
        self._side = side
        self._size = size
        self._shape = shape
        self._color = color
        self._mirror = mirror
        self._mirrorAxis = mirrorAxis
        self._asymmetry = asymmetry
        self._clavicle = clavicle
        self._scapula = scapula

        #--- vars
        self.root = 'GUIDE_ROOT'
        self.mod = None
        self.position = list()
        self.rotation = list()

        self.controls = list()
        self.aims = list()
        self.clavicle_controls = list()
        self.scapula_controls = list()

        self.to_ihi = list()
        self.to_lock = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        """ Check the parameters of this rig class for validation """
        msg = "Please call SetupRoot(__file__) before creating guides!"
        assert cmds.objExists(self.root), check.error(self, 0, `self.root`, msg)

        #--- moduleName
        assert self._moduleName, check.error(self, 1, `self._moduleName`)
        assert isinstance(self._moduleName, str), check.error(self, 2, `self._moduleName`)

        #--- mirrorAxis
        assert (self._mirrorAxis == 'x' or self._mirrorAxis == 'y' or
                self._mirrorAxis == 'z'), check.error(self, 1, `self._mirrorAxis`)
    #END __check_parameters()

    def __prepare(self):
        """ Prepare colors, positions and rotations for the rig setup """
        #--- color
        if self._color is None:
            self._color = 17
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
        #--- position
        self.position = [[5, 0, 0], [5, 0, 0], [10, 0, 0], [15, 0, 0]]
        #--- rotation
        self.rotation = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    #END __prepare()

    def __setup_mod_group(self):
        """ Setup the module group of this rig setup """
        #--- mod grp
        side = self._side
        if self._mirror:
            side = 'C'
        self.mod = side + '_' + self._moduleName.upper() + '_MOD'
        if not cmds.objExists(self.mod):
            self.mod = cmds.createNode('transform', name=self.mod, parent=self.root)
            attribute.lock_all(self.mod)
        #--- add attributes
        if not cmds.objExists(self.mod + '.guideDATA'):
            cmds.addAttr(self.mod, longName="guideDATA", dataType='string')
    #END __setup_mod_group

    def __prepare_controls(self):
        """ Prepare the controls, setup and connect the curves for them """
        self.up_vector = None
        for i in range(4):
            #--- create the controls
            ctl = self.__create_control(self._side, self._moduleName, i,
                                        self._color, self.mod)
            self.controls.append(ctl)

            #--- create aim transforms for a proper setup
            name = self._side + '_' + self._moduleName + 'Aim' + repr(i)
            aim = node.transform(name=name, suffix='TRN', parent=ctl.transform)
            self.to_lock.append(aim)
            self.aims.append(aim)

            #--- create the mirrored guides
            if self._mirror:
                self.__mirror_guides(ctl.transform, i)
        #--- create control chain
        self.__setup_controls(self.controls)
        #--- connect controls by a curve
        self.__connect_via_curve(self.controls)

        #--- clavicle
        if self._clavicle:
            for i in range(2):
                #--- create the controls
                ctl = self.__create_control(self._side,
                                            self._moduleName + 'Clavicle', i,
                                            self._color, self.mod)
                self.clavicle_controls.append(ctl)
                #--- create the mirrored guides
                if self._mirror:
                    self.__mirror_guides(ctl.transform, i, addName='Clavicle')
            #--- create control chain
            self.__create_chain(self.clavicle_controls)
            #--- connect controls by a curve
            self.__connect_via_curve(self.clavicle_controls)

        #--- scapula
        if self._scapula:
            for i in range(2):
                #--- create the controls
                ctl = self.__create_control(self._side,
                                            self._moduleName + 'Scapula', i,
                                            self._color, self.mod)
                self.scapula_controls.append(ctl)
                #--- create the mirrored guides
                if self._mirror:
                    self.__mirror_guides(ctl.transform, i, addName='Scapula')
            #--- create control chain
            self.__create_chain(self.scapula_controls)
            #--- connect controls by a curve
            self.__connect_via_curve(self.scapula_controls)
    #END __prepare_controls()

    def __create_control(self, side, name, index, color, parent):
        """ Create the controls and add proper attributes """
        shape = self._shape
        orientation = 0
        if not index:
            shape = 0
            orientation = 16
        ctl = controls.Control(side=side, name=name + 'Guide' + repr(index),
                               shape=shape, size=self._size, color=color,
                               orientation=orientation,
                               position=self.position[index],
                               rotation=self.rotation[index], parent=parent)
        self.__add_control_attributes(ctl.transform, side, name, index)
        return ctl
    #END __create_control()

    def __add_control_attributes(self, control, side, name, index):
        """ Add control attributes properly """
        #--- side
        if not cmds.objExists(control + '.side'):
            cmds.addAttr(control, longName="side", dataType='string')
            cmds.setAttr(control + '.side', side, type='string', lock=True)
        #--- name
        if not cmds.objExists(control + '.name'):
            cmds.addAttr(control, longName="name", dataType='string')
            cmds.setAttr(control + '.name', name, type='string', lock=True)
        #--- index
        if not cmds.objExists(control + '.index'):
            cmds.addAttr(control, longName="index", dataType='string')
            cmds.setAttr(control + '.index', repr(index), type='string', lock=True)
        #--- guideID
        if not cmds.objExists(control + '.guideID'):
            cmds.addAttr(control, longName="guideID", dataType='string')
            cmds.setAttr(control + '.guideID', name + repr(index),
                         type='string', lock=True)
    #END __add_control_attributes()

    def __setup_controls(self, controls):
        """ Setup constraints and aims for the controls """
        goe.parent(controls[1].group, controls[0].transform)
        goe.parent(controls[-1].group, controls[0].transform)

        #--- create point and orientConstraint on the elbow control group
        pcn = node.pointConstraint(objA=[self.aims[0], controls[-1].transform],
                                   objB=controls[2].group,
                                   maintainOffset=False, lock=True)
        self.to_lock.append(pcn)
        ocn = node.orientConstraint(objA=self.aims[0],
                                    objB=controls[2].group,
                                    maintainOffset=False, lock=True)
        self.to_lock.append(ocn)

        #--- aim constraint the controls properly
        aima = node.aimConstraint(target=controls[2].transform,
                                  source=controls[-1].transform,
                                  aimVector=[-1, 0, 0], upVector=[0, 1, 0],
                                  skip='x')
        self.to_lock.append(aima)
        aimb = node.aimConstraint(target=self.aims[-1],
                                  source=controls[2].transform,
                                  aimVector=[1, 0, 0], upVector=[0, 1, 0],
                                  skip='x')
        self.to_lock.append(aimb)
        aimc = node.aimConstraint(target=self.controls[2].transform,
                                  source=controls[1].transform,
                                  aimVector=[1, 0, 0], upVector=[0, 1, 0],
                                  skip='x')
        self.to_lock.append(aimc)

        #--- lock attributes
        attribute.lock_attributes(controls[1].transform, ['t', 'r'])
        attribute.lock_attributes(controls[2].transform, ['ty', 'r'])
        attribute.lock_attributes(controls[-1].transform, ['ty', 'tz', 'r'])
    #END __setup_controls()

    def __create_chain(self, controls):
        """ Create a control chain """
        for i, ctl in enumerate(controls):
            j = i + 1
            if not j == len(controls):
                goe.parent(controls[j].group, ctl.transform)
    #END __create_chain()

    def __connect_via_curve(self, controls=None):
        """ Connect the controls by using a curve
        @type  controls: list
        @param controls: specify the controls list to be connected via curve
        """
        #--- create proper transform nodes and curves
        crv_grp = "CURVE_TMP"
        if not cmds.objExists(crv_grp):
            crv_grp = node.transform(name='CURVE', suffix='TMP', parent='GUIDE_ROOT')
        pos = [[i, 0, 0] for i in range(len(controls))]
        crv = cmds.curve(point=pos, degree=1)
        shp = cmds.listRelatives(crv, allDescendents=True)[0]
        cmds.parent(crv, crv_grp)

        #--- connect the curve controlPoints with the controls
        for j, i in enumerate(controls):
            dcm = node.decomposeMatrix()
            cmds.connectAttr(i.transform + '.worldMatrix', dcm + '.inputMatrix')
            cmds.connectAttr(dcm + '.outputTranslate',
                             crv + '.controlPoints[' + str(j) + ']')

        #--- set displayType of the curve to template
        cmds.setAttr(shp + '.overrideEnabled', 1)
        cmds.setAttr(shp + '.overrideColor', self._color)
        cmds.setAttr(crv + '.overrideEnabled', 1)
        cmds.setAttr(crv + '.overrideDisplayType', 2)
    #END __connect_via_curve()

    def __mirror_guides(self, obj, index, addName=""):
        """ Mirror the guides properly
        @type  obj: string
        @param obj: specify the object to be mirrored

        @type  index: bool
        @param index: specify the index of the control

        @type  addName: string
        @param addName: add an additional name to the mirrored control
        """
        #--- check and setup the side
        msg = "Please specify 'L' or 'R' as valid side!"
        assert not self._side == 'C', check.error(self, 1, str(self._side), msg)
        side = 'R'
        color = 13
        if self._side == 'R':
            side = 'L'
            color = 6

        #--- create mirror control
        name = self._moduleName + addName
        ctl = self.__create_control(side, name, index, color, self.mod)

        #--- add mirror attribute
        if not cmds.objExists(ctl.transform + '.MIRROR'):
            cmds.addAttr(ctl.transform, longName="MIRROR", attributeType='bool')
            cmds.setAttr(ctl.transform + '.MIRROR', 1, lock=True, keyable=False)
            if self._asymmetry:
                if not cmds.objExists(ctl.transform + '.ASYM'):
                    cmds.addAttr(ctl.transform, longName="ASYM", attributeType='bool')
                    cmds.setAttr(ctl.transform + '.ASYM', 1, lock=True, keyable=False)

        #--- create mirror setup
        name = side + "_" + self._moduleName + repr(index) + "_MIR"
        mir = cmds.createNode("goe_mirror", name=name)
        self.to_ihi.append(mir)

        #--- connect mirror setup
        cmds.connectAttr(obj + ".worldMatrix", mir + ".inputMatrix")
        cmds.connectAttr(mir + ".outTranslation", ctl.group + ".translate")
        cmds.connectAttr(mir + ".outRotation", ctl.group + ".rotate")

        #--- setup mirror attrs
        if self._mirrorAxis == 'x':
            cmds.setAttr(mir + '.mirrorAxis', 0, lock=True, keyable=False)
        elif self._mirrorAxis == 'y':
            cmds.setAttr(mir + '.mirrorAxis', 1, lock=True, keyable=False)
        elif self._mirrorAxis == 'z':
            cmds.setAttr(mir + '.mirrorAxis', 2, lock=True, keyable=False)
        cmds.setAttr(mir + '.mirror', 1, lock=True, keyable=False)
        cmds.setAttr(ctl.group + '.inheritsTransform', lock=False)
        cmds.setAttr(ctl.group + '.inheritsTransform', 0, lock=True)

        #--- global scale connection
        for axis in 'xyz':
            cmds.setAttr(ctl.group + '.s' + axis, lock=False, keyable=True)
        cmds.connectAttr(self.root + ".globalScale", ctl.group + ".sx")
        cmds.connectAttr(self.root + ".globalScale", ctl.group + ".sy")
        cmds.connectAttr(self.root + ".globalScale", ctl.group + ".sz")
        for axis in 'xyz':
            cmds.setAttr(ctl.group + '.s' + axis, lock=True, keyable=False)

        #--- change displayType to reference
        if not self._asymmetry:
            cmds.setAttr(ctl.shape + '.overrideEnabled', 1)
            cmds.setAttr(ctl.shape + '.overrideDisplayType', 2)
            for axis in 'xyz':
                cmds.setAttr(ctl.transform + '.t' + axis, lock=True, keyable=False)
                cmds.setAttr(ctl.transform + '.r' + axis, lock=True, keyable=False)
    #END __mirror_guides()

    def __cleanup(self):
        """ Cleanup the rig system """
        for i in self.to_ihi:
            cmds.setAttr(i + '.ihi', 0)
        for i in self.to_lock:
            cmds.setAttr(i + '.ihi', 0)
            attribute.lock_all(i)
    #END __cleanup()

    def __setup_data(self):
        """ Setup the guide data """
        data = dict()
        data['GUIDE'] = str(self.mod)
        data['GUIDETYPE'] = 'armCmds'
        data['moduleName'] = str(self._moduleName)
        data['side'] = str(self._side)
        data['size'] = float(self._size)
        data['shape'] = int(self._shape)
        data['color'] = int(self._color)
        data['mirror'] = bool(self._mirror)
        data['mirrorAxis'] = str(self._mirrorAxis)
        data['asymmetry'] = bool(self._asymmetry)
        if not cmds.getAttr(self.mod + '.guideDATA'):
            cmds.setAttr(self.mod + '.guideDATA', data, type='string', lock=True)
    #END __setup_data()

    def __create(self):
        """ Call the methods in the proper order """
        #--- check the parameters
        self.__check_parameters()
        #--- prepare parameters
        self.__prepare()
        #--- setup mod_group
        self.__setup_mod_group()
        #--- setup the controls
        self.__prepare_controls()
        #--- cleanup
        self.__cleanup()
        #--- setup data
        self.__setup_data()
    #END __create()
#END BipedCartoonArmGuide()


class BipedCartoonArmRig(rigs.RigCmds):
    """ Create a basic arm setup based on your specifications """
    def __init__(self,
                 side='C',
                 moduleName=None,
                 guides=[],
                 clavicleGuides=[],
                 scapulaGuides=[],
                 shape=14,
                 size=1,
                 color=None,
                 offsetGroups=0,
                 withGimbal=False,
                 rotateOrder='xyz',
                 mirrorAxis='x',
                 fk=True,
                 ik=True,
                 fkik='Blend',
                 addArmTwist=True,
                 addIkStretch=True,
                 addIkBend=True,
                 addSoftIk=True,
                 addSoftClavicle=True,
                 parentType=None,
                 DEBUG=True):
        """
        @type  assetType: string
        @param assetType: specify the character type (ie."HUMAN","FISH")

        @type  moduleName: string
        @param moduleName: specify the name of the module

        @type  side: string
        @param side: specify the side! (ie. 'C', 'L', 'R')

        @type  shape: integer
        @param shape: specify the number of the shape, default is 1

        @type  size: float
        @param size: specify the size of the control, default is 1

        @type  color: integer
        @param color: specify the number of the color, default is 17

        @type  guides: list
        @param guides: specify a list with the guideJoint names

        @type  offsetGroups: integer
        @param offsetGroups: specify the amount of control offsetGroups

        @type  withGimbal: bool
        @param withGimbal: specify if gimbal control shall be created

        @type  rotateOrder: string/integer
        @param rotateOrder: specify the rotateOrder as string or integer

        @type  mirrorAxis: string
        @param mirrorAxis: valid axis are 'x', 'y', 'z'

        @type  fk: bool
        @param fk: Specify if you want to have a fk system or not

        @type  ik: bool
        @param ik: Specify if you want to have an ik system or not

        @type  fkik: string
        @param fkik: Valid are 'blend', 'switch'

        @type  parentType: string
        @param parentType: Valid values are None, parent, constraint.
                           None = the controls will be parented under the
                                  mod groups
                           parent = the controls will be parented underthe
                                    mainGimbal control
                           constraint = the controls will be constraint to the
                                        mainGimbal control

        @type  DEBUG: bool
        @param DEBUG: Show all rig related setups, turn Off when finished
        """
        super(BipedCartoonArmRig, self).__init__()

        #--- args
        self._side = side
        self._shape = shape
        self._size = size
        self._color = color
        self._moduleName = moduleName
        self._guides = guides
        self._clavicleGuides = clavicleGuides
        self._scapulaGuides = scapulaGuides
        self._offsetGroups = offsetGroups
        self._withGimbal = withGimbal
        self._rotateOrder = rotateOrder
        self._mirrorAxis = mirrorAxis
        self._fk = fk
        self._ik = ik
        self._fkik = fkik
        self._addArmTwist = addArmTwist
        self._addIkStretch = addIkStretch
        self._addIkBend = addIkBend
        self._addSoftClavicle = addSoftClavicle
        self._parentType = parentType
        self.DEBUG = DEBUG

        #--- vars
        self.guides = list()

        self.mod_grp = None
        self.bind_grp = None
        self.fk_grp = None
        self.ik_grp = None

        self.joints = list()
        self.fk_joints = list()
        self.ik_joints = list()
        self.joint_pac = list()

        self.fk_controls = list()
        self.ik_controls = list()

        self.to_lock = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        """ Check the class parameters for validation """
        #--- check moduleName
        msg = "moduleName: Please specify a string"
        assert self._moduleName, msg
        assert isinstance(self._moduleName, str), msg

        #--- check side
        assert self._side, ("side: Please specify 'C', 'L' or 'R'!")

        #--- check guideJoints
        msg = "guideJoints: Please specify a list!"
        assert self._guides, msg
        assert isinstance(self._guides, list), msg

        #--- check rotateOrder
        msg = "rotateOrder: Please specify a valid string or an integer!"
        assert self._rotateOrder, msg

        #--- parent type
        if self._parentType == 'None':
            self._parentType = None
    #END __check_parameters()

    @property
    def __mirror_check(self):
        """ Check the scene if there is already a created rig for mirroring """
        check = False
        if self._side == 'C':
            return check

        mirror = 'R'
        if self._side == 'R':
            mirror = 'L'
        if cmds.objExists(mirror + '_' + self._moduleName + '_MOD'):
            check = True

        return check
    #END __mirror_check()

    def __prepare_guides(self):
        """ Check the scene, get the guides and prepare them for the rig """
        to_delete = list()
        for gid in self._guides:
            #--- list all the goe locators in the scene
            shapes = cmds.ls(type='goe_locator')
            if not shapes:
                continue
            for shp in shapes:
                #--- get the transform and group nodes of the guide shapes
                trn = cmds.listRelatives(shp, parent=True, type='transform')[0]
                grp = cmds.listRelatives(trn, parent=True, type='transform')[0]
                #--- check the guide control tags vor validation
                if not cmds.objExists(trn + '.guideID'):
                    continue
                if not cmds.getAttr(trn + '.side') == self._side:
                    continue
                if not cmds.getAttr(trn + '.guideID') == gid:
                    continue
                if not int(cmds.getAttr(trn + '.index')):
                    to_delete.append(grp)
                    continue
                #--- get the name, position and rotation of the guide
                nme = cmds.getAttr(trn + '.name')
                pos = cmds.xform(trn, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(trn, query=True, rotation=True, worldSpace=True)
                #--- check if we deal with a mirrored side and setup rotation
                if self.__mirror_check:
                    if self._mirrorAxis == 'x':
                        rot = [180 + rot[0], rot[1], rot[2]]
                    elif self._mirrorAxis == 'y':
                        rot = [rot[0], 180 + rot[1], rot[2]]
                    elif self._mirrorAxis == 'z':
                        rot = [rot[0], rot[1], 180 + rot[2]]
                #--- append the name, position and rotation to a guide list
                self.guides.append([nme, pos, rot])
                #--- list all the constraints of the groups and delete them
                cnt = cmds.listConnections(grp)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- list all the constraints of the controls and delete them
                cnt = cmds.listConnections(trn)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- add the guide group to the deletion list
                to_delete.append(grp)

        #--- delete the guides itself
        for d in to_delete:
            if cmds.objExists(d):
                cmds.delete(d)

        #--- setup the colors
        if not self._color:
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
            elif self._side == 'C':
                self._color = 17
    #END __prepare_guides()

    def __create_mod_group(self):
        """ Create the module groups for the rig setup """
        #--- create module group
        self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if self._moduleName:
            self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if not cmds.objExists(self.mod_grp):
            self.mod_grp = cmds.createNode('transform', name=self.mod_grp,
                                           parent=self.rig_grp)
        attribute.lock_all(self.mod_grp)

        #--- create bind joint group
        self.bind_grp = self._side + '_' + self._moduleName + 'BIND_MOD'
        if not cmds.objExists(self.bind_grp):
            self.bind_grp = cmds.createNode('transform', name=self.bind_grp,
                                            parent=self.mod_grp)
        attribute.lock_all(self.bind_grp)
    #END __create_mod_group()

    def __setup_mod_group(self):
        """ Setup the module group and att proper attributes """
        #--- showJoints
        if not cmds.objExists(self.mod_grp + '.showJoints'):
            cmds.addAttr(self.mod_grp, longName='showJoints',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showJoints', edit=True, channelBox=True)

        #--- showIkJoints
        if not cmds.objExists(self.mod_grp + '.showIkJoints'):
            cmds.addAttr(self.mod_grp, longName='showIkJoints',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showIkJoints', edit=True, channelBox=True)

        #--- showIkHandles
        if not cmds.objExists(self.mod_grp + '.showIkHandles'):
            cmds.addAttr(self.mod_grp, longName='showIkHandles',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showIkHandles', edit=True, channelBox=True)
    #END __setup_mod_group()

    def __prepare_joint_setup(self):
        """ Prepare, create and setup the joints """
        #--- create joints
        for num, i in enumerate(self.guides):
            cmds.select(clear=True)
            pos = i[1]
            rot = i[2]
            jnt = self.__create_joint_setup(num, pos, rot)
            self.joints.append(jnt)

        self.__create_joint_chain()
    #END __prepare_joint_setup()

    def __create_joint_setup(self, num=0, pos=[0, 0, 0], rot=[0, 0, 0]):
        """
        @type  name: string
        @param name: specify an additional name for the joints

        @type  num: int
        @param num: specify the index num

        @type  pos: list
        @param pos: specify the position values

        @type  rot: list
        @param rot: specify the rotation values
        """
        #--- create and reposition joints
        jnt_name = (self._side + '_' + self._moduleName + repr(num) + '_JNT')
        jnt = cmds.joint(name=jnt_name)
        cmds.xform(jnt, translation=pos, worldSpace=True)
        cmds.setAttr(jnt + '.r', 0, 0, 0)
        cmds.setAttr(jnt + '.jo', rot[0], rot[1], rot[2])

        #--- connect visibility of joints with main group
        cmds.connectAttr(self.mod_grp + '.showJoints', jnt + '.v')
        main = self.main_control.transform + '.globalScale'
        cmds.connectAttr(main, jnt + '.radius')

        #--- change draw style
        cmds.setAttr(jnt + '.drawStyle', 0)

        #--- reparent the joint under the bind group
        cmds.parent(jnt, self.bind_grp)
        return jnt
    #END __create_joint_setup()

    def __create_joint_chain(self):
        """ Create a joint chain """
        for i, jnt in enumerate(self.joints):
            j = i + 1
            if not j == len(self.joints):
                cmds.parent(self.joints[j], jnt)
    #END __create_joint_chain()

    def __fk_setup(self):
        """ Prepare the fk setup for this rig system """
        if not self._fk:
            return
        #--- create fk mod group
        self.__fk_mod_group()
        #--- create fk chain
        self.fk_joints = duplicate.Duplicate(self.joints[0], ['_JNT', 'FK_JNT'],
                                             self.fk_grp).result
        #--- create fk controls
        self.__fk_create_controls()
        #--- setup fk controls
        self.__fk_setup_controls()
    #END __fk_setup()

    def __fk_mod_group(self):
        """ Create the fk module group for the rig setup """
        self.fk_grp = self._side + '_' + self._moduleName + 'FK_MOD'
        if not cmds.objExists(self.fk_grp):
            self.fk_grp = cmds.createNode('transform', name=self.fk_grp,
                                          parent=self.mod_grp)
        attribute.lock_all(self.fk_grp)
    #END __fk_mod_group()

    def __fk_create_controls(self):
        """ Create the fk controls """
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            if not num:
                name = self._moduleName + 'ShoulderFK'
            elif num == 1:
                name = self._moduleName + 'ElbowFK'
            elif num == 2:
                name = self._moduleName + 'WristFK'
            ctl = controls.Control(side=self._side,
                                   name=name,
                                   shape=self._shape,
                                   size=self._size,
                                   color=self._color,
                                   position=pos,
                                   rotation=rot,
                                   withGimbal=self._withGimbal,
                                   rotateOrder=self._rotateOrder,
                                   offsetGroups=self._offsetGroups,
                                   parent=self.mod_grp)
            #--- append to fk list
            self.fk_controls.append(ctl)
    #END __fk_create_controls()

    def __fk_setup_controls(self):
        """ Parent the fk control shapes under the fk joints and rename them """
        for i, jnt in enumerate(self.fk_joints):
            cmds.parent(self.fk_controls[i].shape, jnt, relative=True, shape=True)
            cmds.delete(self.fk_controls[i].group)
            cmds.rename(jnt, self.fk_controls[i].transform)
        #--- overwrite the fk joints list by the fk controls' transform list
        self.fk_joints = [i.transform for i in self.fk_controls]
    #END __fk_setup_controls()

    def __ik_setup(self):
        """ Prepare the ik setup for this rig system """
        if not self._ik:
            return
        #--- create ik mod group
        self.__ik_mod_group()
        #--- create ik chain
        self.ik_joints = duplicate.Duplicate(self.joints[0], ['_JNT', 'IK_JNT'],
                                             self.ik_grp).result
        #--- create ik controls
        self.__ik_create_controls()
        #--- setup ik controls
        self.__ik_setup_handle()
        #--- ik display
        goe.connectAttr(self.mod_grp + '.showIkJoints', self.ik_joints[0] + '.v')
        goe.connectAttr(self.mod_grp + '.showIkHandles', self.ik_handle[0] + '.v')
    #END __ik_setup()

    def __ik_mod_group(self):
        """ Create the ik module group for the rig setup """
        self.ik_grp = self._side + '_' + self._moduleName + 'IK_MOD'
        if not cmds.objExists(self.ik_grp):
            self.ik_grp = cmds.createNode('transform', name=self.ik_grp,
                                          parent=self.mod_grp)
        attribute.lock_all(self.ik_grp)
    #END __ik_mod_group()

    def __ik_create_controls(self):
        """ Create the ik controls """
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            shape = 0
            if not num:
                name = self._moduleName + 'ShoulderIK'
            elif num == 1:
                name = self._moduleName + 'ElbowIK'
                shape = 30
            elif num == 2:
                name = self._moduleName + 'WristIK'
                shape = 14
            ctl = controls.Control(side=self._side, name=name, shape=shape,
                                   size=self._size, color=self._color,
                                   position=pos, rotation=rot,
                                   withGimbal=self._withGimbal,
                                   rotateOrder=self._rotateOrder,
                                   offsetGroups=self._offsetGroups,
                                   parent=self.mod_grp)
            #--- append to ik list
            self.ik_controls.append(ctl)
    #END __ik_create_controls()

    def __ik_setup_handle(self):
        """ Parent the ik control shapes under the ik joints and rename them """
        goe.parent(self.ik_joints[0], self.ik_controls[0].transform)
        self.ik_handle = tools.three_joint_ik(self.ik_joints,
                                              self.ik_controls[-1].transform,
                                              self.ik_controls[1].transform,
                                              self.ik_controls[1].group, 5)
    #END __ik_setup_controls()

    def __ik_setup_stretch(self):
        """ Create an ik squash and stretch setup """
        if not self._addIkStretch:
            return
        #--- create the ik joint stretch setup
        for jnt in self.ik_joints[:-1]:
            #--- add stretch attribute
            cmds.addAttr(jnt, longName='stretch', attributeType='float',
                         min=0.001, max=100.0, defaultValue=1.0)
            #--- create multiplyDivide nodes
            mlt_div = node.multiplyDivide(name=jnt.split('_JNT')[0] + 'StretchDiv',
                                          operation=2, input1X=1, lockAttr='input1X')
            mlt_pow = node.multiplyDivide(name=jnt.split('_JNT')[0] + 'StretchPow',
                                          operation=3, input2X=0.5, lockAttr='input2X')
            self.to_lock.append(mlt_div)
            self.to_lock.append(mlt_pow)
            #---  connect the utility nodes with the ik joints
            goe.connectAttr(jnt + '.stretch', mlt_div + '.input2X')
            goe.connectAttr(mlt_div + '.outputX', mlt_pow + '.input1X')
            goe.connectAttr(jnt + '.stretch', jnt + '.sx')
            for axis in 'yz':
                goe.connectAttr(mlt_pow + '.outputX', jnt + '.s' + axis)

        #--- add squash and stretch
        self.__ik_squash_stretch()
    #END __ik_setup_stretch()

    def __ik_squash_stretch(self):
        """ Create an ik squash and stretch setup for the ik system """
        ctl = self.ik_controls
        main = self.main_control.transform
        fkik = self.fkik_control.transform
        #--- get the full distance length
        distance = goemath.distance(self.ik_joints)

        #--- add stretchy attributes to the ikfk controls
        cmds.addAttr(fkik, longName='ikStretch', attributeType='float',
                     min=0.0, max=1.0, defaultValue=0.0)

        #--- create the utility nodes
        name = self._side + '_' + self._moduleName + 'IkStretch'
        namegs = self._side + '_' + self._moduleName + 'IkStretchGlobalScale'
        dib = node.distanceBetween(name=name, point1=ctl[-1].transform,
                                   point2=ctl[0].transform,
                                   inMatrix1=ctl[-1].transform,
                                   inMatrix2=ctl[0].transform)
        mds = node.multiplyDivide(name=namegs, input2X=distance, lockAttr='input2X')
        md = node.multiplyDivide(name=name, operation=2)
        cnd = node.condition(name=name, secondTerm=1, operation=3, lockAttr='secondTerm')
        blc = node.blendColors(name=name, color2R=1, lockAttr='color2R')
        for i in [dib, mds, md, cnd, blc]:
            self.to_lock.append(i)

        #--- connect the nodes properly
        goe.connectAttr(dib + '.distance', md + '.input1X')
        goe.connectAttr(main + '.scaleY', mds + '.input1X')
        goe.connectAttr(mds + '.outputX', md + '.input2X')
        goe.connectAttr(md + '.outputX', cnd + '.firstTerm')
        goe.connectAttr(md + '.outputX', cnd + '.colorIfTrueR')
        goe.connectAttr(cnd + '.outColorR', blc + '.color1R')
        goe.connectAttr(fkik + '.ikStretch', blc + '.blender')

        #--- connect the utility node to the joints
        for jnt in self.ik_joints[:-1]:
            goe.connectAttr(blc + '.outputR', jnt + '.stretch')
    #END __ik_squash_stretch()

    def __ik_bend(self):
        """ Setup the bendy ik functionality by using flexiplanes """
        if not self._addIkBend:
            return
        #--- create bend control
        self.ik_bend_control = controls.Control(side=self._side,
                                                name=self._moduleName + 'Bend',
                                                shape=14,
                                                size=self._size / 4,
                                                color=self._color,
                                                parent=self.ik_joints[1])
        goe.setAttr(self.ik_bend_control.group + '.t', 0, 0, 0)
        goe.setAttr(self.ik_bend_control.group + '.r', 0, 0, 0)
        goe.parent(self.ik_bend_control.group, self.mod_grp)
        #--- parentConstraint the bend control to the elbow joint
        pac = node.parentConstraint(objA=self.joints[1],
                                    objB=self.ik_bend_control.group,
                                    maintainOffset=False, lock=True)
        self.to_lock.append(pac)
        constto = [self.joints[0], self.ik_bend_control.transform]
        #--- create the first flexiplane for the humerus bone
        self.upper_arm_flp = flexiplane.FlexiPlane(side=self._side,
                                                   mod=self._moduleName,
                                                   name='upperArm',
                                                   color=self._color,
                                                   size=self._size - 0.5,
                                                   length=5,
                                                   constraintTo=constto,
                                                   constraintType='point',
                                                   follow=True,
                                                   parent=self.main_mod,
                                                   inheritsTransform=False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        goe.connectAttr(self.ik_bend_control.transform + '.rotateX',
                        self.upper_arm_flp.control_up.transform + '.rotateX')
        #--- parentConstraint the main control to the start joint of the humerus
        pac = node.parentConstraint(objA=self.joints[0],
                                    objB=self.upper_arm_flp.control_main.transform,
                                    maintainOffset=True, lock=True)
        self.to_lock.append(pac)
        constto = [self.ik_bend_control.transform, self.joints[-1]]
        #--- create the second flexiplane for the ulna radius bones
        self.lower_arm_flp = flexiplane.FlexiPlane(side=self._side,
                                                   mod=self._moduleName,
                                                   name='lowerArm',
                                                   color=self._color,
                                                   size=self._size - 0.5,
                                                   length=5,
                                                   constraintTo=constto,
                                                   constraintType='point',
                                                   follow=True,
                                                   parent=self.main_mod,
                                                   inheritsTransform=False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        goe.connectAttr(self.ik_bend_control.transform + '.rotateX',
                        self.lower_arm_flp.control_down.transform + '.rotateX')
        #--- parentConstraint the main control to the start joint of the elbow
        pac = node.parentConstraint(objA=self.joints[1],
                                    objB=self.lower_arm_flp.control_main.transform,
                                    maintainOffset=True, lock=True)
        self.to_lock.append(pac)
        #--- connect the globalScale attr of the flexiplane with the main ctl one
        #--- upper flexiPlane
        goe.connectAttr(self.main_control.transform + '.globalScale',
                        self.upper_arm_flp.control_main.transform + '.globalScale')
        #--- lower flexiPlane
        goe.connectAttr(self.main_control.transform + '.globalScale',
                        self.lower_arm_flp.control_main.transform + '.globalScale')
    #END __ik_bend()

    def __ik_arm_twist(self):
        """ Setup the ik twist based on the flexiplane """
        #--- check if a flexiplane exists
        if self._addArmTwist:
            if not self._addIkBend:
                #--- create the second flexiplane for the lowerArm
                twist = flexiplane.FlexiPlane(mod=self._moduleName,
                                              side=self._side, name='lowerArm',
                                              color=self._color,
                                              size=self._size - 0.5, length=5,
                                              constraintTo=[self.joints[-2],
                                                            self.joints[-1]],
                                              constraintType='point', follow=True,
                                              parent=self.mod_grp, hideControls=True)
                #--- parentConstraint the main control to the start joint of the elbow
                pac = node.parentConstraint(objA=self.joints[1],
                                            objB=twist.control_main.transform,
                                            maintainOffset=True, lock=True)
                self.to_lock.append(pac)
                #--- lock and hide the mid control of the flexiplane
                attribute.lock_all(twist.control_mid.transform)
                attribute.hide(twist.control_mid.transform)
                #--- connect the rotate control with the lowerArm rx
                goe.connectAttr(self.ik_controls[-1].transform + '.rx',
                                twist.control_up.transform + '.rx')
            else:
                #--- connect the rotate control with the lowerArm rx
                goe.connectAttr(self.ik_controls[-1].transform + '.rx',
                                self.lower_arm_flp.control_up.transform + '.rx')
        else:
            if self._addIkBend:
                #--- lock and hide the controls of the flexiplane
                attribute.lock_all(self.upper_arm_flp.control_mid.transform)
                attribute.lock_all(self.upper_arm_flp.control_up.transform)
                attribute.lock_all(self.upper_arm_flp.control_down.transform)

                attribute.lock_all(self.lower_arm_flp.control_mid.transform)
                attribute.lock_all(self.lower_arm_flp.control_up.transform)
                attribute.lock_all(self.lower_arm_flp.control_down.transform)

                attribute.hide(self.upper_arm_flp.control_mid.transform)
                attribute.hide(self.upper_arm_flp.control_up.transform)
                attribute.hide(self.upper_arm_flp.control_down.transform)

                attribute.hide(self.lower_arm_flp.control_mid.transform)
                attribute.hide(self.lower_arm_flp.control_up.transform)
                attribute.hide(self.lower_arm_flp.control_down.transform)

                #--- connect the rotate control with the lowerArm rx
                goe.connectAttr(self.ik_controls[-1].transform + '.rx',
                                self.lower_arm_flp.control_up.transform + '.rx')
    #END __ik_arm_twist()

    def __fkik_constraint_joints(self):
        """ Constraint the bind joints to the fk and ik joints """
        #--- fk and ik
        if self._fk and self._ik:
            for i, jnt in enumerate(self.joints):
                pac = node.parentConstraint(objA=[self.fk_joints[i], self.ik_joints[i]],
                                            objB=jnt, maintainOffset=False, lock=True)
                self.joint_pac.append(pac)
                self.to_lock.append(pac)
        #--- fk only
        elif self._fk and not self._ik:
            for i, jnt in enumerate(self.joints):
                pac = node.parentConstraint(objA=self.fk_joints[i], objB=jnt,
                                            maintainOffset=False, lock=True)
                self.joint_pac.append(pac)
                self.to_lock.append(pac)
        #--- ik only
        elif self._ik and not self._fk:
            for i, jnt in enumerate(self.joints):
                pac = node.parentConstraint(objA=self.ik_joints[i], objB=jnt,
                                            maintainOffset=False, lock=True)
                self.joint_pac.append(pac)
                self.to_lock.append(pac)
    #END __fkik_constraint_joints()

    def __fkik_setup(self):
        """ Create an fkik blend or fkik switch """
        if not (self._fk or self._ik):
            return
        offset = [0, 0, -3]
        if self.__mirror_check:
            offset = [0, 0, 3]
        #--- create a fkik control
        name = self._moduleName + 'FKIK'
        self.fkik_control = controls.Control(side=self._side,
                                             name=name,
                                             shape=30,
                                             size=self._size / 2,
                                             color=self._color,
                                             shapeOffset=offset,
                                             lockAttrs={'transform': ['t', 'r']},
                                             parent=self.joints[-1])
        goe.setAttr(self.fkik_control.group + '.t', 0, 0, 0)
        goe.setAttr(self.fkik_control.group + '.r', 0, 0, 0)

        #--- fkik blend or switch
        if self._fkik == 'Blend':
            self.__fkik_blend_switch('float')
        elif self._fkik == 'Switch':
            self.__fkik_blend_switch('short')

        #--- display setup
        self.__fkik_display_setup()
    #END __fkik_setup()

    def __fkik_blend_switch(self, attrType='float'):
        """ Blend or switch setup for fkik attribute
        @type  attrType: string
        @param attrType: valid is 'float' or 'short'
        """
        #--- add fkik blend attribute
        if not cmds.objExists(self.fkik_control.transform + '.fkik'):
            cmds.addAttr(self.fkik_control.transform, longName='fkik',
                         attributeType=attrType, min=0, max=1,
                         defaultValue=1.0, keyable=True)
        #--- create node
        name = self._side + '_' + self._moduleName + 'FKIK'
        rev = node.reverse(name)
        self.to_lock.append(rev)
        #--- connect attributes
        for pac, axis in zip(self.joint_pac, 'XYZ'):
            value = cmds.listAttr(pac, userDefined=True)
            cmds.connectAttr(self.fkik_control.transform + '.fkik', pac + '.' + value[1])
            cmds.connectAttr(self.fkik_control.transform + '.fkik', rev + '.input' + axis)
            cmds.connectAttr(rev + '.output' + axis, pac + '.' + value[0])
    #END __fkik_blend_switch()

    def __fkik_display_setup(self):
        """ Setup the display between fk and ik controls """
        #--- create nodes
        name = self._side + '_' + self._moduleName + 'DisplayFKIK'
        rev = node.reverse(name)
        self.to_lock.append(rev)
        goe.connectAttr(self.fkik_control.transform + '.fkik', rev + '.inputX')
        for i in self.fk_controls:
            goe.connectAttr(rev + '.outputX', i.transform + '.v')
        for i in self.ik_controls:
            goe.connectAttr(self.fkik_control.transform + '.fkik', i.transform + '.v')
    #END __fkik_display_setup()

    def __clavicle(self):
        """ Call clavicle class """
        if not self._clavicleGuides:
            return
        self.clavicle = BipedCartoonClavicleRig(side=self._side,
                                                moduleName=self._moduleName + 'Clavicle',
                                                guides=self._clavicleGuides,
                                                autoClaviclePos=[self.guides[0][1],
                                                                 self.guides[-1][1]],
                                                addSoftClavicle=self._addSoftClavicle)

        goe.connectAttr(self.fkik_control.transform + '.fkik',
                        self.clavicle.mlt_ikfk + '.input2X')
    #END __clavicle()

    def __scapula(self):
        """ Call scapula class """
        if not self._scapulaGuides or not self._clavicleGuides:
            return
        self.scapula = BipedCartoonScapulaRig(side=self._side,
                                              moduleName=self._moduleName + 'Scapula',
                                              guides=self._scapulaGuides,
                                              autoScapulaPos=self.clavicle.joints)
    #END __scapula()

    def __parent_setup(self, controls=None):
        """ Parent the given controls by the specified parent method
        @type  controls: string
        @param controls: valid is 'float' or 'short'
        """
        if not controls:
            return
        if not self._parentType:
            return
        if self._parentType == 'parent':
            #--- parent
            for ctl in controls:
                goe.parent(ctl.group, self.main_control.gimbal)
        elif self._parentType == 'constraint':
            #--- constraint
            for ctl in controls:
                node.parentConstraint(self.main_control.gimbal, ctl.group)
                for axis in 'xyz':
                    cmds.setAttr(ctl.group + '.s' + axis, lock=False)
                    cmds.connectAttr(self.main_control.transform + '.globalScale',
                                     ctl.group + '.s' + axis)
                    cmds.setAttr(ctl.group + '.s' + axis, lock=True)
    #END __parent_setup()

    def __cleanup(self):
        """ Cleanup, delete nodes and lock attributes """
        if self._moduleName:
            guideGrp = self._moduleName.upper() + 'GUIDE'
            if cmds.objExists(guideGrp):
                cmds.delete(guideGrp)
            else:
                if self._guides:
                    for i in self._guides:
                        if cmds.objExists(i):
                            cmds.delete(i)
            guideTrn = self._side + '_' + self._moduleName + 'Guide_TRN'
            if cmds.objExists(guideTrn):
                cmds.delete(guideTrn)

        guideRoot = 'GUIDE_ROOT'
        if cmds.objExists(guideRoot):
            if not cmds.listRelatives(guideRoot, children=True):
                cmds.delete(guideRoot)
            elif not cmds.listRelatives(guideRoot, allDescendents=True,
                                        type='goe_locator'):
                cmds.delete(guideRoot)

        if self.DEBUG:
            return

        #--- set the display to OFF
        cmds.setAttr(self.mod_grp + '.showJoints', 0)
        cmds.setAttr(self.mod_grp + '.showIkHandles', 0)

        #--- cleanup the constraints
        pac = cmds.ls(type='parentConstraint')
        pcn = cmds.ls(type='pointConstraint')
        ocn = cmds.ls(type='orientConstraint')
        scn = cmds.ls(type='scaleConstraint')
        constraints = [pac, pcn, ocn, scn]
        for const in constraints:
            for i in const:
                if not i:
                    continue
                cmds.setAttr(i + '.ihi', 0)
                attribute.lock_all(i)

        #--- cleanup joints
        for jnt in self.joints:
            cmds.setAttr(jnt + '.ihi', 0)

        #--- hide joints
        for i, obj in enumerate(self.joints):
            for axis in 'xyz':
                cmds.setAttr(obj + '.t' + axis, keyable=False, lock=True)
                cmds.setAttr(obj + '.r' + axis, keyable=False, lock=False)
                cmds.setAttr(obj + '.s' + axis, keyable=False, lock=True)
            cmds.setAttr(obj + '.v', keyable=False, lock=True)
            cmds.setAttr(obj + '.radi', keyable=False, channelBox=False)
            cmds.setAttr(obj + '.drawStyle', 0)

        #--- lock all attributes in the to_lock list
        for i in self.to_lock:
            cmds.setAttr(i + '.ihi', 0)
            attribute.lock_all(i)
    #END __cleanup()

    def __create(self):
        """ Call the methods in the proper order """
        #--- check parameters
        self.__check_parameters()

        #--- prepare guides
        self.__prepare_guides()

        #--- create mod group
        self.__create_mod_group()

        #--- setup mod group
        self.__setup_mod_group()

        #--- create joints
        self.__prepare_joint_setup()

        #--- fk setup
        self.__fk_setup()

        #--- ik setup
        self.__ik_setup()

        #--- constraint joints
        self.__fkik_constraint_joints()

        #--- setup fk ik
        self.__fkik_setup()

        #--- setup ik stretch
        self.__ik_setup_stretch()

        #--- setup ik bend
        self.__ik_bend()

        #--- setup arm twist
        self.__ik_arm_twist()

        #--- clavicle
        self.__clavicle()

        #--- scapula
        self.__scapula()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END BipedCartoonArmRig()


class BipedCartoonClavicleRig(rigs.RigCmds):
    """ Create a basic arm setup based on your specifications """
    def __init__(self,
                 side='C',
                 moduleName=None,
                 guides=[],
                 shape=14,
                 size=1,
                 color=None,
                 rotateOrder='xyz',
                 mirrorAxis='x',
                 autoClaviclePos=[[0, 0, 0], [5, 0, 0]],
                 addSoftClavicle=True,
                 DEBUG=True):
        """
        @type  assetType: string
        @param assetType: specify the character type (ie."HUMAN","FISH")

        @type  moduleName: string
        @param moduleName: specify the name of the module

        @type  side: string
        @param side: specify the side! (ie. 'C', 'L', 'R')

        @type  shape: integer
        @param shape: specify the number of the shape, default is 1

        @type  size: float
        @param size: specify the size of the control, default is 1

        @type  color: integer
        @param color: specify the number of the color, default is 17

        @type  guides: list
        @param guides: specify a list with the guideJoint names

        @type  offsetGroups: integer
        @param offsetGroups: specify the amount of control offsetGroups

        @type  rotateOrder: string/integer
        @param rotateOrder: specify the rotateOrder as string or integer

        @type  mirrorAxis: string
        @param mirrorAxis: valid axis are 'x', 'y', 'z'

        @type  DEBUG: bool
        @param DEBUG: Show all rig related setups, turn Off when finished
        """
        super(BipedCartoonClavicleRig, self).__init__()

        #--- args
        self._side = side
        self._shape = shape
        self._size = size
        self._color = color
        self._moduleName = moduleName
        self._guides = guides
        self._rotateOrder = rotateOrder
        self._mirrorAxis = mirrorAxis
        self._autoClaviclePos = autoClaviclePos
        self._addSoftClavicle = addSoftClavicle
        self.DEBUG = DEBUG

        #--- vars
        self.guides = list()

        self.mod_grp = None
        self.bind_grp = None
        self.fk_grp = None
        self.ik_grp = None

        self.joints = list()
        self.joint_pac = list()

        self.fk_controls = list()

        self.to_lock = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        """ Check the class parameters for validation """
        #--- check moduleName
        msg = "moduleName: Please specify a string"
        assert self._moduleName, msg
        assert isinstance(self._moduleName, str), msg

        #--- check side
        assert self._side, ("side: Please specify 'C', 'L' or 'R'!")

        #--- check guideJoints
        msg = "guideJoints: Please specify a list!"
        assert self._guides, msg
        assert isinstance(self._guides, list), msg

        #--- check rotateOrder
        msg = "rotateOrder: Please specify a valid string or an integer!"
        assert self._rotateOrder, msg
    #END __check_parameters()

    @property
    def __mirror_check(self):
        """ Check the scene if there is already a created rig for mirroring """
        check = False
        if self._side == 'C':
            return check

        mirror = 'R'
        if self._side == 'R':
            mirror = 'L'
        if cmds.objExists(mirror + '_' + self._moduleName + '_MOD'):
            check = True

        return check
    #END __mirror_check()

    def __prepare_guides(self):
        """ Check the scene, get the guides and prepare them for the rig """
        to_delete = list()
        for gid in self._guides:
            #--- list all the goe locators in the scene
            shapes = cmds.ls(type='goe_locator')
            if not shapes:
                continue
            for shp in shapes:
                #--- get the transform and group nodes of the guide shapes
                trn = cmds.listRelatives(shp, parent=True, type='transform')[0]
                grp = cmds.listRelatives(trn, parent=True, type='transform')[0]
                #--- check the guide control tags vor validation
                if not cmds.objExists(trn + '.guideID'):
                    continue
                if not cmds.getAttr(trn + '.side') == self._side:
                    continue
                if not cmds.getAttr(trn + '.guideID') == gid:
                    continue
                #--- get the name, position and rotation of the guide
                nme = cmds.getAttr(trn + '.name')
                pos = cmds.xform(trn, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(trn, query=True, rotation=True, worldSpace=True)
                #--- check if we deal with a mirrored side and setup rotation
                if self.__mirror_check:
                    if self._mirrorAxis == 'x':
                        rot = [180 + rot[0], rot[1], rot[2]]
                    elif self._mirrorAxis == 'y':
                        rot = [rot[0], 180 + rot[1], rot[2]]
                    elif self._mirrorAxis == 'z':
                        rot = [rot[0], rot[1], 180 + rot[2]]
                #--- append the name, position and rotation to a guide list
                self.guides.append([nme, pos, rot])
                #--- list all the constraints of the groups and delete them
                cnt = cmds.listConnections(grp)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- list all the constraints of the controls and delete them
                cnt = cmds.listConnections(trn)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- add the guide group to the deletion list
                to_delete.append(grp)

        #--- delete the guides itself
        for d in to_delete:
            if cmds.objExists(d):
                cmds.delete(d)

        #--- setup the colors
        if not self._color:
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
            elif self._side == 'C':
                self._color = 17
    #END __prepare_guides()

    def __create_mod_group(self):
        """ Create the module groups for the rig setup """
        #--- create module group
        self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if self._moduleName:
            self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if not cmds.objExists(self.mod_grp):
            self.mod_grp = cmds.createNode('transform', name=self.mod_grp,
                                           parent=self.rig_grp)
        attribute.lock_all(self.mod_grp)

        #--- create bind joint group
        self.bind_grp = self._side + '_' + self._moduleName + 'BIND_MOD'
        if not cmds.objExists(self.bind_grp):
            self.bind_grp = cmds.createNode('transform', name=self.bind_grp,
                                            parent=self.mod_grp)
        attribute.lock_all(self.bind_grp)
    #END __create_mod_group()

    def __setup_mod_group(self):
        """ Setup the module group and att proper attributes """
        #--- showJoints
        if not cmds.objExists(self.mod_grp + '.showJoints'):
            cmds.addAttr(self.mod_grp, longName='showJoints',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showJoints', edit=True, channelBox=True)

        #--- showIkHandles
        if not cmds.objExists(self.mod_grp + '.showIkHandles'):
            cmds.addAttr(self.mod_grp, longName='showIkHandles',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showIkHandles', edit=True, channelBox=True)
    #END __setup_mod_group()

    def __prepare_joint_setup(self):
        """ Prepare, create and setup the joints """
        #--- create joints
        for num, i in enumerate(self.guides):
            cmds.select(clear=True)
            pos = i[1]
            rot = i[2]
            jnt = self.__create_joint_setup(num, pos, rot)
            self.joints.append(jnt)

        self.__create_joint_chain()
    #END __prepare_joint_setup()

    def __create_joint_setup(self, num=0, pos=[0, 0, 0], rot=[0, 0, 0]):
        """
        @type  name: string
        @param name: specify an additional name for the joints

        @type  num: int
        @param num: specify the index num

        @type  pos: list
        @param pos: specify the position values

        @type  rot: list
        @param rot: specify the rotation values
        """
        #--- create and reposition joints
        jnt_name = (self._side + '_' + self._moduleName + repr(num) + '_JNT')
        jnt = cmds.joint(name=jnt_name)
        cmds.xform(jnt, translation=pos, worldSpace=True)
        cmds.setAttr(jnt + '.r', 0, 0, 0)
        cmds.setAttr(jnt + '.jo', rot[0], rot[1], rot[2])

        #--- connect visibility of joints with main group
        cmds.connectAttr(self.mod_grp + '.showJoints', jnt + '.v')
        main = self.main_control.transform + '.globalScale'
        cmds.connectAttr(main, jnt + '.radius')

        #--- change draw style
        cmds.setAttr(jnt + '.drawStyle', 0)

        #--- reparent the joint under the bind group
        cmds.parent(jnt, self.bind_grp)
        return jnt
    #END __create_joint_setup()

    def __create_joint_chain(self):
        """ Create a joint chain """
        for i, jnt in enumerate(self.joints):
            j = i + 1
            if not j == len(self.joints):
                cmds.parent(self.joints[j], jnt)
    #END __create_joint_chain()

    def __fk_setup(self):
        """ Prepare the fk setup for this rig system """
        #--- create fk controls
        self.__fk_create_controls()
        #--- setup fk controls
        self.__fk_setup_controls()
    #END __fk_setup()

    def __fk_create_controls(self):
        """ Create the fk controls """
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            if not num:
                name = self._moduleName + 'Sternal'
            elif num == 1:
                name = self._moduleName + 'Acromial'
            ctl = controls.Control(side=self._side,
                                   name=name,
                                   shape=self._shape,
                                   size=self._size,
                                   color=self._color,
                                   position=pos,
                                   rotation=rot,
                                   rotateOrder=self._rotateOrder,
                                   parent=self.mod_grp)
            #--- append to fk list
            self.fk_controls.append(ctl)
    #END __fk_create_controls()

    def __fk_setup_controls(self):
        """ Parent the fk control shapes under the fk joints and rename them """
        for i, jnt in enumerate(self.joints):
            cmds.parent(self.fk_controls[i].shape, jnt, relative=True, shape=True)
            cmds.delete(self.fk_controls[i].group)
            cmds.rename(jnt, self.fk_controls[i].transform)
        #--- overwrite the fk joints list by the fk controls' transform list
        self.joints = [i.transform for i in self.fk_controls]
    #END __fk_setup_controls()

    def __prepare_clavicle_setup(self):
        """ Prepare attributes for the autoClavicle """
        #--- add autoClavicle attributes
        print self.fk_controls
        cmds.addAttr(self.fk_controls[0].transform, longName='autoClavicle',
                     attributeType='float', min=0, max=1, defaultValue=1, keyable=True)
        #--- lock unnecessary attributes on the clavicle control
        attribute.lock_attributes(self.fk_controls[0].transform, ['t', 's', 'v'])

        self.__auto_clavicle_setup()
        self.__soft_clavicle_setup()
    #END __prepare_clavicle_setup()

    def __auto_clavicle_setup(self):
        """ Setup the autoClavicle """
        #--- connect the clavicle with the arm
        node.pointConstraint(objA=self.joints[-1],
                             objB=self._side + "_armShoulderFK_CTL",
                             maintainOffset=True, lock=True)
        #--- connect the clavicle with the arm
        node.pointConstraint(objA=self.joints[-1],
                             objB=self._side + "_armShoulderIK_GRP",
                             maintainOffset=True, lock=True)
        cmds.select(clear=True)

        #--- create the autoClavicle joint setup
        ls = [self._moduleName + 'AutoClavStart', self._moduleName + 'AutoClavEnd']
        auto_clav_joints = joint.IkChain(side=self._side, name=ls,
                                         position=[self.guides[0][1],
                                                   self._autoClaviclePos[1]],
                                         orientation=[[0.0, 0.0, 0.0],
                                                      [0.0, 0.0, 0.0]],
                                         parentJoint=self.mod_grp,
                                         parentIk=self.mod_grp,
                                         mirror=False)

        #--- AUTOCLAVICLE SETUP
        self.joints_ac = auto_clav_joints.joint_names
        self.ik_handle_ac = auto_clav_joints.ik_handle_names
        #--- create the poleVector setup
        nme = self._side + '_' + self._moduleName + 'AutoClavPoleVector'
        self.pole_vector = node.locator(name=nme, parent=self.joints_ac[-1])
        cmds.parent(self.pole_vector, self.mod_grp)
        #--- create poleVectorConstraint
        node.poleVectorConstraint(objA=self.pole_vector, objB=self.ik_handle_ac[0])
        #--- pointConstraint the locator to the ik control
        node.pointConstraint(objA=self._side + "_armWristIK_CTL",
                             objB=self.pole_vector, maintainOffset=False, lock=True)

        #--- pointConstraint the ikHandle to the ik control
        node.pointConstraint(objA=self._side + "_armWristIK_CTL",
                             objB=self.ik_handle_ac[0], maintainOffset=False, lock=True)

        #--- SETUP rotation automation of the clavicle
        #--- create a rotation group above the clavicle control
        nme = self.fk_controls[0].transform.split('_CTL')[0] + '_SDK'
        rot_grp = cmds.group(self.fk_controls[0].transform, name=nme)
        #--- set the group pivot to the controls pivot
        cmds.xform(rot_grp, pivots=self.guides[0][1], worldSpace=True)

        #--- limit rotations of this SDK group
        cmds.transformLimits(rot_grp, enableRotationX=(1, 1), enableRotationY=(1, 0),
                             enableRotationZ=(1, 0), rotationX=(-20, 20),
                             rotationY=(-50, 45), rotationZ=(0, 45))

        #--- create nodes for the automation setup
        mlt = node.multiplyDivide(name=self._side + '_' + self._moduleName + 'AutoClavRot',
                                  input2X=0.9, input2Y=0.9, input2Z=0.5)
        blc = node.blendColors(name=self._side + '_' + self._moduleName + 'AutoClavEnable',
                               color2R=0, color2G=0, color2B=0,
                               lockAttr=['color2R', 'color2G', 'color2B'])
        mlt_ikfk = node.multiplyDivide(name=self._side + '_' + self._moduleName + 'AutoClavIkFk',
                                       input1X=1.0, lockAttr='input1X')
        if self.__mirror_check:
            goe.setAttr(mlt_ikfk + '.input1X', -1.0)
        blc_ikfk = node.blendColors(name=self._side + '_' + self._moduleName + 'AutoClavIkFk',
                                    color2R=0, color2G=0, color2B=0,
                                    lockAttr=['color2R', 'color2G', 'color2B'])
        #--- connect attributes for the automation
        goe.connectAttr(self.joints_ac[0] + '.rotate', mlt + '.input1')
        goe.connectAttr(mlt + '.output', blc + '.color1')
        goe.connectAttr(blc + '.output', rot_grp + '.rotate')
        #--- connect the clavicle controls attributes
#         goe.connectAttr(self.ikfk_blenode.transform + '.fkIk', mlt_ikfk + '.input2X')
        goe.connectAttr(mlt_ikfk + '.outputX', blc_ikfk + '.blender')
        goe.connectAttr(self.fk_controls[0].transform + '.autoClavicle',
                        blc_ikfk + '.color1R')
        goe.connectAttr(blc_ikfk + '.outputR', blc + '.blender')
        self.mlt = mlt
        self.mlt_ikfk = mlt_ikfk
        self.sdk = rot_grp
    #END __auto_clavicle_setup()

    def __soft_clavicle_setup(self):
        """ Prepare the soft clavicle system """
        if not self._addSoftClavicle:
            return
        cmds.addAttr(self.fk_controls[0].transform, longName='softness',
                     attributeType='float', min=1, defaultValue=10, keyable=True)
        cmds.addAttr(self.fk_controls[0].transform, longName='smoothRotateY',
                     attributeType='float', min=0, max=1, defaultValue=0.5)
        cmds.addAttr(self.fk_controls[0].transform, longName='smoothRotateZ',
                     attributeType='float', min=0, max=1, defaultValue=0.5)

        #--- create softClavicle groups
        self.soft_grp = node.transform(name=self._side + '_' + self._moduleName + 'SoftSetup',
                                       suffix='GRP', parent=self.mod_grp)

        #--- LOCATORS
        #--- translate Y
        self.ty_loc = node.locator(name=self._side + '_' + self._moduleName + 'SoftTY',
                                   suffix='LOC', position=[1, 0, 0],
                                   worldSpace=True, parent=self.soft_grp)
        #--- translate Y Target
        self.tyIk_loc = node.locator(name=self._side + '_' + self._moduleName + 'SoftIkTY',
                                     suffix='LOC', position=[1, 0, 0],
                                     worldSpace=True, parent=self.soft_grp)
        #--- translate Z
        self.tz_loc = node.locator(name=self._side + '_' + self._moduleName + 'SoftTZ',
                                   suffix='LOC', position=[1, 0, 0],
                                   worldSpace=True, parent=self.soft_grp)
        #--- translate Z Target
        self.tzIk_loc = node.locator(name=self._side + '_' + self._moduleName + 'SoftIkTZ',
                                     suffix='LOC', position=[1, 0, 0],
                                     worldSpace=True, parent=self.soft_grp)

        #--- UTILITY NODES
        #--- multiplyDivide translation
        nme = self._side + '_' + self._moduleName + 'SoftTranslate'
        self.translate_mlt = node.multiplyDivide(name=nme, input2Y=0.005, input2Z=0.005,
                                                 lockAttr=['input2Y', 'input2Z'])
        #--- condition ty and tz
        self.ty_cnd = node.condition(name=self._side + '_' + self._moduleName + 'SoftTY',
                                     secondTerm=0, operation=2, lockAttr='secondTerm')
        self.tz_cnd = node.condition(name=self._side + '_' + self._moduleName + 'SoftTZ',
                                     secondTerm=0, operation=4, lockAttr='secondTerm')
        #--- remapValue ty and tz
        self.ty_rmv = node.remapValue(name=self._side + '_' + self._moduleName + 'SoftTY',
                                      inputMin=-1, inputMax=2, outputMin=0,
                                      lockAttr=['inputMin', 'inputMax', 'outputMin'])
        self.tz_rmv = node.remapValue(name=self._side + '_' + self._moduleName + 'SoftTZ',
                                      inputMin=-2, inputMax=1, outputMin=0,
                                      lockAttr=['inputMin', 'inputMax', 'outputMin'])
        #--- connect the utility nodes
        #--- translateY
        goe.connectAttr(self.ty_loc + '.ty', self.translate_mlt + '.input1Y')
        goe.connectAttr(self.translate_mlt + '.outputY', self.ty_cnd + '.colorIfFalseG')
        goe.connectAttr(self.ty_loc + '.ty', self.ty_cnd + '.firstTerm')
        goe.connectAttr(self.ty_loc + '.ty', self.ty_cnd + '.colorIfTrueG')
        goe.connectAttr(self.ty_cnd + '.outColorG', self.ty_rmv + '.inputValue')
        goe.connectAttr(self.ty_loc + '.ty', self.ty_rmv + '.outputMax')
        goe.connectAttr(self.ty_rmv + '.outValue', self.tyIk_loc + '.ty')
        #--- translateZ
        goe.connectAttr(self.tz_loc + '.tz', self.translate_mlt + '.input1Z')
        goe.connectAttr(self.translate_mlt + '.outputZ', self.tz_cnd + '.colorIfFalseB')
        goe.connectAttr(self.tz_loc + '.translateZ', self.tz_cnd + '.firstTerm')
        goe.connectAttr(self.tz_loc + '.translateZ', self.tz_cnd + '.colorIfTrueB')
        goe.connectAttr(self.tz_cnd + '.outColorG', self.tz_rmv + '.inputValue')
        goe.connectAttr(self.tz_loc + '.translateZ', self.tz_rmv + '.outputMax')
        goe.connectAttr(self.tz_rmv + '.outValue', self.tzIk_loc + '.translateZ')
        #--- smoothRotate to value[1].float_Value
        goe.connectAttr(self.fk_controls[0].transform + '.smoothRotateZ',
                        self.ty_rmv + '.value[1].value_FloatValue')
        goe.connectAttr(self.fk_controls[0].transform + '.smoothRotateY',
                        self.tz_rmv + '.value[1].value_FloatValue')

        #--- CREATE JOINT CHAIN
        #--- create the rotationY setup
        self.soft_ry_jnt = joint.IkChain(side=self._side,
                                         name=[self._moduleName + 'SoftRotY1',
                                               self._moduleName + 'SoftRotY2'],
                                         suffix='JNT',
                                         position=[[0, 0, 0], [1, 0, 0]],
                                         orientation=[[0, 0, 0], [0, 0, 0]],
                                         ikSolver='ikSCSolver',
                                         mirror=False,
                                         radius=0.5,
                                         parentJoint=self.soft_grp,
                                         parentIk=self.tzIk_loc)
        #--- create the rotationZ setup
        self.soft_rz_jnt = joint.IkChain(side=self._side,
                                         name=[self._moduleName + 'SoftRotZ1',
                                               self._moduleName + 'SoftRotZ2'],
                                         suffix='JNT',
                                         position=[[0, 0, 0], [1, 0, 0]],
                                         orientation=[[0, 0, 0], [0, 0, 0]],
                                         ikSolver='ikSCSolver',
                                         mirror=False,
                                         radius=0.5,
                                         parentJoint=self.soft_grp,
                                         parentIk=self.tyIk_loc)
        cmds.setAttr(self.soft_rz_jnt.joint_names[0] + '.t', 0, 0, 0)
        cmds.setAttr(self.soft_rz_jnt.joint_names[1] + '.t', 1, 0, 0)

        #--- connect the softClavicle joints to the autoClavicle nodes system
        cmds.disconnectAttr(self.joints_ac[0] + '.rotate', self.mlt + '.input1')
        goe.connectAttr(self.soft_ry_jnt.joint_names[0] + '.rotateY',
                        self.mlt + '.input1Y')
        goe.connectAttr(self.soft_rz_jnt.joint_names[0] + '.rotateZ',
                        self.mlt + '.input1Z')
        #--- constraint the ik control with the translateY and Z locators
        node.pointConstraint(objA=self._side + "_armWristIK_CTL",
                             objB=self.ty_loc, suffix='PCN')
        node.pointConstraint(objA=self._side + "_armWristIK_CTL",
                             objB=self.tz_loc, suffix='PCN')
        #--- connect the clavicles softness attr with the tx of the locators
        goe.connectAttr(self.fk_controls[0].transform + '.softness',
                        self.tyIk_loc + '.tx')
        goe.connectAttr(self.fk_controls[0].transform + '.softness',
                        self.tzIk_loc + '.tx')
        #--- relimit rotations of the clavicle SDK group
        cmds.transformLimits(self.sdk, enableRotationX=(1, 1),
                             enableRotationY=(0, 0),
                             enableRotationZ=(0, 0),
                             rotationX=(0, 0))
        #--- set the multiplyDivide input2 values of the softClavicle to 1
        goe.setAttr(self.mlt + '.input2', 1, 1, 1)
        attribute.lock_n_hide(self.mlt, ['input2'])
    #END __prepare_soft_clavicle()

    def __cleanup(self):
        """ Cleanup, delete nodes and lock attributes """
        if self._moduleName:
            guideGrp = self._moduleName.upper() + 'GUIDE'
            if cmds.objExists(guideGrp):
                cmds.delete(guideGrp)
            else:
                if self._guides:
                    for i in self._guides:
                        if cmds.objExists(i):
                            cmds.delete(i)
            guideTrn = self._side + '_' + self._moduleName + 'Guide_TRN'
            if cmds.objExists(guideTrn):
                cmds.delete(guideTrn)

        guideRoot = 'GUIDE_ROOT'
        if cmds.objExists(guideRoot):
            if not cmds.listRelatives(guideRoot, children=True):
                cmds.delete(guideRoot)
            elif not cmds.listRelatives(guideRoot, allDescendents=True,
                                        type='goe_locator'):
                cmds.delete(guideRoot)

        if self.DEBUG:
            return

        #--- set the display to OFF
        cmds.setAttr(self.mod_grp + '.showJoints', 0)
        cmds.setAttr(self.mod_grp + '.showIkHandles', 0)

        #--- cleanup the constraints
        pac = cmds.ls(type='parentConstraint')
        pcn = cmds.ls(type='pointConstraint')
        ocn = cmds.ls(type='orientConstraint')
        scn = cmds.ls(type='scaleConstraint')
        constraints = [pac, pcn, ocn, scn]
        for const in constraints:
            for i in const:
                if not i:
                    continue
                cmds.setAttr(i + '.ihi', 0)
                attribute.lock_all(i)

        #--- cleanup joints
        for jnt in self.joints:
            cmds.setAttr(jnt + '.ihi', 0)

        #--- hide joints
        for i, obj in enumerate(self.joints):
            for axis in 'xyz':
                cmds.setAttr(obj + '.t' + axis, keyable=False, lock=True)
                cmds.setAttr(obj + '.r' + axis, keyable=False, lock=False)
                cmds.setAttr(obj + '.s' + axis, keyable=False, lock=True)
            cmds.setAttr(obj + '.v', keyable=False, lock=True)
            cmds.setAttr(obj + '.radi', keyable=False, channelBox=False)
            cmds.setAttr(obj + '.drawStyle', 0)

        #--- lock all attributes in the to_lock list
        for i in self.to_lock:
            cmds.setAttr(i + '.ihi', 0)
            attribute.lock_all(i)
    #END __cleanup()

    def __create(self):
        #--- check parameters
        self.__check_parameters()

        #--- prepare guides
        self.__prepare_guides()

        #--- create mod group
        self.__create_mod_group()

        #--- setup mod group
        self.__setup_mod_group()

        #--- create joints
        self.__prepare_joint_setup()

        #--- fk setup
        self.__fk_setup()

        #--- auto clavicle
        self.__prepare_clavicle_setup()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END BipedCartoonClavicleRig()


class BipedCartoonScapulaRig(rigs.RigCmds):
    """ Create a basic arm setup based on your specifications """
    def __init__(self,
                 side='C',
                 moduleName=None,
                 guides=[],
                 shape=14,
                 size=1,
                 color=None,
                 rotateOrder='xyz',
                 mirrorAxis='x',
                 autoScapulaPos=[],
                 DEBUG=True):
        """
        @type  assetType: string
        @param assetType: specify the character type (ie."HUMAN","FISH")

        @type  moduleName: string
        @param moduleName: specify the name of the module

        @type  side: string
        @param side: specify the side! (ie. 'C', 'L', 'R')

        @type  shape: integer
        @param shape: specify the number of the shape, default is 1

        @type  size: float
        @param size: specify the size of the control, default is 1

        @type  color: integer
        @param color: specify the number of the color, default is 17

        @type  guides: list
        @param guides: specify a list with the guideJoint names

        @type  offsetGroups: integer
        @param offsetGroups: specify the amount of control offsetGroups

        @type  rotateOrder: string/integer
        @param rotateOrder: specify the rotateOrder as string or integer

        @type  mirrorAxis: string
        @param mirrorAxis: valid axis are 'x', 'y', 'z'

        @type  DEBUG: bool
        @param DEBUG: Show all rig related setups, turn Off when finished
        """
        super(BipedCartoonScapulaRig, self).__init__()

        #--- args
        self._side = side
        self._shape = shape
        self._size = size
        self._color = color
        self._moduleName = moduleName
        self._guides = guides
        self._rotateOrder = rotateOrder
        self._mirrorAxis = mirrorAxis
        self._autoScapulaPos = autoScapulaPos
        self.DEBUG = DEBUG

        #--- vars
        self.guides = list()

        self.mod_grp = None
        self.bind_grp = None
        self.fk_grp = None
        self.ik_grp = None

        self.joints = list()
        self.joint_pac = list()

        self.fk_controls = list()

        self.to_lock = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        """ Check the class parameters for validation """
        #--- check moduleName
        msg = "moduleName: Please specify a string"
        assert self._moduleName, msg
        assert isinstance(self._moduleName, str), msg

        #--- check side
        assert self._side, ("side: Please specify 'C', 'L' or 'R'!")

        #--- check guideJoints
        msg = "guideJoints: Please specify a list!"
        assert self._guides, msg
        assert isinstance(self._guides, list), msg

        #--- check rotateOrder
        msg = "rotateOrder: Please specify a valid string or an integer!"
        assert self._rotateOrder, msg
    #END __check_parameters()

    @property
    def __mirror_check(self):
        """ Check the scene if there is already a created rig for mirroring """
        check = False
        if self._side == 'C':
            return check

        mirror = 'R'
        if self._side == 'R':
            mirror = 'L'
        if cmds.objExists(mirror + '_' + self._moduleName + '_MOD'):
            check = True

        return check
    #END __mirror_check()

    def __prepare_guides(self):
        """ Check the scene, get the guides and prepare them for the rig """
        to_delete = list()
        for gid in self._guides:
            #--- list all the goe locators in the scene
            shapes = cmds.ls(type='goe_locator')
            if not shapes:
                continue
            for shp in shapes:
                #--- get the transform and group nodes of the guide shapes
                trn = cmds.listRelatives(shp, parent=True, type='transform')[0]
                grp = cmds.listRelatives(trn, parent=True, type='transform')[0]
                #--- check the guide control tags vor validation
                if not cmds.objExists(trn + '.guideID'):
                    continue
                if not cmds.getAttr(trn + '.side') == self._side:
                    continue
                if not cmds.getAttr(trn + '.guideID') == gid:
                    continue
                #--- get the name, position and rotation of the guide
                nme = cmds.getAttr(trn + '.name')
                pos = cmds.xform(trn, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(trn, query=True, rotation=True, worldSpace=True)
                #--- check if we deal with a mirrored side and setup rotation
                if self.__mirror_check:
                    if self._mirrorAxis == 'x':
                        rot = [180 + rot[0], rot[1], rot[2]]
                    elif self._mirrorAxis == 'y':
                        rot = [rot[0], 180 + rot[1], rot[2]]
                    elif self._mirrorAxis == 'z':
                        rot = [rot[0], rot[1], 180 + rot[2]]
                #--- append the name, position and rotation to a guide list
                self.guides.append([nme, pos, rot])
                #--- list all the constraints of the groups and delete them
                cnt = cmds.listConnections(grp)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- list all the constraints of the controls and delete them
                cnt = cmds.listConnections(trn)
                if cnt:
                    cnt = [cmds.delete(i) for i in cnt if cmds.objExists(i)
                           if 'Constraint' in cmds.nodeType(i)]
                #--- add the guide group to the deletion list
                to_delete.append(grp)

        #--- delete the guides itself
        for d in to_delete:
            if cmds.objExists(d):
                cmds.delete(d)

        #--- setup the colors
        if not self._color:
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
            elif self._side == 'C':
                self._color = 17
    #END __prepare_guides()

    def __create_mod_group(self):
        """ Create the module groups for the rig setup """
        #--- create module group
        self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if self._moduleName:
            self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if not cmds.objExists(self.mod_grp):
            self.mod_grp = cmds.createNode('transform', name=self.mod_grp,
                                           parent=self.rig_grp)
        attribute.lock_all(self.mod_grp)

        #--- create bind joint group
        self.bind_grp = self._side + '_' + self._moduleName + 'BIND_MOD'
        if not cmds.objExists(self.bind_grp):
            self.bind_grp = cmds.createNode('transform', name=self.bind_grp,
                                            parent=self.mod_grp)
        attribute.lock_all(self.bind_grp)
    #END __create_mod_group()

    def __setup_mod_group(self):
        """ Setup the module group and att proper attributes """
        #--- showJoints
        if not cmds.objExists(self.mod_grp + '.showJoints'):
            cmds.addAttr(self.mod_grp, longName='showJoints',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showJoints', edit=True, channelBox=True)

        #--- showIkHandles
        if not cmds.objExists(self.mod_grp + '.showIkHandles'):
            cmds.addAttr(self.mod_grp, longName='showIkHandles',
                         attributeType='short', defaultValue=1, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showIkHandles', edit=True, channelBox=True)
    #END __setup_mod_group()

    def __prepare_joint_setup(self):
        """ Prepare, create and setup the joints """
        #--- create joints
        for num, i in enumerate(self.guides):
            cmds.select(clear=True)
            pos = i[1]
            rot = i[2]
            jnt = self.__create_joint_setup(num, pos, rot)
            self.joints.append(jnt)

        self.__create_joint_chain()
    #END __prepare_joint_setup()

    def __create_joint_setup(self, num=0, pos=[0, 0, 0], rot=[0, 0, 0]):
        """
        @type  name: string
        @param name: specify an additional name for the joints

        @type  num: int
        @param num: specify the index num

        @type  pos: list
        @param pos: specify the position values

        @type  rot: list
        @param rot: specify the rotation values
        """
        #--- create and reposition joints
        jnt_name = (self._side + '_' + self._moduleName + repr(num) + '_JNT')
        jnt = cmds.joint(name=jnt_name)
        cmds.xform(jnt, translation=pos, worldSpace=True)
        cmds.setAttr(jnt + '.r', 0, 0, 0)
        cmds.setAttr(jnt + '.jo', rot[0], rot[1], rot[2])

        #--- connect visibility of joints with main group
        cmds.connectAttr(self.mod_grp + '.showJoints', jnt + '.v')
        main = self.main_control.transform + '.globalScale'
        cmds.connectAttr(main, jnt + '.radius')

        #--- change draw style
        cmds.setAttr(jnt + '.drawStyle', 0)

        #--- reparent the joint under the bind group
        cmds.parent(jnt, self.bind_grp)
        return jnt
    #END __create_joint_setup()

    def __create_joint_chain(self):
        """ Create a joint chain """
        for i, jnt in enumerate(self.joints):
            j = i + 1
            if not j == len(self.joints):
                cmds.parent(self.joints[j], jnt)
    #END __create_joint_chain()

    def __fk_setup(self):
        """ Prepare the fk setup for this rig system """
        #--- create fk controls
        self.__fk_create_controls()
        #--- setup fk controls
        self.__fk_setup_controls()
    #END __fk_setup()

    def __fk_create_controls(self):
        """ Create the fk controls """
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            if not num:
                name = self._moduleName + 'Sternal'
            elif num == 1:
                name = self._moduleName + 'Acromial'
            ctl = controls.Control(side=self._side,
                                   name=name,
                                   shape=self._shape,
                                   size=self._size,
                                   color=self._color,
                                   position=pos,
                                   rotation=rot,
                                   rotateOrder=self._rotateOrder,
                                   parent=self.mod_grp)
            #--- append to fk list
            self.fk_controls.append(ctl)
    #END __fk_create_controls()

    def __fk_setup_controls(self):
        """ Parent the fk control shapes under the fk joints and rename them """
        for i, jnt in enumerate(self.joints):
            cmds.parent(self.fk_controls[i].shape, jnt, relative=True, shape=True)
            cmds.delete(self.fk_controls[i].group)
            cmds.rename(jnt, self.fk_controls[i].transform)
        #--- overwrite the fk joints list by the fk controls' transform list
        self.joints = [i.transform for i in self.fk_controls]
    #END __fk_setup_controls()

    def __auto_scapula_setup(self):
        """ Create and setup the autoScapula """
        #--- create locators for the autoScapula setup
        pos = cmds.xform(self._autoScapulaPos[-1], query=True, translation=True, worldSpace=True)
        target_loc = node.locator(name=self._side + '_' + self._moduleName + 'AutoScapTarget',
                                  suffix='LOC', position=[0, 22, 0],
                                  worldSpace=True, parent=self.mod_grp)
        pos_loc = node.locator(name=self._side + '_' + self._moduleName + 'AutoScapPosition',
                               suffix='LOC', position=pos, worldSpace=True,
                               parent=self.mod_grp)
        aim_loc = node.locator(name=self._side + '_' + self._moduleName + 'AutoScapAim',
                               suffix='LOC', parent=pos_loc)
        up_loc = node.locator(name=self._side + '_' + self._moduleName + 'AutoScapUp',
                              suffix='LOC', position=[0, 5, 0], worldSpace=False,
                              parent=pos_loc)
        #--- constraint the locators properly
        node.pointConstraint(objA=self._autoScapulaPos[-1], objB=pos_loc,
                             suffix='PCN', maintainOffset=False)
        node.aimConstraint(target=target_loc, source=aim_loc, suffix='AIM',
                           worldUpObject=up_loc, worldUpType='object')
        node.parentConstraint(objA=aim_loc, objB=self.joints[0], suffix='PAC')
    #END __auto_scapula_setup()

    def __cleanup(self):
        """ Cleanup, delete nodes and lock attributes """
        if self._moduleName:
            guideGrp = self._moduleName.upper() + 'GUIDE'
            if cmds.objExists(guideGrp):
                cmds.delete(guideGrp)
            else:
                if self._guides:
                    for i in self._guides:
                        if cmds.objExists(i):
                            cmds.delete(i)
            guideTrn = self._side + '_' + self._moduleName + 'Guide_TRN'
            if cmds.objExists(guideTrn):
                cmds.delete(guideTrn)

        guideRoot = 'GUIDE_ROOT'
        if cmds.objExists(guideRoot):
            if not cmds.listRelatives(guideRoot, children=True):
                cmds.delete(guideRoot)
            elif not cmds.listRelatives(guideRoot, allDescendents=True,
                                        type='goe_locator'):
                cmds.delete(guideRoot)

        if self.DEBUG:
            return

        #--- set the display to OFF
        cmds.setAttr(self.mod_grp + '.showJoints', 0)
        cmds.setAttr(self.mod_grp + '.showIkHandles', 0)

        #--- cleanup the constraints
        pac = cmds.ls(type='parentConstraint')
        pcn = cmds.ls(type='pointConstraint')
        ocn = cmds.ls(type='orientConstraint')
        scn = cmds.ls(type='scaleConstraint')
        constraints = [pac, pcn, ocn, scn]
        for const in constraints:
            for i in const:
                if not i:
                    continue
                cmds.setAttr(i + '.ihi', 0)
                attribute.lock_all(i)

        #--- cleanup joints
        for jnt in self.joints:
            cmds.setAttr(jnt + '.ihi', 0)

        #--- hide joints
        for i, obj in enumerate(self.joints):
            for axis in 'xyz':
                cmds.setAttr(obj + '.t' + axis, keyable=False, lock=True)
                cmds.setAttr(obj + '.r' + axis, keyable=False, lock=False)
                cmds.setAttr(obj + '.s' + axis, keyable=False, lock=True)
            cmds.setAttr(obj + '.v', keyable=False, lock=True)
            cmds.setAttr(obj + '.radi', keyable=False, channelBox=False)
            cmds.setAttr(obj + '.drawStyle', 0)

        #--- lock all attributes in the to_lock list
        for i in self.to_lock:
            cmds.setAttr(i + '.ihi', 0)
            attribute.lock_all(i)
    #END __cleanup()

    def __create(self):
        #--- check parameters
        self.__check_parameters()

        #--- prepare guides
        self.__prepare_guides()

        #--- create mod group
        self.__create_mod_group()

        #--- setup mod group
        self.__setup_mod_group()

        #--- create joints
        self.__prepare_joint_setup()

        #--- fk setup
        self.__fk_setup()

        #--- auto clavicle
        self.__auto_scapula_setup()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END BipedCartoonScapulaRig()


def main_call(callMethod='guide', data=None):
    """ Call the guides or puppets giving the proper data
    @type  callMethod: string
    @param callMethod: specify 'guide' or 'puppet' to build properly

    @type  data: dict
    @param data: specify the rigdata from the ui to build the guides properly
    """
    if callMethod == 'guide':
        guide_ui(data)
    elif callMethod == 'puppet':
        key, value = rig_ui(data)
        return key, value
#END main_call()


def guide_ui(rdata):
    """
    @type  rdata: dict
    @param rdata: specify the rigdata from the ui to build the guides pistonerly
    """
    BipedCartoonArmGuide(moduleName=str(rdata['moduleName']),
                         side=str(rdata['side']),
                         size=float(rdata['size']),
                         shape=30,
                         color=int(rdata['color']),
                         mirror=rdata['mirror'],
                         mirrorAxis=str(rdata['mirrorAxis']),
                         asymmetry=rdata['asymmetry'],
                         clavicle=rdata['addClavicle'],
                         scapula=rdata['addScapula'])
#END guide_ui()


def rig_ui(rdata):
    """
    @type  rdata: dict
    @param rdata: specify the rigdata from the ui to build the rig properly
    """
    guides = [rdata['moduleName'] + str(num) for num in range(4)]
    clavicle_guides = [rdata['moduleName'] + 'Clavicle' + str(num) for num in range(2)]
    scapula_guides = [rdata['moduleName'] + 'Scapula' + str(num) for num in range(2)]
    if not rdata['addClavicle']:
        clavicle_guides = None
    if not rdata['addScapula']:
        scapula_guides = None
    p = BipedCartoonArmRig(side=str(rdata['side']),
                           moduleName=str(rdata['moduleName']),
                           guides=guides,
                           clavicleGuides=clavicle_guides,
                           scapulaGuides=scapula_guides,
                           size=float(rdata['size']),
                           shape=int(rdata['shape']),
                           color=int(rdata['color']),
                           offsetGroups=int(rdata['offsets']),
                           withGimbal=rdata['withGimbal'],
                           rotateOrder=str(rdata['rotateOrder']),
                           mirrorAxis=rdata['mirrorAxis'],
                           fk=rdata['fk'],
                           ik=rdata['ik'],
                           fkik=rdata['fkik'],
                           addArmTwist=rdata['addArmTwist'],
                           addIkStretch=rdata['addIkStretch'],
                           addIkBend=rdata['addIkBend'],
                           addSoftClavicle=rdata['addSoftClavicle'],
                           parentType=rdata['parentMethod'])
    mod = rdata['side'].lower() + rdata['moduleName']
    jnt = p.joints
    fk_jnt = p.fk_joints
    ik_jnt = p.ik_joints
    return mod, [p.fk_controls, p.ik_controls, jnt, fk_jnt, ik_jnt]
#END rig_ui()


def data_ui():
    """ save the pistoncmds flags to show off in the ui """
    data.save_cmds_data({'biped_cartoon_arm':
                         [{'side': {'default': 'C', 'widget': 'combobox', 'value': ['C', 'L', 'R']}},
                          {'moduleName': {'default': None, 'widget': 'lineEdit', 'value': None}},
                          {'size': {'default': 1.0, 'widget': 'double', 'value': 1.0}},
                          {'shape': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'orientation': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'color': {'default': 17, 'widget': 'int', 'value': 0}},
                          {'offsets': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'withGimbal': {'default': 'False', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'rotateOrder': {'default': 'xyz', 'widget': 'combobox', 'value': ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']}},
                          {'mirror': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'mirrorAxis': {'default': 'x', 'widget': 'combobox', 'value': ['x', 'y', 'z']}},
                          {'asymmetry': {'default': 'False', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'fk': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'ik': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'fkik': {'default': 'Blend', 'widget': 'combobox', 'value': ['Blend', 'Switch']}},
                          {'addArmTwist': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'addIkStretch': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'addIkBend': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'addClavicle': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'addSoftClavicle': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'addScapula': {'default': 'True', 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'parentMethod': {'default': 'parent', 'widget': 'combobox', 'value': ['parent', 'constraint', 'None']}}]})
#END data_ui()
