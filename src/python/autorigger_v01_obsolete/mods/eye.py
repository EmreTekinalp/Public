'''
Created on 19.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Eye module with different eye classes
'''

from maya import cmds
from fundamentals import attribute, duplicate, ikhandle, node
from functions import control, hook, puppet
from mods import mod
reload(attribute)
reload(control)
reload(duplicate)
reload(ikhandle)
reload(hook)
reload(mod)
reload(node)
reload(puppet)


class BipedEyeGuide(mod.MasterMod):
    """
    This class creates a biped eye guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'eye',
                  side = 'L',
                  name = ['ball', 'pupil'],
                  suffix = 'GCTL',
                  size = 0.20,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 15,
                  position = [[1,26,2],[1,26,2.5]],
                  rotation = [0,0,0],
                  upVectorOffset = [6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None,
                  parent = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedEyeGuide, self).__init__()

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

        #methods
        self.__main_setup()
    #end def __init__()

    def __eye_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()  
        #--- unlock all necessary attributes from specified nodes
        if not self.mirrorGuideObj:
            attr.lockAttr(node = self.gd.g_grp, 
                          attribute = ['t', 'r', 's'], 
                          lock = False, show = True)        
            #--- parent the guides properly
            for i in range(len(self.gd.g_grp)):
                j = i + 1
                if not j == len(self.gd.g_grp):
                    cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])

        #--- parent the first guide to the given parent object
        if self.parent:
            if self.mirrorGuideObj:
                try:
                    #--- hook the finger guide to the hand
                    hook.Hook(mod = self.parent, 
                              hookParent = self.parent, 
                              hookChild = self, 
                              hookType = None,
                              hookMessage = False,
                              hookParentIndex=0)
                except:
                    pass
            else:
                try:
                    #--- hook the guide to the parent
                    hook.Hook(mod = self.parent, 
                              hookParent = self.parent, 
                              hookChild = self, 
                              hookType = 'parentConstraint',
                              hookMessage = False,
                              hookParentIndex=0)
                except:
                    pass

        #--- connect messages
        self.__connect_message() 
    #end def __eye_setup()

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
    #end def __connect_message()

    def __eye_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)        
#        attr.lockAttr(node = self.gd.g_ctl[1:], attribute = ['tx'])
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __eye_cleanup()

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
        #--- create eye setup
        self.__eye_setup()
        #--- cleanup the mod
        self.__eye_cleanup()
    #end def __main_setup
#end class BipedEyeGuide()


class BipedEyePuppet(puppet.Puppet):
    """
    This class creates a biped eye rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedEyePuppet, self).__init__(character = character,
                                             guideObj = guideObj)

        #args
        self.character = character
        self.guideObj  = guideObj
        self.puppetObj = puppetObj

        #vars
        self.control_eyes = None
        self.control_eye  = None

        #methods
        self.__create_puppet()
    #end def __init__()

    def __setup_joints(self):
        #--- this method setups the eye joints
        attr = attribute.Attribute()
        #--- parent the first eye joint to the joint of the puppetObj
        cmds.parent(self.joints[0], self.puppetObj.joints[0])
        #--- disable skin tag on last joint
        attr.setAttr(self.joints[-1], ['SKIN'], 0)        
    #END def __setup_joints()

    def __create_eye_controls(self):
        #--- this method creates the eye controls
        attr = attribute.Attribute()
        #--- main eye control
        name = self.mod + 'Main'
        if not cmds.objExists('C_' + name + '_CTL'):
            ctl = control.Control(side = 'C', 
                                  name = name, 
                                  suffix = 'CTL', 
                                  size = self.size, 
                                  shape = 1, 
                                  color = 17, 
                                  position = [0,0,0], 
                                  rotation = [0,0,0],
                                  offset = [0,0,0],
                                  orientation = [0,0,90], 
                                  parent = self.joints[0],
                                  lockAttrs = ['s', 'r'])
            cmds.parent(ctl.group, world = True)
            attr.setAttr(node = ctl.group, attribute = 'tx', value = 0)
            attr.setAttr(node = ctl.group, attribute = 'tz', value = 20)            
            cmds.parent(ctl.group, self.puppetObj.control_head.transform) 
            self.control_eyes = ctl
        else:
            self.control_eyes= 'C_' + name + '_CTL'

        #--- jaw control
        name = self.mod + self.name[0][0].upper() + self.name[0][1:]
        ctl = control.Control(side = self.side, 
                              name = name, 
                              suffix = 'CTL', 
                              size = self.size, 
                              shape = 0, 
                              color = self.guideObj.color, 
                              position = [0,0,0], 
                              rotation = [0,0,0],
                              offset = [0,0,0],
                              orientation = [0,0,90], 
                              parent = self.joints[0],
                              lockAttrs = ['s', 'r'])
        try:
            cmds.parent(ctl.group, self.control_eyes.transform)
            cmds.setAttr(ctl.group +'.tx', 0)
        except:
            cmds.parent(ctl.group, self.control_eyes)
        attr.setAttr(ctl.group, ['tx'], 0)
        self.control_eye = ctl
    #END def __create_head_controls()

    def __setup_eye_controls(self):
        #--- this method setups the eye controls
        ik = ikhandle.IkHandle()
        attr = attribute.Attribute()
        #--- create ikHandles for the eye joints and parent it under the control
        ikh = ik.ikSCsolver(startJoint = self.joints[0], 
                            endEffector = self.joints[1], 
                            side = self.side, 
                            name = self.mod, 
                            suffix = 'IK', 
                            parent = self.control_eye.transform, 
                            hide = True)
        attr.setAttr(ikh[0], ['t'], 0)
    #END def __setup_eye_controls()

    def __create_puppet(self):
        #--- this is the main create method
        #--- setup eye joints
        self.__setup_joints()
        #--- create eye controls
        self.__create_eye_controls()
        #--- setup eye controls
        self.__setup_eye_controls()
    #END def __create_puppet()
#END class BipedEyePuppet()


class QuadrupedEyeGuide(mod.MasterMod):
    """
    This class creates a quadruped eye guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'eye',
                  side = 'L',
                  name = ['base', 'pupil'],
                  size = 0.20,
                  shape = 2, 
                  color = 6, 
                  position = [[1,22,15],
                              [1,22,16]],
                  eyesAmount = 1,
                  upVectorOffset = [0,0,6],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedEyeGuide, self).__init__()

        #vars
        self.jnt        = []
        self.ctl        = []
        self.grp        = []
        self.mirror_ctl = []
        self.mirror_pos = []

        #methods
        self.__main_setup(character = character,
                          mod = mod, 
                          side = side, 
                          name = name, 
                          size = size,
                          shape = shape, 
                          color = color, 
                          position = position,
                          eyesAmount = eyesAmount,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #end def __init__()

    def __eye_offset(self,
                      position = [0,0,0],
                      eyesAmount = 1):
        #--- this method creates an eyesAmount offset
        self.position = []
        for e in range(eyesAmount):
            tmp = []
            for p in range(len(position)):
                pos = [position[p][0], position[p][1] + e, position[p][2]]
                tmp.append(pos)
            self.position.append(tmp)
    #end def ___eye_offset()

    def __eye_setup(self,
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
        #--- parent the guides properly
        for i in range(len(self.gd.g_grp)):
            j = i + 1
            if not j == len(self.gd.g_grp):
                cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])
        #--- connect messages
        self.__connect_message()
    #end def __eye_setup()

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
    #end def __connect_message()

    def __eye_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls        
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)        
        attr.lockAttr(node = self.gd.g_ctl[1:], attribute = ['tx'])
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __eye_cleanup()

    def __main_setup(self,
                       character = None,
                       mod = None,
                       side = None,
                       name = None,
                       size = 1,
                       shape = 0, 
                       color = 0, 
                       position = [0,0,0],
                       eyesAmount = 1,
                       upVectorOffset = [6,0,0],
                       aimVector = [0,1,0],
                       upVector = [1,0,0],
                       mirror = True):
        #--- this method makes use of the MasterMod inheritance
        self.__eye_offset(eyesAmount = eyesAmount, 
                          position = position)
        if eyesAmount:
            for iter in range(eyesAmount):
                self.create(character = character,
                            mod = mod, 
                            side = side, 
                            name = name, 
                            size = size,
                            shape = shape, 
                            color = color, 
                            position = self.position[iter],
                            upVectorOffset = upVectorOffset, 
                            aimVector = aimVector,
                            upVector = upVector,
                            mirror = mirror)
                self.jnt.append(self.gd.g_jnt)
                self.ctl.append(self.gd.g_ctl)
                self.grp.append(self.gd.g_grp)
                self.mirror_ctl.append(self.gd.mirror_ctl)
                self.mirror_pos.append(self.gd.mirror_pos)
                #--- mod specific setup         
                self.__eye_setup(mod = mod, 
                                 side = side, 
                                 name = name, 
                                 size = size,
                                 shape = shape, 
                                 color = color, 
                                 position = self.position[iter],
                                 upVectorOffset = upVectorOffset, 
                                 aimVector = aimVector,
                                 upVector = upVector,
                                 mirror = mirror)
                self.__eye_cleanup()
        else:
            print 'EyesAmount is 0. You have to specify at least an amount of 1!'
    #end def __main_setup
#end class QuadrupedEyeGuide()