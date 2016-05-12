'''
Created on 17.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Hand module with different hand classes
'''

from maya import cmds
from fundamentals import attribute, node
from mods import mod
reload(attribute)
reload(mod)
reload(node)


class BipedHandGuide(mod.MasterMod):
    
    """
    This class creates a biped hand guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'hand',
                  side = 'L',
                  name = 'palm',
                  suffix = 'GCTL',
                  size = 0.5,
                  shape = 2,
                  orientation = [0,0,0],
                  color = 6,
                  position = [11,20,0],
                  rotation = [0,0,0],
                  upVectorOffset = [0,0,6],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedHandGuide, self).__init__()

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

        #methods
        self.__main_setup()
    #end def __init__()

    def __hand_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes
        attr.lockAttr(node = self.gd.g_ctl[0], attribute = ['s', 'v'])  
    #end def __hand_cleanup()

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
        #--- mod specific cleanup
        self.__hand_cleanup()
    #end def __main_setup
#end class BipedHandGuide()