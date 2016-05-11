'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Neck module with different neck classes
'''

from maya import cmds
from fundamentals import attribute, duplicate, node
from functions import control, hook, puppet
from mods import mod
reload(attribute)
reload(control)
reload(duplicate)
reload(hook)
reload(mod)
reload(node)
reload(puppet)


class BipedNeckGuide(mod.MasterMod):
    """
    This class creates a biped neck guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'neck',
                  side = 'C',
                  name = ['cervicalVertebraeA', 
                          'cervicalVertebraeB'],
                  suffix = 'GCTL',
                  size = 0.25,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 22, 
                  position = [[0,21,0],[0,22,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [-6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedNeckGuide, self).__init__()

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

        #methods
        self.__main_setup()
    #end def __init__()

    def __neck_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()        
        #--- unlock all necessary attributes from specified node
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False, show = True)        
        #--- parent the guides in fk style
        for i in range(len(self.gd.g_grp)):
            j = i + 1
            if not j == len(self.gd.g_grp):
                cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])
        #--- create the message connection setup
        self.__connect_message()
    #end def __neck_setup()

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
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #end def __connect_message()

    def __neck_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()        
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)              
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['tx', 'ry','rz'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __neck_cleanup()

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
                    flip = self.flip)
        #--- mod specific setup        
        self.__neck_setup()
        #--- mod specific cleanup
        self.__neck_cleanup()
    #end def __main_setup()
#end class BipedNeckGuide()


class BipedNeckPuppet(puppet.Puppet):
    """
    This class creates a biped neck rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedNeckPuppet, self).__init__(character = character,
                                              guideObj = guideObj)

        #args
        self.character = character
        self.guideObj  = guideObj
        self.puppetObj = puppetObj

        #vars
        self.controls_neck = list()

        #methods
        self.__create_puppet()
    #end def __init__()

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
        for pos in range(len(self.joint_position)):
            name = (self.mod + self.name[pos][0].upper() + self.name[pos][1:])                
            ctl = control.Control(side = self.side, 
                                  name = name, 
                                  suffix = 'CTL', 
                                  size = self.size + 0.5, 
                                  shape = 9, 
                                  color = self.guideObj.color, 
                                  position = [0,0,0], 
                                  rotation = [0,0,0],
                                  orientation = [0,-90,90], 
                                  parent = self.joints_fk[pos],
                                  lockAttrs = ['t','s'])
            cmds.parent(ctl.group, self.side_ctl_grp) 
            self.controls_neck.append(ctl)
    #END def __create_fk_controls()

    def __setup_fk_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- parent the fk controls properly
        ctl = self.controls_neck
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
                                          maintainOffset = True)[0]
                self.pac.append(pac)
            else:
                #--- parentConstraint the side last joint to the control
                pac = nd.parentConstraint(objA = ctl[i].transform,
                                          objB = self.joints_fk[i], 
                                          name = (self.side + '_' + self.mod + 
                                                  self.name[i][0].upper() + 
                                                  self.name[i][1:]), 
                                          maintainOffset = True)[0]
                self.pac.append(pac)
        #--- parentConstraint the first fk control to the sternum control
        nd.parentConstraint(objA=self.puppetObj.sternum_control.transform,
                            objB=ctl[0].group)
    #END def __setup_fk_controls()

    def __create_puppet(self):
        #--- this is the main create method
        #--- get the fk and bind joints
        self.__get_fk_joints()
        #--- setup fk and bind joints
        self.__setup_joints()
        #--- create fk controls
        self.__create_fk_controls()
        #--- setup fk controls
        self.__setup_fk_controls()
    #END def __create_puppet()
#END class BipedNeckPuppet()


class QuadrupedNeckGuide(mod.MasterMod):
    """
    This class creates a quadruped neck guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'neck',
                  side = 'C',
                  name = ['cervicalVertebraeA', 
                          'cervicalVertebraeB', 
                          'cervicalVertebraeC',
                          'cervicalVertebraeD',
                          'cervicalVertebraeE',
                          'cervicalVertebraeF'],
                  size = 0.25,
                  shape = 2, 
                  color = 17, 
                  position = [[0.0, 15, 8] ,
                              [0.0, 17, 9.25] ,
                              [0.0, 19, 10] ,
                              [0.0, 21, 10.5] ,
                              [0.0, 22.5, 11.5] ,
                              [0.0, 24, 13]],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedNeckGuide, self).__init__()
        
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
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #end def __init__()

    def __neck_setup(self,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      upVectorOffset = [6,0,0],
                      aimVector = [0,1,0],
                      upVector = [1,0,0],
                      mirror = True):
        #--- this method is a mod specific setup
        #--- unlock all necessary attributes from specified nodes
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False, show = True)        
        #--- parent the guides in fk style
        for i in range(len(self.gd.g_grp)):
            j = i + 1
            if not j == len(self.gd.g_grp):
                cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])
        #--- create the message connection setup
        self.__connect_message()                                          
    #end def __neck_setup()

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
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #end def __connect_message()

    def __neck_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)              
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['tx', 'ry','rz'])
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __neck_cleanup()

    def __main_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      upVectorOffset = [6,0,0],
                      aimVector = [0,1,0],
                      upVector = [1,0,0],
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
        self.__neck_setup(mod = mod, 
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
        #--- mod specific cleanup
        self.__neck_cleanup()
    #end def __main_setup()
#end class QuadrupedNeckGuide()
