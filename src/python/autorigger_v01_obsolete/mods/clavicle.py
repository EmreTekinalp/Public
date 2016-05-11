'''
Created on 17.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Clavicle module with different clavicle classes
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


class BipedClavicleGuide(mod.MasterMod):
    
    """
    This class creates a biped clavicle guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'clavicle',
                  side = 'L',
                  name = ['sternal', 'acromial'],
                  suffix = 'GCTL',
                  size = 0.75,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 6, 
                  position = [[1,20,0], [4,20,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [0,6,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedClavicleGuide, self).__init__()

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

    def __clavicle_setup(self):
        #--- this method is a mod specific setup
        #--- connect messages
        self.__connect_message()      
    #end def __clavicle_setup()

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
        self.__clavicle_setup()
    #end def __main_setup
#end class BipedClavicleGuide()


class BipedClaviclePuppet(puppet.Puppet):
    """
    This class prepares a biped clavicle rig system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).       
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  autoClavicle = False,
                  softClavicle = False):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedClaviclePuppet, self).__init__(character = character,
                                                  guideObj = guideObj)

        #args
        self.character    = character
        self.guideObj     = guideObj
        self.autoClavicle = autoClavicle
        self.softClavicle = softClavicle

        #vars
        self.control      = None
        self.ocn          = None

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
        ctl_ocn = nd.orientConstraint(objA = ctl.transform,
                                      objB = self.joints[0], 
                                      name = self.side + '_' + self.mod,
                                      maintainOffset = False)[0]
        self.ocn = ctl_ocn
    #end def __setup_controls()

    def __prepare_auto_clavicle(self):
        #--- this method prepares attributes for the autoClavicle
        attr = attribute.Attribute()
        #--- add autoClavicle attributes
        attr.addAttr(node = self.control.transform, 
                     attrName = 'autoClavicle', 
                     attrType = 'float', 
                     min = 0, 
                     max = 1, 
                     default = 1)
        if self.softClavicle:
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
        #--- lock unnecessary attributes on the clavicle control
        attr.lockAttr(node = self.control.transform, 
                      attribute = ['t','s', 'v'])
    #end def __prepare_auto_clavicle()

    def __prepare_soft_clavicle(self):
        #--- this method prepares the soft clavicle system
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create softClavicle groups
        self.soft_grp = nd.transform(name = (self.side + '_' + self.mod + 
                                             'SoftSetup'), 
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
                         attribute = ['smoothRotateZ', 'value[1].value_FloatValue'])
        attr.connectAttr(node = [self.control.transform, self.tz_rmv], 
                         attribute = ['smoothRotateY', 'value[1].value_FloatValue'])

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
    #end def __prepare_soft_clavicle()

    def __create_puppet(self):
        #--- this is the main create method
        #--- create the controls
        self.__create_controls()
        #--- setup the controls
        self.__setup_controls()
        if self.autoClavicle:
            #--- setup for autoClavicle
            self.__prepare_auto_clavicle()
        if self.softClavicle:
            #--- setup for softClavicle
            self.__prepare_soft_clavicle()
    #end def __create_puppet()
#end class BipedClaviclePuppet()