'''
Created on 17.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Hip module with different hip classes
'''

from maya import cmds
from fundamentals import attribute, duplicate, node
from functions import control, jointchain, puppet
from mods import mod
reload(attribute)
reload(control)
reload(duplicate)
reload(jointchain)
reload(mod)
reload(node)
reload(puppet)


class BipedHipGuide(mod.MasterMod):
    
    """
    This class creates a biped hip guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'hip',
                  side = 'L',
                  name = 'pelvis',
                  suffix = 'GCTL',
                  size = 0.75,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 6, 
                  position = [1,11,0],
                  rotation = [0,0,0],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,0,1],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedHipGuide, self).__init__()

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

        #methods
        self.__main_setup()
    #end def __init__()

    def __hip_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAttr(node = self.gd.g_ctl, 
                      attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __hip_setup()

    def __main_setup(self):
        #--- this method makes use of the MasterMod inheritance
        if self.mirrorGuideObj:
            self.upVectorOffset = [-6,-0.1,0]
            self.aimVector = [0,0,-1]
            self.upVector = [0,1,0]
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
        if not self.mirrorGuideObj:
            #--- cleanup
            self.__hip_cleanup()
    #end def __main_setup
#end class BipedHipGuide()


class BipedHipPuppet(puppet.Puppet):
    """
    This class prepares a biped hip rig system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).       
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  autoHip = False,
                  softHip = False):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedHipPuppet, self).__init__(character = character,
                                             guideObj = guideObj)

        #args
        self.character = character
        self.guideObj = guideObj
        self.autoHip = autoHip
        self.softHip = softHip

        #vars
        self.control = None
        self.ocn = None

        #methods
        self.__create_puppet()
    #end def __init__()

    def __create_controls(self):
        #--- this method creates the controls
        if self.guideObj.gd.flip:
            ctl = control.Control(side = self.side, 
                                  name = self.mod, 
                                  suffix = 'CTL', 
                                  size = self.size * 0.75, 
                                  shape = 4, 
                                  color = self.color, 
                                  position = [0,0,0], 
                                  rotation = [0,0,0],
                                  orientation = [90,0,180],
                                  offset = [-0.5,0,-1], 
                                  parent = self.joints[0])
        else:
            ctl = control.Control(side = self.side, 
                                  name = self.mod, 
                                  suffix = 'CTL', 
                                  size = self.size * 0.75, 
                                  shape = 4, 
                                  color = self.color, 
                                  position = [0,0,0], 
                                  rotation = [0,0,0],
                                  orientation = [90,0,0],
                                  offset = [0.5,0,1], 
                                  parent = self.joints[0])
        cmds.parent(ctl.group, self.side_ctl_grp) 
        self.control = ctl
    #end def __create_controls()

    def __setup_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- orientConstraint the joint to the control
        ctl = self.control
        ocn = nd.parentConstraint(objA = ctl.transform,
                                  objB = self.joints[0], 
                                  name = self.side + '_' + self.mod + self.name,
                                  maintainOffset = False)[0]
        self.ocn = ocn
    #end def __setup_controls()

    def __prepare_auto_hip(self):
        #--- this method prepares attributes for the autoHip
        attr = attribute.Attribute()
        #--- add autoHip attributes
        attr.addAttr(node = self.control.transform, 
                     attrName = 'autoHip', 
                     attrType = 'float', 
                     min = 0, 
                     max = 1, 
                     default = 1)
        if self.softHip:
            attr.addAttr(node = self.control.transform, 
                         attrName = 'softness', 
                         attrType = 'float', 
                         min = 1, 
                         default = 10)
            attr.addAttr(node = self.control.transform, 
                         attrName = 'smoothRotateY', 
                         attrType = 'float', 
                         min = 0, 
                         max = 1,
                         default = 0.5)
            attr.addAttr(node = self.control.transform, 
                         attrName = 'smoothRotateZ', 
                         attrType = 'float', 
                         min = 0, 
                         max = 1,
                         default = 0.5)
        #--- lock unnecessary attributes on the hip control
        attr.lockAttr(node = self.control.transform, 
                      attribute = ['t','s', 'v'])
    #end def __prepare_auto_hip()

    def __prepare_soft_hip(self):
        #--- this method prepares the soft hip system
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create softHip groups
        self.soft_grp = nd.transform(name = self.side + '_' + self.mod + 'SoftSetup', 
                                     suffix = 'GRP', 
                                     parent = self.side_extra_grp)      

        #--- LOCATORS
        #--- translate Y
        self.ty_loc = nd.locator(name = self.side + '_' + self.mod + 'SoftTY', 
                                 suffix = 'LOC', 
                                 position = [1,0,0], 
                                 worldSpace = True, 
                                 parent = self.soft_grp)         
        #--- translate Y Target        
        self.tyIk_loc = nd.locator(name = self.side + '_' + self.mod + 'SoftIkTY', 
                                   suffix = 'LOC', 
                                   position = [1,0,0], 
                                   worldSpace = True, 
                                   parent = self.soft_grp)
        #--- translate Z
        self.tz_loc = nd.locator(name = self.side + '_' + self.mod + 'SoftTZ', 
                                 suffix = 'LOC', 
                                 position = [1,0,0], 
                                 worldSpace = True, 
                                 parent = self.soft_grp)           
        #--- translate Z Target
        self.tzIk_loc = nd.locator(name = self.side + '_' + self.mod + 'SoftIkTZ', 
                                   suffix = 'LOC', 
                                   position = [1,0,0], 
                                   worldSpace = True, 
                                   parent = self.soft_grp)

        #--- UTILITY NODES
        #--- multiplyDivide translation
        self.translate_mlt = nd.multiplyDivide(name = (self.side + '_' + self.mod 
                                                       + 'SoftTranslate'),
                                               input2Y = 0.005, 
                                               input2Z = 0.005, 
                                               lockAttr = ['input2Y', 
                                                           'input2Z'])
        #--- condition ty and tz
        self.ty_cnd = nd.condition(name = self.side + '_' + self.mod + 'SoftTY', 
                                   secondTerm = 0, 
                                   operation = 2,
                                   lockAttr = 'secondTerm')
        self.tz_cnd = nd.condition(name = self.side + '_' + self.mod + 'SoftTZ', 
                                   secondTerm = 0, 
                                   operation = 4,
                                   lockAttr = 'secondTerm')
        #--- remapValue ty and tz
        self.ty_rmv = nd.remapValue(name = self.side + '_' + self.mod + 'SoftTY', 
                                    inputMin = -1, 
                                    inputMax = 2, 
                                    outputMin = 0,
                                    lockAttr = ['inputMin',
                                                'inputMax',
                                                'outputMin'])
        self.tz_rmv = nd.remapValue(name = self.side + '_' + self.mod + 'SoftTZ', 
                                    inputMin = -2, 
                                    inputMax = 1, 
                                    outputMin = 0,
                                    lockAttr = ['inputMin',
                                                'inputMax',
                                                'outputMin'])
        #--- connect the utility nodes
        #--- translateY
        attr.connectAttr(node = [self.ty_loc, self.translate_mlt], 
                         attribute = ['translateY', 'input1Y'])
        attr.connectAttr(node = [self.translate_mlt, self.ty_cnd], 
                         attribute = ['outputY', 'colorIfFalseG'])
        attr.connectAttr(node = [self.ty_loc, self.ty_cnd], 
                         attribute = ['translateY', 'firstTerm'])
        attr.connectAttr(node = [self.ty_loc, self.ty_cnd], 
                         attribute = ['translateY', 'colorIfTrueG'])
        attr.connectAttr(node = [self.ty_cnd, self.ty_rmv], 
                         attribute = ['outColorG', 'inputValue'])
        attr.connectAttr(node = [self.ty_loc, self.ty_rmv], 
                         attribute = ['translateY', 'outputMax'])
        attr.connectAttr(node = [self.ty_rmv, self.tyIk_loc], 
                         attribute = ['outValue', 'translateY'])
        #--- translateZ
        attr.connectAttr(node = [self.tz_loc, self.translate_mlt], 
                         attribute = ['translateZ', 'input1Z'])
        attr.connectAttr(node = [self.translate_mlt, self.tz_cnd], 
                         attribute = ['outputZ', 'colorIfFalseB'])
        attr.connectAttr(node = [self.tz_loc, self.tz_cnd], 
                         attribute = ['translateZ', 'firstTerm'])
        attr.connectAttr(node = [self.tz_loc, self.tz_cnd], 
                         attribute = ['translateZ', 'colorIfTrueB'])
        attr.connectAttr(node = [self.tz_cnd, self.tz_rmv], 
                         attribute = ['outColorG', 'inputValue'])
        attr.connectAttr(node = [self.tz_loc, self.tz_rmv], 
                         attribute = ['translateZ', 'outputMax'])
        attr.connectAttr(node = [self.tz_rmv, self.tzIk_loc], 
                         attribute = ['outValue', 'translateZ'])
        #--- smoothRotate to value[1].float_Value
        attr.connectAttr(node = [self.control.transform, self.ty_rmv], 
                         attribute = ['smoothRotateZ', 
                                      'value[1].value_FloatValue'])
        attr.connectAttr(node = [self.control.transform, self.tz_rmv], 
                         attribute = ['smoothRotateY', 
                                      'value[1].value_FloatValue'])

        #--- CREATE JOINT CHAIN
        #--- create the rotationY setup
        self.soft_ry_jnt = jointchain.IkChain(side = self.side, 
                                              name = [self.mod + 'SoftRotY1', 
                                                      self.mod + 'SoftRotY2'], 
                                              suffix = 'JNT', 
                                              position = [[0,0,0], [1,0,0]], 
                                              ikSolver = 'ikSCSolver',
                                              mirror = False, 
                                              radius = 0.5, 
                                              parentJoint = self.soft_grp, 
                                              parentIk = self.tzIk_loc)
        #--- create the rotationZ setup
        self.soft_rz_jnt = jointchain.IkChain(side = self.side, 
                                              name = [self.mod + 'SoftRotZ1', 
                                                      self.mod + 'SoftRotZ2'], 
                                              suffix = 'JNT', 
                                              position = [[0,0,0], [1,0,0]], 
                                              ikSolver = 'ikSCSolver',
                                              mirror = False, 
                                              radius = 0.5, 
                                              parentJoint = self.soft_grp, 
                                              parentIk = self.tyIk_loc)
    #end def __prepare_soft_hip()

    def __create_puppet(self):
        #--- this is the main create method
        #--- create the controls
        self.__create_controls()
        #--- setup the controls
        self.__setup_controls()
        if self.autoHip:
            #--- setup for autoHip
            self.__prepare_auto_hip()
        if self.softHip:
            #--- setup for softHip
            self.__prepare_soft_hip()
    #end def __create_puppet()
#end class BipedHipPuppet()


class QuadrupedHipGuide(mod.MasterMod):
    
    """
    This class creates a quadruped hip guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'hip',
                  side = 'L',
                  name = 'ilium',
                  size = 0.75,
                  shape = 2, 
                  color = 6, 
                  position = [1, 17.5, -5],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [-1,0,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedHipGuide, self).__init__()

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

    def __hip_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_ctl, 
                      attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __hip_setup()

    def __main_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
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
        self.__hip_cleanup()
    #end def __main_setup
#end class QuadrupedHipGuide()