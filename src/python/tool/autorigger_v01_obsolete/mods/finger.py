'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Finger module with different finger classes
'''

import string
from maya import cmds
from fundamentals import attribute, duplicate, node
from functions import control, hook, puppet
from mods import hand, mod
reload(attribute)
reload(control)
reload(duplicate)
reload(hand)
reload(hook)
reload(mod)
reload(node)
reload(puppet)


class BipedFingerGuide(mod.MasterMod):
    """
    This class creates a biped finger guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'finger',
                  side = 'L',
                  name = 'index',
                  suffix = 'GCTL',
                  size = 0.25,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 15,
                  position = [[1,0,0],[2,0,0],[3,0,0],[4,0,0]], 
                  rotation = [0,0,0],
                  upVectorOffset = [0,6,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None,
                  parent = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedFingerGuide, self).__init__()

        #args
        self.character      = character
        self.mod            = mod
        self.side           = side
        self.name           = name
        self.suffix         = suffix
        self.size           = size
        self.shape          = shape
        self.orientation    = orientation 
        self.color          = color
        self.position       = position
        self.rotation       = rotation
        self.upVectorOffset = upVectorOffset
        self.aimVector      = aimVector
        self.upVector       = upVector
        self.rotateOrder    = rotateOrder
        self.flip           = flip
        self.mirrorGuideObj = mirrorGuideObj
        self.parent         = parent

        #vars
        self.original_name  = name

        #methods
        self.__main_setup()
    #END def __init__()

    def __finger_setup(self):
        #--- this method creates the finger guides and setup them properly
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the finger guide controls
        guide_names    = []
        for p in range(len(self.position)):
            #--- create an alphabetical iterator
            abc = string.uppercase
            #--- create the guide names
            guide_names.append(self.name + abc[p])
        self.name = guide_names
        if self.mirrorGuideObj:
            self.upVectorOffset = [0,-6,0]
            self.upVector = [0,-1,0]
        #--- create the guides
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

        #--- unlock all necessary attributes from specified nodes
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False,
                      show = True)

        if not self.mirrorGuideObj:
            #--- parent the controls fk style
            for i in range(len(self.gd.g_grp)):
                j = i + 1
                if not j == len(self.gd.g_grp):
                    cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])

        #--- parent the first index to the given parent object
        if self.parent:
            if self.mirrorGuideObj:
                try:
                    #--- hook the finger guide to the hand
                    hook.Hook(mod = self.parent, 
                              hookParent = self.parent, 
                              hookChild = self, 
                              hookType = None,
                              hookMessage = False)
                except:
                    pass
            else:
                try:
                    #--- hook the finger guide to the hand
                    hook.Hook(mod = self.parent, 
                              hookParent = self.parent, 
                              hookChild = self, 
                              hookType = 'parentConstraint',
                              hookMessage = False)
                except:
                    pass
        #--- connect messages
        self.__connect_message()               
        #--- mod specific cleanup
        self.__cleanup()                        
    #END def __finger_setup()

    def __connect_message(self):
        #--- this method connects the message attributes between the joints
        #--- create the message connections
        for i in range(len(self.gd.g_jnt)):
            j = i + 1
            if not j == len(self.gd.g_jnt):
                #--- get the guide joints of the selections
                if cmds.objExists(self.gd.g_jnt[j] + '.connection'):
                    if cmds.objExists(self.gd.g_jnt[i] + '.connection'):
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #END def __connect_message()

    def __cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)
        attr.lockAttr(node = self.gd.g_ctl[1:], 
                      attribute = ['tz'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl, 
                      attribute = ['s', 'v'], 
                      lock = True, show = False)
        cmds.select(clear = True)
    #END def __cleanup()

    def __main_setup(self):
        #--- this method makes use of the MasterMod inheritance        
        #--- mod specific setup
        self.__finger_setup()
    #END def __main_setup()
#END class BipedFingerGuide()


class BipedFingerPuppet(puppet.Puppet):
    """
    This class creates a biped finger rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None,
                  curlEnable = True,
                  spreadEnable = True,
                  spreadValue = 0,
                  twistEnable = True):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedFingerPuppet, self).__init__(character = character,
                                                guideObj = guideObj)

        #args
        self.character = character
        self.guideObj  = guideObj
        self.puppetObj = puppetObj

        #vars
        self.controls_finger = list()
        self.finger_grp      = list()
        self.spread_grp      = list()
        self.pac             = list()

        #methods
        self.__create_puppet()
    #END def __init__()

    def __get_fk_joints(self):
        #--- this method gets the skeleton joints and stores them properly
        self.joints_fk = duplicate.Duplicate(obj = self.joints[0], 
                                             replace = ['_JNT', 'FK_JNT']).result
    #END def __get_fk_joints()

    def __setup_joints(self):
        #--- this method connects the ik fk joints with the bind one
        attr = attribute.Attribute()
        nd = node.Node()
        #--- constraint fk joints to the bind ones
        self.pac = nd.parentConstraint(objA = self.joints_fk,
                                       objB = self.joints,
                                       maintainOffset = False)
        #--- connect the bind joints to the last joint of the puppetObj
        cmds.parent(self.joints[0], self.puppetObj.joints[-1])
        #--- disable skin tag
        for fk in self.joints_fk:
            attr.setAttr(fk, ['SKIN'], 0)        
    #END def __setup_joints()

    def __create_fk_controls(self):
        #--- this method creates the fk controls
        #--- fk controls
        for pos in range(len(self.joint_position)-1):
            name = (self.mod + self.name[pos][0].upper() + self.name[pos][1:])                
            ctl = control.Control(side = self.side, 
                                  name = name, 
                                  suffix = 'CTL', 
                                  size = self.size/1.5, 
                                  shape = 15, 
                                  color = self.guideObj.color, 
                                  position = [0,0,0], 
                                  rotation = [0,0,0],
                                  orientation = [0,0,90], 
                                  parent = self.joints_fk[pos],
                                  lockAttrs = ['t','s'])
            cmds.parent(ctl.group, self.side_ctl_grp) 
            self.controls_finger.append(ctl)
            #--- create a spread group on top of the control
            off = cmds.group(ctl.transform, name = self.side + '_' + name + 'Spread_GRP')
            self.spread_grp.append(off)
            #--- create another group on top of the spread group
            grp = cmds.group(off, name = self.side + '_' + name + 'Finger_GRP')
            self.finger_grp.append(grp)
    #END def __create_fk_controls()

    def __setup_fk_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- parent the fk controls properly
        ctl = self.controls_finger
        for i in range(len(ctl)):
            j = i + 1
            if not j == len(ctl):
                cmds.parent(ctl[j].group, ctl[i].transform)
                #--- parentConstraint the ctl joints to the controls
                pac = nd.parentConstraint(objA = ctl[i].transform,
                                          objB = self.joints_fk[i], 
                                          name = (self.side + '_' + self.mod + 
                                                  self.name[i][0].upper() + 
                                                  self.name[i][1:]), 
                                          maintainOffset = False)[0]
                self.pac.append(pac)
            else:
                #--- parentConstraint the side last joint to the control
                pac = nd.parentConstraint(objA = ctl[i].transform,
                                          objB = self.joints_fk[i], 
                                          name = (self.side + '_' + self.mod + 
                                                  self.name[i][0].upper() + 
                                                  self.name[i][1:]), 
                                          maintainOffset = False)[0]
                self.pac.append(pac)
        #--- parentConstraint the first finger fk control to the rotate control
        nd.parentConstraint(objA=self.puppetObj.rotate_ctl[0].transform,
                            objB=ctl[0].group)
    #END def __setup_fk_controls()

    def __add_finger_attributes(self):
        #--- this method adds the foot roll attributes
        attr = attribute.Attribute()
        #--- finger controls
        finger_ctl = self.puppetObj.ikfk_blend
        name = (self.mod + self.name[0][0].upper() + self.name[0][1:])
        #--- finger name
        attr.addAttr(node = finger_ctl.transform,
                     attrName = self.guideObj.original_name,
                     attrType = 'enum',
                     enum = ['       '])
        attr.lockAttr(node = finger_ctl.transform, 
                      attribute = [self.guideObj.original_name], 
                      show = True)
        #--- curl attribute
        for iter in range(len(self.guideObj.name)-1):
            attr_name = self.guideObj.name[iter] + '_Curl'
            attr.addAttr(node = finger_ctl.transform,
                         attrName = attr_name,
                         attrType = 'float')
            attr.connectAttr(node = [finger_ctl.transform, self.finger_grp[iter]],
                             attribute = [attr_name, 'rz'])
        #--- swivel attribute
        for iter in range(len(self.guideObj.name)-1):
            attr_name = self.guideObj.name[iter] + '_Swivel'
            attr.addAttr(node = finger_ctl.transform,
                         attrName = attr_name,
                         attrType = 'float')
            attr.connectAttr(node = [finger_ctl.transform, self.finger_grp[iter]],
                             attribute = [attr_name, 'ry'])
        #--- twist attribute
        for iter in range(len(self.guideObj.name)-1):
            attr_name = self.guideObj.name[iter] + '_Twist'
            attr.addAttr(node = finger_ctl.transform,
                         attrName = attr_name,
                         attrType = 'float')
            attr.connectAttr(node = [finger_ctl.transform, self.finger_grp[iter]],
                             attribute = [attr_name, 'rx'])
        #--- finger visibility
        attr_name = self.guideObj.original_name + 'ShowControls'
        attr.addAttr(node = finger_ctl.transform,
                     attrName = attr_name,
                     attrType = 'short',
                     min = 0,
                     max = 1,
                     keyable = False,
                     channelBox = True)
        attr.connectAttr(node = [finger_ctl.transform, 
                                 self.controls_finger[0].transform],
                         attribute = [attr_name, 'v'])
    #END def __add_finger_attributes()

    def __create_puppet(self):
        #--- this is the main create method
        #--- get the bind, fk and ik joints
        self.__get_fk_joints()
        #--- setup fk and bind joints
        self.__setup_joints()
        #--- create fk controls
        self.__create_fk_controls()
        #--- setup fk controls
        self.__setup_fk_controls()
        #--- add_finger_attributes()
        self.__add_finger_attributes()
    #END def __create_puppet()
#END class BipedFingerPuppet()