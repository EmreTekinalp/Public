'''
@author:  etekinalp
@date:    Sep 12, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates piston rigs
'''


from maya import cmds

from goe_functions import attribute, check, controls, data, goe, node, rigs, tools

reload(attribute)
reload(controls)
reload(data)
reload(goe)
reload(node)
reload(rigs)
reload(tools)


class PistonGuide(object):
    def __init__(self,
                 moduleName=None,
                 side=None,
                 size=1,
                 shape=30,
                 color=None,
                 mirror=False,
                 mirrorAxis='x',
                 asymmetry=False):
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

        #--- vars
        self.root = 'GUIDE_ROOT'
        self.mod = None
        self.position = list()
        self.rotation = list()

        self.controls = list()
        self.mirror_control = list()

        self.to_ihi = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
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
        #--- color
        if self._color == None:  # @IgnorePep8
            self._color = 17
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
        #--- position
        if not self.position:
            for pos in range(2):
                pos = [0, pos, 0]
                self.position.append(pos)
        #--- rotation
        if not self.rotation:
            for rot in range(2):
                rot = [0, 0, 0]
                self.rotation.append(rot)
    #END __prepare()

    def __setup_mod_group(self):
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

    def __setup_controls(self):
        self.up_vector = None
        for i in range(2):
            ctl = self.__create_control(self._side, self._moduleName, i,
                                        self._color, self.mod)
            if not i:
                nme = self._side + '_' + self._moduleName + "Up"
                self.up_vector = node.transform(name=nme, position=[1, 0, 0],
                                                parent=ctl.transform)
            if i:
                aim = node.aimConstraint(target=self.controls[0].transform,
                                         source=ctl.transform,
                                         aimVector=[0, -1, 0],
                                         upVector=[0, 0, 0],
                                         worldUpObject=self.up_vector,
                                         worldUpType='object')
                self.to_ihi.append(aim)
                attribute.lock_attributes(ctl.transform, ['r'], False, True)
                attribute.lock_n_hide(self.controls[0].transform, ['r'], True)
            self.controls.append(ctl)
            if self._mirror:
                self.__mirror_guides(ctl.transform, i)
        #-- create control chain
        self.__create_chain(self.controls)
    #END __setup_controls()

    def __create_control(self, side, name, index, color, parent):
        ctl = controls.Control(side=side, name=name + 'Guide' + repr(index),
                               shape=self._shape, size=self._size, color=color,
                               position=self.position[index],
                               rotation=self.rotation[index],
                               parent=parent)
        self.__add_control_attributes(ctl.transform, side, name, index)
        return ctl
    #END __create_control()

    def __add_control_attributes(self, control, side, name, index):
        if not cmds.objExists(control + '.side'):
            cmds.addAttr(control, longName="side", dataType='string')
            cmds.setAttr(control + '.side', side, type='string', lock=True)
        if not cmds.objExists(control + '.name'):
            cmds.addAttr(control, longName="name", dataType='string')
            cmds.setAttr(control + '.name', name, type='string', lock=True)
        if not cmds.objExists(control + '.index'):
            cmds.addAttr(control, longName="index", dataType='string')
            cmds.setAttr(control + '.index', repr(index), type='string', lock=True)
        if not cmds.objExists(control + '.guideID'):
            cmds.addAttr(control, longName="guideID", dataType='string')
            cmds.setAttr(control + '.guideID', name + repr(index),
                         type='string', lock=True)
    #END __add_control_attributes()

    def __mirror_guides(self, obj, index):
        #--- check and setup the side
        msg = "Please specify 'L' or 'R' as valid side!"
        assert not self._side == 'C', check.error(self, 1, str(self._side), msg)
        side = 'R'
        color = 13
        if self._side == 'R':
            side = 'L'
            color = 6

        #--- create mirror control
        ctl = self.__create_control(side, self._moduleName,
                                    index, color, self.mod)

        #--- add mirror attribute
        if not cmds.objExists(ctl.transform + '.MIRROR'):
            cmds.addAttr(ctl.transform, longName="MIRROR", attributeType='bool')
            cmds.setAttr(ctl.transform + '.MIRROR', 1, lock=True, keyable=False)
            if self._asymmetry:
                if not cmds.objExists(ctl.transform + '.ASYM'):
                    cmds.addAttr(ctl.transform, longName="ASYM",
                                 attributeType='bool')
                    cmds.setAttr(ctl.transform + '.ASYM', 1,
                                 lock=True, keyable=False)

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

        self.mirror_control.append(ctl)
    #END __mirror_guides()

    def __create_chain(self, controls):
        for i, ctl in enumerate(controls):
            j = i + 1
            if not j == len(controls):
                attribute.lock_all(controls[j].group, True)
                cmds.parent(controls[j].group, ctl.transform)
                attribute.lock_all(controls[j].group)
    #END __create_chain()

    def __cleanup(self):
        for i in self.to_ihi:
            cmds.setAttr(i + '.ihi', 0)
    #END __cleanup()

    def __setup_data(self):
        data = dict()
        data['GUIDE'] = str(self.mod)
        data['GUIDETYPE'] = 'pistonCmds'
        data['moduleName'] = str(self._moduleName)
        data['side'] = str(self._side)
        data['size'] = float(self._size)
        data['shape'] = int(self._shape)
        data['color'] = int(self._color)
        data['mirror'] = bool(self._mirror)
        data['mirrorAxis'] = str(self._mirrorAxis)
        data['asymmetry'] = bool(self._asymmetry)
        if not cmds.getAttr(self.mod + '.guideDATA'):
            cmds.setAttr(self.mod + '.guideDATA', data,
                         type='string', lock=True)
    #END __setup_data()

    def __create(self):
        #--- check the parameters
        self.__check_parameters()
        #--- prepare parameters
        self.__prepare()
        #--- setup mod_group
        self.__setup_mod_group()
        #--- setup the controls
        self.__setup_controls()
        #--- cleanup
        self.__cleanup()
        #--- setup data
        self.__setup_data()
    #END __create()
#END PistonGuide()


class PistonRig(rigs.RigCmds):
    """ Create a basic control setup based on your specifications """
    def __init__(self,
                 side='C',
                 moduleName=None,
                 guides=[],
                 shape=14,
                 size=1,
                 color=None,
                 offsetGroups=0,
                 withGimbal=False,
                 rotateOrder='xyz',
                 mirrorAxis='x',
                 parentFirst=None,
                 parentLast=None,
                 parentType=None):
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

        @type  parentFirst: string
        @param parentFirst: parent the first control under a specified transform

        @type  parentLast: string
        @param parentLast: parent the last control under a specified transform

        @type  parentType: string
        @param parentType: Valid values are None, parent, constraint.
                           None = the controls will be parented under the
                                  mod groups
                           parent = the controls will be parented underthe
                                    mainGimbal control
                           constraint = the controls will be constraint to the
                                        mainGimbal control
        """
        super(PistonRig, self).__init__()

        #--- args
        self._side = side
        self._shape = shape
        self._size = size
        self._color = color
        self._moduleName = moduleName
        self._guides = guides
        self._offsetGroups = offsetGroups
        self._withGimbal = withGimbal
        self._rotateOrder = rotateOrder
        self._mirrorAxis = mirrorAxis
        self._parentFirst = parentFirst
        self._parentLast = parentLast
        self._parentType = parentType

        #--- vars
        self.mod_grp = None
        self.guides = list()
        self.controls = list()
        self.joints = list()
        self.rev_joints = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
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

        #--- parent first
        if self._parentFirst:
            if not cmds.objExists(self._parentFirst):
                msg = ("ModuleName: " + str(self._moduleName.upper()) + " "
                       "parentFirst: " + str(self._parentFirst) + " --> "
                       "Specified object does not exist in scene! "
                       "parentFirst will be set to None automatically! "
                       "Check the correct spelling of the object OR "
                       "Check the order of the rig setups!")
                cmds.warning(msg)
                self._parentFirst = None

        #--- parent last
        if self._parentLast:
            if not cmds.objExists(self._parentLast):
                msg = ("ModuleName: " + str(self._moduleName.upper()) + " "
                       "parentLast: " + str(self._parentLast) + " --> "
                       "Specified object does not exist in scene! "
                       "parentLast will be set to None automatically! "
                       "Check the correct spelling of the object OR "
                       "Check the order of the rig setups!")
                cmds.warning(msg)
                self._parentLast = None

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
        to_delete = list()
        for gd in self._guides:
            shapes = cmds.ls(type='goe_locator')
            if not shapes:
                continue
            for shp in shapes:
                trn = cmds.listRelatives(shp, parent=True, type='transform')[0]
                grp = cmds.listRelatives(trn, parent=True, type='transform')[0]
                if cmds.objExists(trn + '.guideID'):
                    if cmds.getAttr(trn + '.side') == self._side:
                        if cmds.getAttr(trn + '.guideID') == gd:
                            nme = cmds.getAttr(trn + '.name')
                            pos = cmds.xform(trn, query=True, translation=True,
                                             worldSpace=True)
                            rot = cmds.xform(trn, query=True, rotation=True,
                                             worldSpace=True)
                            #--- check if we deal with a mirrored side
                            if self.__mirror_check:
                                if self._mirrorAxis == 'x':
                                    rot = [180 + rot[0], rot[1], rot[2]]
                                elif self._mirrorAxis == 'y':
                                    rot = [rot[0], 180 + rot[1], rot[2]]
                                elif self._mirrorAxis == 'z':
                                    rot = [rot[0], rot[1], 180 + rot[2]]
                            self.guides.append([nme, pos, rot])
                            to_delete.append(grp)
        for d in to_delete:
            if cmds.objExists(d):
                cmds.delete(d)

        if not self._color:
            if self._side == 'L':
                self._color = 6
            elif self._side == 'R':
                self._color = 13
            elif self._side == 'C':
                self._color = 17
    #END __prepare_guides()

    def __create_mod_group(self):
        self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if self._moduleName:
            self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if not cmds.objExists(self.mod_grp):
            self.mod_grp = cmds.createNode('transform', name=self.mod_grp,
                                           parent=self.rig_grp)
        attribute.lock_all(self.mod_grp)
    #END __create_mod_group()

    def __setup_mod_group(self):
        #--- showJoints
        if not cmds.objExists(self.mod_grp + '.showJoints'):
            cmds.addAttr(self.mod_grp, longName='showJoints',
                         attributeType='short', defaultValue=0, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showJoints', edit=True, channelBox=True)

        #--- showIkHandles
        if not cmds.objExists(self.mod_grp + '.showIkHandles'):
            cmds.addAttr(self.mod_grp, longName='showIkHandles',
                         attributeType='short', defaultValue=0, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showIkHandles', edit=True, channelBox=True)
    #END __setup_mod_group()

    def __create_controls(self):
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            name = self._moduleName + repr(num)
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
            #--- append to a list
            self.controls.append(ctl)
    #END __create_controls()

    def __setup(self):
        if not self._parentType:
            return
        if self._parentType == 'parent':
            #--- parent
            for ctl in self.controls:
                attribute.lock_n_hide(ctl.group, ['t', 'r', 's'], True)
                cmds.parent(ctl.group, self.main_control.gimbal)
                attribute.lock_n_hide(ctl.group, ['t', 'r', 's'])
        elif self._parentType == 'constraint':
            #--- constraint
            for ctl in self.controls:
                node.parentConstraint(self.main_control.gimbal, ctl.group)
                for axis in 'xyz':
                    cmds.setAttr(ctl.group + '.s' + axis, lock=False)
                    cmds.connectAttr(self.main_control.transform + '.globalScale',
                                     ctl.group + '.s' + axis)
                    cmds.setAttr(ctl.group + '.s' + axis, lock=True)
    #END __setup()

    def __prepare_joint_setup(self):
        #--- create joints
        joints = list()
        for num, i in enumerate(self.guides):
            cmds.select(clear=True)
            pos = i[1]
            rot = i[2]
            jnt = self.__create_joint_setup(num, pos, rot)
            joints.append(jnt)

        #--- reparent joints
        cmds.parent(joints[0], joints[1])
        cmds.setAttr(joints[0] + '.jo', 0, 0, 0)
        cmds.parent(joints[0], self.controls[0].transform)
        cmds.parent(joints[1], joints[0])
        cmds.setAttr(joints[1] + '.jo', 0, 0, 0)

        #--- create reverse joints
        rev = list()
        for num, jnt in enumerate(joints):
            nme = self._side + '_' + self._moduleName + "Reverse" + repr(num) + '_JNT'
            dup = cmds.duplicate(jnt, name=nme, parentOnly=True)[0]

            #--- connect visibility of joints with main group
            cmds.connectAttr(self.mod_grp + '.showJoints', dup + '.v')
            main = self.main_control.transform + '.globalScale'
            cmds.connectAttr(main, dup + '.radius')

            #--- change draw style
            cmds.setAttr(dup + '.drawStyle', 0)
            rev.append(dup)

        #--- reparent reversed joints
        cmds.parent(rev[0], rev[1])
        cmds.parent(rev[1], self.controls[1].transform)

        self.joints = joints
        self.rev_joints = rev
    #END __prepare_joint_setup()

    def __create_joint_setup(self,
                             num=0,
                             pos=[0, 0, 0],
                             rot=[0, 0, 0]):
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
        ctl = self.controls[num].transform
        if self._withGimbal:
            ctl = self.controls[num].gimbal
        jnt_name = (self._side + '_' + self._moduleName + repr(num) + '_JNT')
        jnt = cmds.joint(name=jnt_name)
        cmds.xform(jnt, translation=pos, worldSpace=True)
        cmds.setAttr(jnt + '.rotate', rot[0], rot[1], rot[2])

        #--- parent the joint under the control
        cmds.parent(jnt, ctl)
        cmds.setAttr(jnt + '.t', 0, 0, 0)
        cmds.setAttr(jnt + '.r', 0, 0, 0)
        cmds.setAttr(jnt + '.jo', 0, 0, 0)
        #--- connect visibility of joints with main group
        cmds.connectAttr(self.mod_grp + '.showJoints', jnt + '.v')
        main = self.main_control.transform + '.globalScale'
        cmds.connectAttr(main, jnt + '.radius')

        #--- change draw style
        cmds.setAttr(jnt + '.drawStyle', 0)
        return jnt
    #END __create_joint_setup()

    def __create_ik_setup(self):
        """ Create an ikSingleSolver setup """
        ik = tools.two_joint_ik(self.joints[0], self.joints[1],
                                self.controls[1].transform)
        rev_ik = tools.two_joint_ik(self.rev_joints[1], self.rev_joints[0],
                                    self.controls[0].transform)

        #--- connect visibility of ikHandles with main group
        attribute.lock_attributes(ik, ['v'], False)
        attribute.lock_attributes(rev_ik, ['v'], False)
        cmds.connectAttr(self.mod_grp + '.showIkHandles', ik[0] + '.v')
        cmds.connectAttr(self.mod_grp + '.showIkHandles', rev_ik[0] + '.v')
        attribute.lock_attributes(ik, ['v'])
        attribute.lock_attributes(rev_ik, ['v'])
    #END __create_ik_setup()

    def __reparent_controls(self):
        """ Reparent the controls properly """
        if self._parentFirst:
            attribute.lock_all(self.controls[0].group, True)
            parent = cmds.listRelatives(self.controls[0].group, parent=True)
            if not parent or not parent[0] == self._parentFirst:
                cmds.parent(self.controls[0].group, self._parentFirst)
            attribute.lock_all(self.controls[0].group)

        if self._parentLast:
            attribute.lock_all(self.controls[-1].group, True)
            parent = cmds.listRelatives(self.controls[-1].group, parent=True)
            if not parent or not parent[0] == self._parentLast:
                cmds.parent(self.controls[-1].group, self._parentLast)
            attribute.lock_all(self.controls[-1].group)
    #END __reparent_controls()

    def __cleanup(self):
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
                attribute.lock_all(i)
                cmds.setAttr(i + '.ihi', 0)

        #--- cleanup joints
        for jnt in self.joints:
            cmds.setAttr(jnt + '.ihi', 0)
        for jnt in self.rev_joints:
            cmds.setAttr(jnt + '.ihi', 0)
            self.joints.append(jnt)

        #--- hide joints
        for i, obj in enumerate(self.joints):
            for axis in 'xyz':
                cmds.setAttr(obj + '.t' + axis, keyable=False, lock=True)
                cmds.setAttr(obj + '.r' + axis, keyable=False, lock=False)
                cmds.setAttr(obj + '.s' + axis, keyable=False, lock=True)
            cmds.setAttr(obj + '.v', keyable=False, lock=True)
            cmds.setAttr(obj + '.radi', keyable=False, channelBox=False)
            cmds.setAttr(obj + '.drawStyle', 0)
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

        #--- create controls
        self.__create_controls()

        #--- setup
        self.__setup()

        #--- create joints
        self.__prepare_joint_setup()

        #--- create ik handle
        self.__create_ik_setup()

        #--- reparent controls
        self.__reparent_controls()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END PistonRig()


def main_call(callMethod='guide', data=None):
    """ Call the guides or puppets giving the proper data """
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
    PistonGuide(moduleName=str(rdata['moduleName']),
                side=str(rdata['side']),
                size=float(rdata['size']),
                shape=30,
                color=int(rdata['color']),
                mirror=rdata['mirror'],
                mirrorAxis=str(rdata['mirrorAxis']),
                asymmetry=rdata['asymmetry'])
#END guide_ui()


def rig_ui(rdata):
    """
    @type  rdata: dict
    @param rdata: specify the rigdata from the ui to build the rigs properly
    """
    guides = list()
    for num in range(2):
        guide = rdata['moduleName'] + str(num)
        guides.append(guide)
    p = PistonRig(side=str(rdata['side']),
                  moduleName=str(rdata['moduleName']),
                  guides=guides,
                  size=float(rdata['size']),
                  shape=int(rdata['shape']),
                  color=int(rdata['color']),
                  offsetGroups=int(rdata['offsets']),
                  withGimbal=rdata['withGimbal'],
                  rotateOrder=str(rdata['rotateOrder']),
                  mirrorAxis=rdata['mirrorAxis'],
                  parentFirst=rdata['parentFirst'],
                  parentLast=rdata['parentLast'],
                  parentType=rdata['hookType'])
    mod = rdata['side'].lower() + rdata['moduleName']
    jnt = p.joints
    if not jnt:
        jnt = None
    return mod, [p.controls, jnt]
#END rig_ui()


def data_ui():
    """ save the pistoncmds flags to show off in the ui """
    data.save_cmds_data({'piston':
                         [{'side': {'default': 'C', 'widget': 'combobox', 'value': ['C', 'L', 'R']}},
                          {'moduleName': {'default': None, 'widget': 'lineEdit', 'value': None}},
                          {'size': {'default': 1.0, 'widget': 'double', 'value': 1.0}},
                          {'shape': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'orientation': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'color': {'default': 17, 'widget': 'int', 'value': 0}},
                          {'offsets': {'default': 0, 'widget': 'int', 'value': 0}},
                          {'withGimbal': {'default': 0, 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'rotateOrder': {'default': 'xyz', 'widget': 'combobox', 'value': ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']}},
                          {'mirror': {'default': 0, 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'mirrorAxis': {'default': 'x', 'widget': 'combobox', 'value': ['x', 'y', 'z']}},
                          {'asymmetry': {'default': 0, 'widget': 'combobox', 'value': ['False', 'True']}},
                          {'parentFirst': {'default': None, 'widget': 'lineEdit', 'value': None}},
                          {'parentLast': {'default': None, 'widget': 'lineEdit', 'value': None}},
                          {'hookType': {'default': 0, 'widget': 'combobox', 'value': ['parent', 'constraint', 'None']}}]})
#END data_ui()
