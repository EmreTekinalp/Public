'''
Created on 19.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Mouth module with different mouth classes
'''

from maya import cmds
from fundamentals import attribute, node
from mods import mod
reload(attribute)
reload(mod)
reload(node)


class BipedMouthGuide(mod.MasterMod):
    """
    This class creates a biped mouth guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'mouth',
                  side = 'C',
                  name = ['pivotA', 'pivotB'],
                  suffix = 'GCTL',
                  size = 0.25,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 17, 
                  position = [[0,24,-1],[0,24,3]],
                  rotation = [0,0,0],
                  upVectorOffset = [-6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedMouthGuide, self).__init__()

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

    def __mouth_setup(self):
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
        #--- create the message connection setup
        self.__connect_message()                
    #end def __mouth_setup()

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

    def __mouth_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)        
        attr.lockAttr(node = self.gd.g_ctl[1:], attribute = ['tx'])
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
    #end def __mouth_cleanup()

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
        self.__mouth_setup()
        self.__mouth_cleanup()
    #end def __main_setup
#end class BipedMouthGuide()


class QuadrupedMouthGuide(mod.MasterMod):
    """
    This class creates a quadruped mouth guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'mouth',
                  side = 'C',
                  name = ['pivotA', 'pivotB'],
                  size = 0.25,
                  shape = 2, 
                  color = 17, 
                  position = [[0.0, 24, 14.5],
                              [0.0, 18.5, 18]],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedMouthGuide, self).__init__()

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

    def __mouth_setup(self,
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
        #--- create the message connection setup
        self.__connect_message()                
    #end def __mouth_setup()

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

    def __mouth_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls        
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)        
        attr.lockAttr(node = self.gd.g_ctl[1:], attribute = ['tx'])
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
    #end def __mouth_cleanup()

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
        self.__mouth_setup(mod = mod, 
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
        self.__mouth_cleanup()
    #end def __main_setup
#end class QuadrupedMouthGuide()