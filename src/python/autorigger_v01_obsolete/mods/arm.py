'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Arm module with different arm classes
'''

import re
import os
from maya import cmds
from fundamentals import api, attribute, duplicate, ikhandle, measure, node
from functions import control, flexiplane, hook, jointchain, puppet
from mods import clavicle, mod, scapula
reload(api)
reload(attribute)
reload(clavicle)
reload(control)
reload(duplicate)
reload(flexiplane)
reload(hook)
reload(ikhandle)
reload(jointchain)
reload(measure)
reload(mod)
reload(node)
reload(puppet)
reload(scapula)


class BipedArmGuide(mod.MasterMod):
    """
    This class creates a biped arm guide system based on the specification made 
    in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'arm',
                  side = 'L',
                  name = ['shoulder', 'elbow', 'wrist'],
                  suffix = 'GCTL',
                  size = 0.75,
                  shape = 2,
                  orientation = [0,0,0],
                  color = 15,
                  position = [[3,20,0],[7,20,-1],[11,20,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [0,6,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None,
                  clavicleEnable = True,
                  clavicleNames = ['sternal', 'acromial'],
                  claviclePosition = [[1,20,0], [3,20,0]],
                  scapulaEnable = False,
                  scapulaNames = ['acromion', 'inferiorAngle'],
                  scapulaPosition = [[4,20,-1],[1,16,0]]):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedArmGuide, self).__init__()

        #args
        self.character        = character
        self.mod              = mod
        self.side             = side
        self.name             = name
        self.suffix           = suffix
        self.size             = size
        self.shape            = shape
        self.orientation      = orientation 
        self.color            = color
        self.position         = position
        self.rotation         = rotation
        self.upVectorOffset   = upVectorOffset
        self.aimVector        = aimVector
        self.upVector         = upVector
        self.rotateOrder      = rotateOrder
        self.flip             = flip
        self.mirrorGuideObj   = mirrorGuideObj
        self.clavicleEnable   = clavicleEnable
        self.clavicleNames    = clavicleNames
        self.claviclePosition = claviclePosition
        self.scapulaEnable    = scapulaEnable
        self.scapulaNames     = scapulaNames
        self.scapulaPosition  = scapulaPosition 

        #vars
        self.clavicle = None
        self.scapula  = None

        #methods
        self.__main_setup()
    #END def __init__()

    def __arm_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()
        nd = node.Node()
        if not self.mirrorGuideObj:
            #--- unlock the proper groups to work with them        
            attr.lockAttr(node = self.gd.g_grp, 
                          attribute = ['t', 'r', 's'], 
                          lock = False)
            #--- pointConstraint the elbowGuide to the other ones
            nd.pointConstraint(objA = [self.gd.g_ctl[0], self.gd.g_ctl[2]], 
                               objB = self.gd.g_grp[1],
                               name = (self.side + '_' + self.mod + 
                                       self.name[1][0].upper() + self.name[1][1:]))
            #--- parent the controls to the shoulder ctl
            cmds.parent(self.gd.g_grp[1], self.gd.g_grp[2], self.gd.g_ctl[0])
        else:
            self.flip = True

        #--- create the message connection setup
        self.__connect_message()

        #--- check for clavicle setup
        if self.clavicleEnable:
            #--- get the proper position values for the clavicle
            self.__arm_clavicle_setup()

        #--- check for scapula setup
        if self.scapulaEnable:
            #--- get the proper position values for the scapula
            self.__arm_scapula_setup()
    #END def __arm_setup()

    def __arm_clavicle_setup(self):
        #--- this method calls the clavicle mod
        if self.mirrorGuideObj:
            mirror_clavicle = self.mirrorGuideObj.clavicle
        else:
            mirror_clavicle = None
        self.clavicle = clavicle.BipedClavicleGuide(character = self.character,
                                                    mod = 'clavicle', 
                                                    side = self.side,
                                                    name = self.clavicleNames,
                                                    suffix = self.suffix,
                                                    size = self.size - 0.5,
                                                    orientation = self.orientation,
                                                    color = self.color,
                                                    position = self.claviclePosition,
                                                    rotation = self.rotation,
                                                    upVectorOffset = self.upVectorOffset,
                                                    aimVector = self.aimVector,
                                                    upVector = self.upVector,
                                                    rotateOrder = self.rotateOrder,
                                                    flip = self.flip,
                                                    mirrorGuideObj = mirror_clavicle)
        if not self.mirrorGuideObj:
            #--- hook the clavicle        
            hook.Hook(mod = self.clavicle, 
                      hookParent = self.gd.g_ctl[0], 
                      hookChild = self.clavicle.gd.g_grp[-1], 
                      hookType = 'pointConstraint')
    #END def __arm_clavicle_setup()

    def __arm_scapula_setup(self):
        #--- this method calls the scapula mod
        if self.mirrorGuideObj:
            mirror_scapula = self.mirrorGuideObj.scapula
        else:
            mirror_scapula = None
        self.scapula = scapula.BipedScapulaGuide(character = self.character,
                                                 mod = 'scapula', 
                                                 side = self.side,
                                                 name = self.scapulaNames,
                                                 suffix = self.suffix,
                                                 size = self.size - 0.5,
                                                 orientation = self.orientation,
                                                 color = self.color,
                                                 position = self.scapulaPosition,
                                                 rotation = self.rotation,
                                                 upVectorOffset = self.upVectorOffset,
                                                 aimVector = self.aimVector,
                                                 upVector = self.upVector,
                                                 rotateOrder = self.rotateOrder,
                                                 flip = self.flip,
                                                 mirrorGuideObj = mirror_scapula) 
        if not self.mirrorGuideObj:
            #--- hook the scapula
            hook.Hook(mod = self.scapula,
                      hookParent = self.clavicle.gd.g_ctl[-1], 
                      hookChild = self.scapula.gd.g_grp[0])
    #END def __arm_scapula_setup()

    def __connect_message(self):
        #--- this method connects the message attributes between the joints
        attr = attribute.Attribute()
        #--- create the message connections
        for i in range(len(self.gd.g_jnt)):
            j = i + 1
            if not j == len(self.gd.g_jnt):
                #--- get the guide joints of the selections
                if cmds.objExists(self.gd.g_jnt[j] + '.connection'):
                    if cmds.objExists(self.gd.g_jnt[i] + '.connection'):
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', 
                                     lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #END def __connect_message()

    def __cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['s', 'v'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl[1], 
                      attribute = ['ty','r','s','v'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl[2], 
                      attribute = ['ty','rx','rz','s','v'], 
                      lock = True, show = False)
        if not self.mirrorGuideObj:
            if self.clavicleEnable:
                attr.lockAttr(node = self.clavicle.gd.g_ctl, 
                              attribute = ['s', 'v'], 
                              lock = True, show = False)
            if self.scapulaEnable:
                attr.lockAttr(node = self.scapula.gd.g_ctl, 
                              attribute = ['s', 'v'], 
                              lock = True, show = False)
        cmds.select(clear = True)
    #END def __cleanup()

    def __main_setup(self):
        #--- this method makes use of the MasterMod inheritance        
        self.create(character = self.character,
                    mod = self.mod, 
                    side = self.side,
                    name = self.name,
                    suffix = self.suffix, 
                    size = self.size, 
                    shape = self.shape,
                    orientation = self.orientation,
                    color = self.color,
                    position = self.position,
                    rotation = self.rotation,
                    upVectorOffset = self.upVectorOffset, 
                    aimVector = self.aimVector,
                    upVector = self.upVector,
                    rotateOrder = self.rotateOrder,
                    flip = self.flip,
                    mirrorGuideObj = self.mirrorGuideObj)
        #--- mod specific setup
        self.__arm_setup()
        #--- mod specific cleanup
        self.__cleanup()
    #END def __main_setup()
#END class BipedArmGuide()


class BipedArmPuppet(puppet.Puppet):
    """
    This class creates a biped arm rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).

    @DONE: api mod and class
    @DONE: measure mod and class
    @DONE: poleVector position measure
    @DONE: ikBend
    @DONE: fkBend
    @DONE: armTwist
    @DONE: autoCalvicle
    @DONE: SoftClavicle
    @DONE: autoScapula
    @todo: ikPin
    @todo: fkPin
    @DONE: spaceSwitch for ik fk
    @todo: spaceSwitch in general
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None,
                  fk = True,
                  ik = True,
                  ikfk = 'Blend',
                  ikStretch = True,
                  ikBend = True,
                  armTwist = True,
                  autoClavicle = True,
                  softClavicle = True,
                  autoScapula = True):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedArmPuppet, self).__init__(character = character,
                                             guideObj = guideObj)

        #args
        self.character    = character
        self.guideObj     = guideObj
        self.puppetObj    = puppetObj
        self.fk           = fk
        self.ik           = ik
        self.ikfk         = ikfk
        self.ikStretch    = ikStretch
        self.ikBend       = ikBend
        self.armTwist     = armTwist
        self.autoClavicle = autoClavicle
        self.softClavicle = softClavicle
        self.autoScapula  = autoScapula

        #vars
        self.joints_fk     = list()
        self.joints_ik     = list()

        self.pac           = list()
        self.ocn_fk        = list()

        self.controls_fk   = list()
        self.controls_ik   = list()
        self.rotate_ctl    = list()

        self.ik_handle     = list()
        self.ikfk_blend    = None

        self.bend_ctl      = None
        self.upper_arm_flp = None
        self.lower_arm_flp = None

        self.clavicle      = None
        self.joints_ac     = list()
        self.ik_handle_ac  = list()
        self.mlt           = None
        self.sdk           = None 
        self.scapula       = None

        #methods
        self.__create_puppet()
    #END def __init__()

    def __get_ikfk_joints(self):
        #--- this method gets the skeleton joints and stores them properly
        if self.fk:
            self.joints_fk = duplicate.Duplicate(obj = self.joints[0], 
                                                 replace = ['_JNT', 'FK_JNT']).result

        if self.ik:
            self.joints_ik = duplicate.Duplicate(obj = self.joints[0], 
                                                 replace = ['_JNT', 'IK_JNT']).result
    #END def __get_ikfk_joints()

    def __setup_joints(self):
        #--- this method connects the ik fk joints with the bind one
        attr = attribute.Attribute()
        nd = node.Node()
        if self.fk:
            #--- constraint fk joints to the bind ones
            self.pac = nd.parentConstraint(objA = self.joints_fk,
                                           objB = self.joints,
                                           maintainOffset = False)
            #--- disable skin tag
            for fk in self.joints_fk:
                attr.setAttr(fk, ['SKIN'], 0)
        if self.ik:
            #--- constraint ik joints to the bind ones
            self.pac = nd.parentConstraint(objA = self.joints_ik,
                                           objB = self.joints, 
                                           maintainOffset = False)
            #--- disable skin tag
            for ik in self.joints_ik:
                attr.setAttr(ik, ['SKIN'], 0)
    #END def __setup_joints()

    def __create_fk_controls(self):
        #--- this method creates the fk controls
        #--- fk controls
        for pos in range(len(self.joint_position)-1):
            fk_ctl = control.Control(side = self.side, 
                                     name = (self.mod 
                                             + self.name[pos][0].upper()
                                             + self.name[pos][1:] + 'FK'), 
                                     suffix = 'CTL', 
                                     size = self.size, 
                                     shape = 15, 
                                     color = self.color, 
                                     position = [0,0,0], 
                                     rotation = [0,0,0],
                                     orientation = [0,0,90], 
                                     parent = self.joints_fk[pos],
                                     lockAttrs = ['t','s'])
            cmds.parent(fk_ctl.group, self.side_ctl_grp) 
            self.controls_fk.append(fk_ctl)
    #END def __create_fk_controls()

    def __setup_fk_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- parent the fk controls properly
        ctl = self.controls_fk
        for i in range(len(ctl)):
            j = i + 1
            if not j == len(ctl):
                cmds.parent(ctl[j].group, ctl[i].transform)
                #--- orientConstraint the ctl joints to the controls
                ctl_ocn = nd.orientConstraint(objA = ctl[i].transform,
                                               objB = self.joints_fk[i], 
                                               name = (self.side + '_' + self.mod + 
                                                       self.name[i][0].upper() + 
                                                       self.name[i][1:]), 
                                               maintainOffset = False)[0]
                self.ocn_fk.append(ctl_ocn)
            else:
                #--- orientConstraint the side last joint to the control
                ctl_ocn = nd.orientConstraint(objA = ctl[i].transform,
                                               objB = self.joints_fk[i], 
                                               name = (self.side + '_' + self.mod + 
                                                       self.name[i][0].upper() + 
                                                       self.name[i][1:]), 
                                               maintainOffset = False)[0]
                self.ocn_fk.append(ctl_ocn)

        #--- setup wrist rotation control
        wrist = control.Control(side = self.side, 
                                name = self.mod + 'Rotate',
                                suffix = 'CTL', 
                                size = self.size -0.25, 
                                shape = 2, 
                                color = self.color, 
                                position = [0,0,0], 
                                rotation = [0,0,0],
                                orientation = [0,0,0], 
                                parent = self.joints[-1],
                                lockAttrs = ['t','s'])
        cmds.parent(wrist.group, self.side_ctl_grp)
        nd.parentConstraint(objA = self.joints[-1], 
                            objB = wrist.group, 
                            suffix = 'PAC', 
                            lock = True)
        self.rotate_ctl.append(wrist)
    #END def __setup_fk_controls()

    def __create_ik_controls(self):
        #--- this method creates the ik controls
        attr = attribute.Attribute()
        #--- wrist ik controls
        wrist = control.Control(side = self.side, 
                                name = self.mod + 'TranslateIK',
                                suffix = 'CTL', 
                                size = self.size, 
                                shape = 1, 
                                color = self.color, 
                                position = [0,0,0], 
                                rotation = [0,0,0],
                                orientation = [0,0,0], 
                                parent = self.joints_ik[-1],
                                lockAttrs = ['r','s'])
        cmds.parent(wrist.group, self.side_ctl_grp)
        #--- zero out the rotation
        attr.setAttr(node = wrist.group, 
                     attribute = ['r'], 
                     value = 0)
        self.controls_ik.append(wrist)

        #--- shoulder ik control
        shoulder = control.Control(side = self.side, 
                                   name = self.mod + 'ShoulderIK',
                                   suffix = 'CTL', 
                                   size = self.size, 
                                   shape = 0, 
                                   color = self.color, 
                                   position = [0,0,0], 
                                   rotation = [0,0,0],
                                   orientation = [0,0,90], 
                                   parent = self.joints_ik[0])
        cmds.parent(shoulder.group, self.side_ctl_grp)
        self.controls_ik.append(shoulder)
    #END def __create_ik_controls()

    def __setup_ik_handles(self):
        #--- this method setups the ik handles, parents them under the shoulder
        ik = ikhandle.IkHandle()
        #--- get the shoulder ik controls
        ctl = self.controls_ik[-1]
        self.ik_handle = ik.ikRPsolver(startJoint = self.joints_ik[0], 
                                       endEffector = self.joints_ik[-1], 
                                       side = self.side, 
                                       name = self.mod, 
                                       suffix = 'IK',
                                       parent = ctl.transform,
                                       hide = True)
    #END def __setup_ik_handles()

    def __setup_ik_controls(self):
        #--- this method setups the ik controls
        nd = node.Node()
        #--- get the ik controls
        ctl = self.controls_ik        
        #--- create a pointConstraint of the wrist ik to the ik handle
        nd.pointConstraint(objA = ctl[0].transform, 
                           objB = self.ik_handle[0],
                           suffix = 'PCN', 
                           maintainOffset = False)
        #--- create a parentConstraint of the shoulder ik to the shoulder joint
        nd.parentConstraint(objA = ctl[-1].transform, 
                            objB = self.joints_ik[0],
                            suffix = 'PAC', 
                            maintainOffset = False)
    #END def __setup_ik_controls()

    def __setup_ik_pole_vector(self):
        #--- this method setups the ik pole vector controls
        ap = api.API()
        nd = node.Node()
        #--- get the poleVector position and rotation
        pole_vector = ap.get_pole_vector(jointChain = self.joints_ik)
        pos = pole_vector[0]
        rot = pole_vector[1]
        #--- create the control based on the poleVector position
        self.pole_vector_ctl = control.Control(side = self.side,
                                               name = self.mod + 'ElbowIK',
                                               suffix = 'CTL',
                                               size = self.size - 0.5,
                                               shape = 12,
                                               color = self.color,
                                               position = [pos[0], 
                                                           pos[1], 
                                                           pos[2] - 10],
                                               rotation = rot,
                                               orientation = [0,0,0],
                                               parent = self.side_ctl_grp)
        #--- create poleVector constraint
        nd.poleVectorConstraint(objA = self.pole_vector_ctl.transform, 
                                objB = self.ik_handle[0],
                                suffix = 'PVC')       
    #END def __Setup_ik_pole_vector()

    def __setup_ikfk(self):
        #--- this method creates an ikfk blend or ikfk spaceSwitch
        attr = attribute.Attribute()
        if self.ikfk:
            #--- create a ikfk switch control
            if self.guideObj.flip:
                self.ikfk_blend = control.Control(side = self.side,
                                                  name = self.mod + 'IKFK',
                                                  suffix = 'CTL',
                                                  size = self.size - 0.5,
                                                  shape = 9,
                                                  color = self.color,
                                                  position = [-2,-2,0],
                                                  rotation = [0,0,0],
                                                  orientation = [0,0,-90],
                                                  parent = self.joints[-1])
            else:
                self.ikfk_blend = control.Control(side = self.side,
                                                  name = self.mod + 'IKFK',
                                                  suffix = 'CTL',
                                                  size = self.size - 0.5,
                                                  shape = 9,
                                                  color = self.color,
                                                  position = [2,2,0],
                                                  rotation = [0,0,0],
                                                  orientation = [0,0,90],
                                                  parent = self.joints[-1])
            #--- lock attributes
            attr.lockAll(node = self.ikfk_blend.transform)

            if self.ikfk == 'Blend':
                self.__setup_blend()
    #END def __setup_ikfk()

    def __setup_blend(self):
        #--- this method creates a blending setup between ik and fk
        attr = attribute.Attribute()
        nd = node.Node()
        #--- add an fkik blend attribute
        attr.addAttr(node = self.ikfk_blend.transform,
                     attrName = 'fkIk',
                     attrType = 'float',
                     min = 0,
                     max = 10,
                     default = 10)
        #--- create proper utility nodes to setup ikfk Blend
        mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkFkBlend', 
                                operation = 2,
                                input2X = 10,
                                lockAttr = 'input2X')
        rev = nd.reverse(name = self.side + '_' + self.mod + 'IkFkBlend')
        #--- connect nodes properly
        attr.connectAttr(node = [self.ikfk_blend.transform, mlt], 
                         attribute = ['fkIk', 'input1X'])
        attr.connectAttr(node = [mlt, rev], 
                         attribute = ['outputX', 'inputX'])
        #--- connect the nodes with the parentConstraint weights
        for pac in range(len(self.pac)):
            attr.connectAttr(node = [rev, self.pac[pac]], 
                             attribute = ['outputX', 
                                          self.joints_fk[pac] + 'W0'])
            attr.connectAttr(node = [mlt, self.pac[pac]], 
                             attribute = ['outputX', 
                                          self.joints_ik[pac] + 'W1'])
            #--- set the interpType of the parentConstraint to shortest(2)
            attr.setAttr(node = self.pac[pac], 
                         attribute = 'interpType', 
                         value = 2)
        #--- connect the nodes with the controls' visibility
        #--- ik controls
        attr.connectAttr(node = [mlt, self.controls_ik[0].transform], 
                         attribute = ['outputX', 'visibility'])
        attr.connectAttr(node = [mlt, self.controls_ik[-1].transform], 
                         attribute = ['outputX', 'visibility'])
        attr.connectAttr(node = [mlt, self.pole_vector_ctl.transform], 
                         attribute = ['outputX', 'visibility'])   
        #--- fk controls
        for fk in range(len(self.controls_fk)):
            attr.connectAttr(node = [rev, self.controls_fk[fk].transform], 
                             attribute = ['outputX', 'visibility'])            
    #END def __setup_blend()

    def __setup_ik_joint_stretch(self):
        #--- this method creates an ik squash and stretch setup on ik joints
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the ik joint stretch setup
        for jnt in self.joints_ik[:-1]:
            #--- add stretch attribute
            attr.addAttr(node = jnt, 
                         attrName = 'stretch', 
                         attrType = 'float', 
                         min = 0.001, 
                         max = 100, 
                         default = 1)
            #--- create multiplyDivide nodes
            mlt_div = nd.multiplyDivide(name = jnt.split('_JNT')[0] + 'StretchDiv', 
                                        operation = 2, 
                                        input1X = 1,
                                        lockAttr = 'input1X')
            mlt_pow = nd.multiplyDivide(name = jnt.split('_JNT')[0] + 'StretchPow', 
                                        operation = 3, 
                                        input2X = 0.5,
                                        lockAttr = 'input2X')
            #---  connect the utility nodes with the ik joints
            attr.connectAttr(node = [jnt, mlt_div], 
                             attribute = ['stretch', 'input2X'])
            attr.connectAttr(node = [mlt_div, mlt_pow], 
                             attribute = ['outputX', 'input1X'])
            attr.connectAttr(node = [jnt, jnt],
                             attribute = ['stretch', 'sx'])
            for axis in 'zy':
                attr.connectAttr(node = [mlt_pow, jnt], 
                                 attribute = ['outputX', 's' + str(axis)])
    #END def __setup_ik_joint_stretch()

    def __setup_ik_squash_stretch(self):
        #--- this method creates an ik squash and stretch setup on the ik system
        attr = attribute.Attribute()
        nd = node.Node()
        #--- get the ik controls
        ctl = self.controls_ik
        #--- get the full distance length
        distance = measure.Measure(objects = self.joints_ik).distance
        #--- add stretchy attributes to the ikfk controls
        attr.addAttr(node = self.ikfk_blend.transform, 
                     attrName = 'ikStretch', 
                     attrType = 'float', 
                     min = 0, 
                     max = 1, 
                     default = 0)
        #--- create the utility nodes
        dib = nd.distanceBetween(name = self.side + '_' + self.mod + 'IkStretch', 
                                 suffix = 'DIB',
                                 point1 = ctl[-1].transform,
                                 point2 = ctl[0].transform,
                                 inMatrix1 = ctl[-1].transform,
                                 inMatrix2 = ctl[0].transform)
        mlt_scale = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkStretchGlobalScale',
                                      input2X = distance,
                                      lockAttr = 'input2X')
        mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkStretch', 
                                suffix = 'MLT', 
                                operation = 2)
        cnd = nd.condition(name = self.side + '_' + self.mod + 'IkStretch', 
                           suffix = 'CND', 
                           secondTerm = 1, 
                           operation = 3, 
                           lockAttr = 'secondTerm')
        blc = nd.blendColors(name = self.side + '_' + self.mod + 'IkStretch', 
                             suffix = 'BLC', 
                             color2R = 1, 
                             lockAttr = 'color2R')
        #--- connect the nodes properly
        attr.connectAttr(node = [dib, mlt], 
                         attribute = ['distance', 'input1X'])
        attr.connectAttr(node = [self.main_ctl, mlt_scale], 
                         attribute = ['scaleY', 'input1X'])
        attr.connectAttr(node = [mlt_scale, mlt], 
                         attribute = ['outputX', 'input2X'])
        attr.connectAttr(node = [mlt, cnd], 
                         attribute = ['outputX', 'firstTerm'])
        attr.connectAttr(node = [mlt, cnd], 
                         attribute = ['outputX', 'colorIfTrueR'])
        attr.connectAttr(node = [cnd, blc], 
                         attribute = ['outColorR', 'color1R'])
        attr.connectAttr(node = [self.ikfk_blend.transform, blc], 
                         attribute = ['ikStretch', 'blender'])
        #--- connect the utility node to the joints
        for jnt in self.joints_ik[:-1]:
            attr.connectAttr(node = [blc, jnt], attribute = ['outputR', 'stretch'])
    #END def __setup_ik_squash_stretch()

    def __setup_ik_bend(self):
        #--- this method setups the bendy ik functionality by using flexiplanes
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create bend control
        self.bend_ctl= control.Control(side = self.side, 
                                       name = self.mod + 'Bend', 
                                       suffix = 'CTL', 
                                       size = self.size - 0.25, 
                                       shape = 10, 
                                       color = self.color, 
                                       position = [0,0,0], 
                                       rotation = [0,0,0],
                                       orientation = [0,90,90], 
                                       parent = self.joints_ik[1])
        cmds.parent(self.bend_ctl.group, self.side_ctl_grp)
        #--- parentConstraint the bend control to the elbow joint
        nd.parentConstraint(objA = self.joints[1], 
                            objB = self.bend_ctl.group, 
                            suffix = 'PCN', 
                            maintainOffset = False,
                            lock = True)        
        #--- create the first flexiplane for the humerus bone
        self.upper_arm_flp = flexiplane.FlexiPlane(character = self.character, 
                                                   mod = self.mod, 
                                                   side = self.side, 
                                                   name = 'upperArm', 
                                                   color = self.color, 
                                                   size = self.size - 0.5,
                                                   length = 5,
                                                   constraintTo = [self.joints[0],
                                                                   self.bend_ctl.transform],
                                                   constraintType = 'point', 
                                                   follow = True,
                                                   parent = self.side_extra_grp,
                                                   inheritsTransform = False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        attr.connectAttr(node = [self.bend_ctl.transform,
                                 self.upper_arm_flp.control_up.transform],
                         attribute = ['rotateX', 'rotateX'])
        #--- parentConstraint the main control to the start joint of the humerus
        nd.parentConstraint(objA = self.joints[0], 
                            objB = self.upper_arm_flp.control_main.transform, 
                            suffix = 'PAC', 
                            maintainOffset = True,
                            lock = True)
        #--- create the second flexiplane for the ulna radius bones
        self.lower_arm_flp = flexiplane.FlexiPlane(character = self.character, 
                                                   mod = self.mod, 
                                                   side = self.side, 
                                                   name = 'lowerArm', 
                                                   color = self.color, 
                                                   size = self.size - 0.5,
                                                   length = 5,
                                                   constraintTo = [self.bend_ctl.transform,
                                                                   self.joints[-1]],
                                                   constraintType = 'point', 
                                                   follow = True,
                                                   parent = self.side_extra_grp,
                                                   inheritsTransform = False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        attr.connectAttr(node = [self.bend_ctl.transform,
                                 self.lower_arm_flp.control_down.transform],
                         attribute = ['rotateX', 'rotateX'])        
        #--- parentConstraint the main control to the start joint of the elbow
        nd.parentConstraint(objA = self.joints[1], 
                            objB = self.lower_arm_flp.control_main.transform, 
                            suffix = 'PAC', 
                            maintainOffset = True,
                            lock = True)
        #--- connect the globalScale attr of the flexiplane with the main ctl one
        #--- upper flexiPlane
        attr.connectAttr(node = [self.main_ctl,
                                 self.upper_arm_flp.control_main.transform],
                         attribute = ['globalScale', 'globalScale'])
        #--- lower flexiPlane        
        attr.connectAttr(node = [self.main_ctl,
                                 self.lower_arm_flp.control_main.transform],
                         attribute = ['globalScale', 'globalScale'])
    #END def __setup_ik_bend()

    def __setup_arm_twist(self):
        #--- this method setups the ik twist based on the flexiplane
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- check if a flexiplane exists
        if self.armTwist:
            if not self.ikBend:
                #--- create the second flexiplane for the lowerArm
                twist = flexiplane.FlexiPlane(mod = self.mod, 
                                              side = self.side, 
                                              name = 'lowerArm', 
                                              color = self.color, 
                                              size = self.size - 0.5,
                                              length = 5,
                                              constraintTo = [self.joints[-2],
                                                              self.joints[-1]],
                                              constraintType = 'point', 
                                              follow = True,
                                              parent = self.side_extra_grp)
                #--- parentConstraint the main control to the start joint of the elbow
                nd.parentConstraint(objA = self.joints[1], 
                                    objB = twist.control_main.transform, 
                                    suffix = 'PAC', 
                                    maintainOffset = True,
                                    lock = True)
                #--- lock and hide the mid control of the flexiplane
                attr.lockAll(node = twist.control_mid.transform)
                #--- connect the rotate control with the lowerArm rx
                attr.connectAttr(node=[self.rotate_ctl[0].transform,
                                       twist.control_up.transform], 
                                 attribute = ['rx', 'rx'])
            else:
                #--- connect the rotate control with the lowerArm rx
                attr.connectAttr(node=[self.rotate_ctl[0].transform,
                                       self.lower_arm_flp.control_up.transform], 
                                 attribute = ['rx', 'rx'])                
        else:
            if self.ikBend:                
                #--- lock and hide the controls of the flexiplane
                attr.lockAll(node = self.upper_arm_flp.control_mid.transform)
                attr.lockAll(node = self.upper_arm_flp.control_up.transform)
                attr.lockAll(node = self.upper_arm_flp.control_down.transform)

                attr.lockAll(node = self.lower_arm_flp.control_mid.transform)
                attr.lockAll(node = self.lower_arm_flp.control_up.transform)
                attr.lockAll(node = self.lower_arm_flp.control_down.transform)

                #--- connect the rotate control with the lowerArm rx
                attr.connectAttr(node=[self.rotate_ctl[0].transform,
                                       self.lower_arm_flp.control_up.transform], 
                                 attribute = ['rx', 'rx'])
    #END def __setup_ik_twist()

    def __auto_clavicle_setup(self):
        #--- this method setups the autoClavicle
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- create clavicle puppet
        if self.guideObj.clavicle:
            clav = clavicle.BipedClaviclePuppet(character = self.character, 
                                                guideObj = self.guideObj.clavicle,
                                                autoClavicle = True,
                                                softClavicle = self.softClavicle)
            self.clavicle = clav
            if self.fk:
                #--- unlock necessary attributes
                attr.lockAttr(node = self.controls_fk[0].group, 
                              attribute = 't', 
                              lock = False, 
                              show = True)                
                #--- connect the clavicle with the arm
                nd.pointConstraint(objA = clav.joints[-1], 
                                   objB = self.controls_fk[0].group, 
                                   suffix = 'PCN', 
                                   maintainOffset = False,
                                   lock = True)
                nd.pointConstraint(objA = clav.joints[-1], 
                                   objB = self.joints_fk[0], 
                                   suffix = 'PCN', 
                                   maintainOffset = False,
                                   lock = True)
            if self.ik:
                #--- unlock necessary attributes
                attr.lockAttr(node = self.controls_ik[-1].group, 
                              attribute = 't', 
                              lock = False, 
                              show = True)
                #--- connect the clavicle with the arm
                nd.pointConstraint(objA = clav.joints[-1], 
                                   objB = self.controls_ik[-1].group, 
                                   suffix = 'PCN', 
                                   maintainOffset = False,
                                   lock = True)
            cmds.select(clear = True)

            #--- create the autoClavicle joint setup
            auto_clav_joints = jointchain.IkChain(side = self.side, 
                                                  name = [self.mod + 'AutoClavStart',
                                                          self.mod + 'AutoClavEnd'], 
                                                  suffix = 'JNT', 
                                                  position = [clav.joint_position[0], 
                                                              self.joint_position[-1]], 
                                                  orientation = [[0.0, 0.0, 0.0,], 
                                                                [0.0, 0.0, 0.0]],
                                                  parentJoint = clav.side_extra_grp,
                                                  parentIk = clav.side_extra_grp,
                                                  mirror = False)
            #--- AUTOCLAVICLE SETUP
            self.joints_ac = auto_clav_joints.ik_joint_names
            self.ik_handle_ac = auto_clav_joints.ik_handle_names
            #--- create the poleVector setup
            #--- create a locator
            pole_vector = nd.locator(name = (self.side + '_' + self.mod + 
                                             'AutoClavPoleVector'), 
                                     suffix = 'LOC', 
                                     parent = self.joints_ac[-1])
            cmds.parent(pole_vector, clav.side_extra_grp)
            #--- create poleVectorConstraint
            nd.poleVectorConstraint(objA = pole_vector, 
                                    objB = self.ik_handle_ac[0], 
                                    suffix = 'PVC')
            #--- pointConstraint the locator to the ik control
            nd.pointConstraint(objA = self.controls_ik[0].transform, 
                               objB = pole_vector, 
                               suffix = 'PCN', 
                               maintainOffset = False, 
                               lock = True)
            #--- pointConstraint the ikHandle to the ik control
            nd.pointConstraint(objA = self.controls_ik[0].transform, 
                               objB = self.ik_handle_ac[0], 
                               suffix = 'PCN', 
                               maintainOffset = False, 
                               lock = True)

            #--- SETUP rotation automation of the clavicle
            #--- create a rotation group above the clavicle control
            rot_grp = cmds.group(clav.control.transform, 
                                 name = (clav.control.transform.split('_CTL')[0] + '_SDK'))
            #--- set the group pivot to the controls pivot
            cmds.xform(rot_grp, pivots = clav.joint_position[0], worldSpace = True)

            #--- limit rotations of this SDK group
            cmds.transformLimits(rot_grp, 
                                 enableRotationX = (1,1), 
                                 enableRotationY = (1,0), 
                                 enableRotationZ = (1,0), 
                                 rotationX = (-20,20),
                                 rotationY = (-50,45),
                                 rotationZ = (0,45))                                 
            #--- create nodes for the automation setup
            mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'AutoClavRot',
                                    input2X = 0.9,
                                    input2Y = 0.9,
                                    input2Z = 0.5)
            blc = nd.blendColors(name = self.side + '_' + self.mod + 'AutoClavEnable',
                                 color2R = 0,
                                 color2G = 0,
                                 color2B = 0,
                                 lockAttr = ['color2R',
                                             'color2G',
                                             'color2B'])
            mlt_ikfk = nd.multiplyDivide(name = self.side + '_' + self.mod + 'AutoClavIkFk',
                                         input1X = 0.1,
                                         lockAttr = 'input1X')
            blc_ikfk = nd.blendColors(name = self.side + '_' + self.mod + 'AutoClavIkFk',
                                      color2R = 0,
                                      color2G = 0,
                                      color2B = 0,
                                      lockAttr = ['color2R',
                                                  'color2G',
                                                  'color2B'])
            #--- connect attributes for the automation
            attr.connectAttr(node = [self.joints_ac[0], mlt], 
                             attribute = ['rotate', 'input1'])
            attr.connectAttr(node = [mlt, blc], 
                             attribute = ['output', 'color1'])
            attr.connectAttr(node = [blc, rot_grp], 
                             attribute = ['output', 'rotate'])
            #--- connect the clavicle controls attributes
            attr.connectAttr(node = [self.ikfk_blend.transform, mlt_ikfk], 
                             attribute = ['fkIk', 'input2X'])
            attr.connectAttr(node = [mlt_ikfk, blc_ikfk], 
                             attribute = ['outputX', 'blender'])
            attr.connectAttr(node = [clav.control.transform, blc_ikfk], 
                             attribute = ['autoClavicle', 'color1R'])
            attr.connectAttr(node = [blc_ikfk, blc], 
                             attribute = ['outputR', 'blender'])
            self.mlt = mlt
            self.sdk = rot_grp

            #--- SOFT CLAVICLE SETUP
            if self.softClavicle:
                self.__soft_clavicle_setup()
    #END def __auto_clavicle_setup()

    def __soft_clavicle_setup(self):
        #--- this method creates and setups the softClavicle
        attr = attribute.Attribute()
        nd = node.Node()
        #--- connect the softClavicle joints to the autoClavicle nodes system
        cmds.disconnectAttr(self.joints_ac[0] + '.rotateX', 
                            self.mlt + '.input1X')
        attr.connectAttr(node = [self.clavicle.soft_ry_jnt.ik_joint_names[0],
                                 self.mlt], 
                         attribute = ['rotateY', 'input1Y'])
        attr.connectAttr(node = [self.clavicle.soft_rz_jnt.ik_joint_names[0],
                                 self.mlt], 
                         attribute = ['rotateZ', 'input1Z'])
        #--- constraint the ik control with the translateY and Z locators
        nd.pointConstraint(objA = self.controls_ik[0].transform, 
                           objB = self.clavicle.ty_loc,
                           suffix = 'PCN')
        nd.pointConstraint(objA = self.controls_ik[0].transform, 
                           objB = self.clavicle.tz_loc,
                           suffix = 'PCN')
        #--- connect the clavicles softness attr with the tx of the locators
        attr.connectAttr(node = [self.clavicle.control.transform,
                                 self.clavicle.tyIk_loc], 
                         attribute = ['softness', 'tx'])
        attr.connectAttr(node = [self.clavicle.control.transform,
                                 self.clavicle.tzIk_loc], 
                         attribute = ['softness', 'tx'])
        #--- relimit rotations of the clavicle SDK group
        cmds.transformLimits(self.sdk, 
                             enableRotationX = (1,1), 
                             enableRotationY = (0,0), 
                             enableRotationZ = (0,0), 
                             rotationX = (0,0))
        #--- set the multiplyDivide input2 values of the softClavicle to 1
        attr.setAttr(node = self.mlt, 
                     attribute = ['input2'],
                     value = 1, 
                     lock = True)
    #END def __soft_clavicle_setup()

    def __auto_scapula_setup(self):
        #--- this method creates and setups the autoScapula
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the scapula puppet
        if self.guideObj.scapula:
            scap = scapula.BipedScapulaPuppet(character = self.character, 
                                              guideObj = self.guideObj.scapula)
            self.scapula = scap
            #--- create locators for the autoScapula setup
            target_loc = nd.locator(name = self.side + '_' + scap.mod + 'AutoScapTarget', 
                                    suffix = 'LOC', 
                                    position = [0,22,0], 
                                    worldSpace = True,
                                    parent = scap.side_extra_grp)
            pos_loc = nd.locator(name = self.side + '_' + scap.mod + 'AutoScapPosition', 
                                 suffix = 'LOC', 
                                 position = self.clavicle.joint_position[-1], 
                                 worldSpace = True,
                                 parent = scap.side_extra_grp)
            aim_loc = nd.locator(name = self.side + '_' + scap.mod + 'AutoScapAim', 
                                 suffix = 'LOC',
                                 parent = pos_loc)
            up_loc = nd.locator(name = self.side + '_' + scap.mod + 'AutoScapUp', 
                                suffix = 'LOC', 
                                position = [0,5,0], 
                                worldSpace = False,
                                parent = pos_loc)
            #--- constraint the locators properly
            nd.pointConstraint(objA = self.clavicle.joints[-1], 
                               objB = pos_loc, 
                               suffix = 'PCN', 
                               maintainOffset = False)
            nd.aimConstraint(target = target_loc, 
                             source = aim_loc, 
                             suffix = 'AIM', 
                             worldUpObject = up_loc, 
                             worldUpType = 'object')
            nd.parentConstraint(objA = aim_loc, 
                                objB = scap.joints[0], 
                                suffix = 'PAC')            
    #END def __auto_scapula_setup()

    def __hook_mod_setup(self):
        #--- this method setups the hooks for this module
        attr = attribute.Attribute()
        nd = node.Node()
        #--- unlock necessary groups
        if self.clavicle:
            attr.lockAttr(node = self.clavicle.control.group, 
                          attribute = ['t', 'r'], 
                          lock = False, 
                          show = True)
            #--- parentConstraint the clavicle control groups to the sternum control
            nd.parentConstraint(objA=self.puppetObj.sternum_control.transform, 
                                objB=self.clavicle.control.group , 
                                suffix = 'PAC', 
                                maintainOffset = True, 
                                lock = True)
            #--- parent the clavicle joint to the sternum joint
            cmds.parent(self.clavicle.joints[0], self.puppetObj.joints[-1])
        else:
            attr.lockAttr(node = self.controls_ik[-1].group,
                          attribute = ['t', 'r'], 
                          lock = False, 
                          show = True)
            attr.lockAttr(node = self.controls_fk[0].group,
                          attribute = ['t', 'r'], 
                          lock = False, 
                          show = True)
            #--- parentConstraint the arm control groups to the sternum control
            if self.ik:
                nd.parentConstraint(objA=self.puppetObj.sternum_control.transform, 
                                    objB=self.controls_ik[-1].group , 
                                    suffix = 'PAC', 
                                    maintainOffset = True, 
                                    lock = True)
                cmds.parent(self.joints_ik[0], self.puppetObj.joints[-1])
            if self.fk:
                nd.parentConstraint(objA=self.puppetObj.sternum_control.transform, 
                                    objB=self.controls_fk[-1].group , 
                                    suffix = 'PAC', 
                                    maintainOffset = True, 
                                    lock = True)
                cmds.parent(self.joints_fk[0], self.puppetObj.joints[-1])
            #--- parent the arm joints to the sternum joint
            cmds.parent(self.joints[0],self.puppetObj.joints[-1])
    #END def __hook_mod_setup()

    def __cleanup(self):
        #--- this is the cleanup method
        attr = attribute.Attribute()
        #--- CLEANUP
        #--- hide the extranodes group
        #--- arm
        attr.setAttr(node = [self.side_extra_grp,
                             self.joints_fk[0],
                             self.joints_ik[0]],
                     attribute = 'v', 
                     value = 0)
        #--- clavicle
        if self.guideObj.clavicle:
            attr.setAttr(node = self.clavicle.side_extra_grp,
                         attribute = 'v', 
                         value = 0)
        #--- scapula
        if self.guideObj.scapula:
            try:
                attr.setAttr(node = self.scapula.side_extra_grp, 
                             attribute = 'v', 
                             value = 0)            
            except:
                pass
    #END def __cleanup()

    def __create_puppet(self):
        #--- this is the main create method
        #--- get the bind, fk and ik joints
        self.__get_ikfk_joints()
        #--- setup the ik, fk, bind joints
        self.__setup_joints()
        if self.fk:
            #--- create fk controls
            self.__create_fk_controls()
            #--- setup fk controls
            self.__setup_fk_controls()
        if self.ik:
            #--- create ik controls
            self.__create_ik_controls()
            #--- setup ik handles
            self.__setup_ik_handles()
            #--- setup ik controls
            self.__setup_ik_controls()
            #--- setup ik pole vectors
            self.__setup_ik_pole_vector()
        if self.ik and self.fk:
            #--- setup the ikfk blend
            self.__setup_ikfk()
        if self.ik:
            if self.ikStretch:
                #--- setup ik squash and stretch
                self.__setup_ik_joint_stretch()
                self.__setup_ik_squash_stretch()
            if self.ikBend:
                #--- setup bendy ik system
                self.__setup_ik_bend()
            #--- setup the arm twist
            self.__setup_arm_twist()
        if self.autoClavicle:
            #--- create the autoClavicle
            self.__auto_clavicle_setup()
            #--- create the autoScapula
            if self.autoScapula:
                self.__auto_scapula_setup()
        #--- hook setup
        self.__hook_mod_setup()
        #--- cleanup the mod
        self.__cleanup()
    #END def __create_puppet()
#END class BipedArmPuppet()


class QuadrupedArmGuide(mod.MasterMod):
    """
    This class creates a quadruped arm guide system based on the specification 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'arm',
                  side = 'L',
                  name = ['humerus', 'elbow', 'cannon', 'fetlock'],
                  size = 0.75,
                  shape = 2, 
                  color = 6, 
                  position = [[2.5, 15, 8], 
                              [2.5, 12, 6],
                              [2.5, 7, 6],
                              [2.5, 3, 5]],
                  clavicle = False,
                  scapula = True,
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedArmGuide, self).__init__()

        #vars

        #methods
        self.__main_setup(character = character,
                          mod = mod, 
                          side = side, 
                          name = name, 
                          size = size,
                          shape = shape, 
                          color = color, 
                          position = position,
                          clavicle = clavicle,
                          scapula = scapula,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #END def __init__()

    def __arm_setup(self,
                     character = None,
                     mod = None,
                     side = None,
                     name = None,
                     size = 1,
                     shape = 0, 
                     color = 0, 
                     position = [0,0,0],
                     clavicle = True,
                     scapula = True,
                     upVectorOffset = [0,6,0],
                     aimVector = [1,0,0],
                     upVector = [0,1,0],
                     mirror = True):
        #--- this method is a mod specific setup
        #--- unlock the proper groups to work with them
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)
        #--- pointConstraint the elbowGuide to the other ones
        nd = node.Node()
        nd.pointConstraint(objA = [self.gd.g_ctl[0], self.gd.g_ctl[2]], 
                           objB = self.gd.g_grp[1],
                           name = side + '_' + mod + name[1].capitalize())
        #--- parent the controls to the shoulder ctl
        cmds.parent(self.gd.g_grp[1:-1], self.gd.g_ctl[0])
        cmds.parent(self.gd.g_grp[-1], self.gd.g_ctl[-2])
        #--- create the message connection setup
        self.__connect_message()

        #--- check for clavicle setup
        if clavicle:
            #--- get the proper position values for the clavicle
            #--- offset the first position x value by 2
            clav_pos = [[position[0][0] - 3, position[0][1], position[0][2]],
                        position[0]]
            self.__arm_clavicle_setup(character = character)

        #--- check for scapula setup
        if scapula:
            #--- get the proper position values for the scapula
            #--- offset the first position x value by 2
            scap_pos = [[position[0][0], position[0][1] -1, position[0][2] -1],
                        [position[0][0] -2, position[0][1] -3, position[0][2] -1]]
            self.__arm_scapula_setup(character = character, 
                                     upVectorOffset = upVectorOffset,
                                     aimVector = aimVector,
                                     upVector = upVector,
                                     mirror = mirror)
    #END def __arm_setup()

    def __arm_clavicle_setup(self,
                               character = None):
        #--- this method calls the clavicle mod
        self.clavicle = clavicle.QuadrupedClavicleGuide(character = character, 
                                                    size = 0.5,
                                                    position = position)        
        hook.Hook(mod = 'clavicle', 
                  hookParent = self.gd.g_ctl[0], 
                  hookChild = self.clavicle.gd.g_grp[-1], 
                  hookType = 'pointConstraint')        
    #END def __arm_clavicle_setup()

    def __arm_scapula_setup(self,
                              character = None,
                              upVectorOffset = [6,0,0],
                              aimVector = [1,0,0],
                              upVector = [0,1,0],                          
                              mirror = True):
        #--- this method calls the scapula mod
        self.scapula = scapula.QuadrupedScapulaGuide(character = character,
                                                     upVectorOffset = upVectorOffset,
                                                     aimVector = aimVector,
                                                     upVector = upVector)
        #--- connect the mouth guides properly regarding the mirror boolean
        self.__connect_guides(mod = self.scapula.gd.mod, 
                              side = self.scapula.gd.side,
                              obj = [self.scapula.gd.g_jnt[0], 
                                     self.gd.g_jnt[0]], 
                              position = [self.scapula.gd.position, 
                                          self.gd.position[0]])
        if mirror:
            self.__connect_guides(mod = self.scapula.gd.mod, 
                                  side = self.scapula.gd.mirror_side,
                                  obj = [self.scapula.gd.mirror_ctl[0], 
                                         self.gd.mirror_ctl[0]], 
                                  position = [self.scapula.gd.mirror_pos[0],
                                              self.gd.mirror_pos[0]])
        #--- unlock the proper groups to work with them
        attr = attribute.Attribute()
        attr.lockAttr(node = self.scapula.gd.g_jnt_off, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)            
        #--- create the proper joint aim constraint
        nd = node.Node()
        nd.aimConstraint(target = self.gd.g_jnt[0], 
                         source = self.scapula.gd.g_jnt_off[0],
                         aimVector = aimVector, 
                         upVector = upVector, 
                         worldUpObject = self.scapula.gd.g_loc[0], 
                         worldUpType = 'object')
        #--- hook the leg guide to the scapula
        hook.Hook(mod = 'scapula', 
                  hookParent = self.scapula.gd.g_ctl[0], 
                  hookChild = self.gd.g_grp[0]) 
    #END def __arm_scapula_setup()

    def __connect_guides(self, 
                           mod = None, 
                           side = None,
                           obj = None, 
                           position = [0,0,0]):
        #--- this method creates the curve which connects the guide controls
        crv = cmds.curve(degree = 1, point = position)
        cmds.parent(crv, self.gd.extras)
        crvShp = cmds.listRelatives(crv, allDescendents = True)[0]
        crvShp = cmds.rename(crvShp, crv + 'Shape')
        shape = cmds.listRelatives(crv, allDescendents = 1)[0]

        #--- connect the cvs to the controls by matrix
        attr = attribute.Attribute()
        nd   = node.Node()
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, shape], 
                             attribute = ['outputTranslate', 
                                          'controlPoints[' + `i` + ']'])
        #--- set the displayType of the curve Shape to template
        attr.setColor(node = crvShp, displayType = 1)
    #END def __connect_guides()

    def __connect_message(self):
        #--- this method connects the message attributes between the joints
        #--- unlock all necessary attributes from specified nodes
        attr = attribute.Attribute()
        #--- create the message connections
        for i in range(len(self.gd.g_jnt)):
            j = i + 1
            if not j == len(self.gd.g_jnt):
                #--- get the guide joints of the selections
                if cmds.objExists(self.gd.g_jnt[j] + '.connection'):
                    if cmds.objExists(self.gd.g_jnt[i] + '.connection'):
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', 
                                     lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #END def __connect_message()

    def __arm_cleanup(self, 
                       clavicle = True,
                       scapula = True):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_ctl[1:], 
                      attribute = ['tx', 'r', 's', 'v'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['s', 'v'], 
                      lock = True, show = False)
        if clavicle:
            attr.lockAttr(node = self.clavicle.gd.g_ctl, 
                          attribute = ['s', 'v'], 
                          lock = True, show = False)
        if scapula:
            attr.lockAttr(node = self.scapula.gd.g_ctl, 
                          attribute = ['s', 'v'], 
                          lock = True, show = False)
        cmds.select(clear = True)
    #END def arm_cleanup()

    def __main_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      clavicle = True,
                      scapula = True,
                      upVectorOffset = [0,6,0],
                      aimVector = [1,0,0],
                      upVector = [0,1,0],
                      mirror = True):
        #--- this method makes use of the MasterMod inheritance        
        self.create(character = character,
                    mod = mod, 
                    side = side,
                    name = name, 
                    size = size, 
                    shape = shape, 
                    color = color,
                    position = position,
                    upVectorOffset = upVectorOffset, 
                    aimVector = aimVector,
                    upVector = upVector,
                    mirror = mirror)
        #--- mod specific setup
        self.__arm_setup(character = character,
                         mod = mod, 
                         side = side,
                         name = name, 
                         size = size, 
                         shape = shape, 
                         color = color,
                         position = position,
                         clavicle = clavicle,
                         scapula = scapula,
                         upVectorOffset = upVectorOffset, 
                         aimVector = aimVector,
                         upVector = upVector,
                         mirror = mirror)
        #--- mod specific cleanup
        self.__arm_cleanup(clavicle = clavicle,
                           scapula = scapula)
    #END def __main_setup()
#END class QuadrupedArmGuide()

