'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Masterclass of the mods
'''

from maya import cmds
from functions import guide
from fundamentals import attribute, node
reload(attribute)
reload(guide)
reload(node)


class MasterMod(object):
    """
    This class is the master class for all modules, which shall be inherited.
    """

    def __init__(self):
        pass
    #END def __init__()

    def __guide_setup(self,
                       character = None,
                       mod = None, 
                       side = None, 
                       name = None, 
                       suffix = 'GCTL',
                       size = 1, 
                       shape = 0,
                       orientation = [0,0,0],
                       color = 0, 
                       position = [0,0,0],
                       rotation = [0,0,0], 
                       upVectorOffset = [0,6,0], 
                       aimVector = [1,0,0], 
                       upVector = [0,1,0],
                       rotateOrder = 3,
                       flip = False,
                       mirrorGuideObj = None):
        #--- this method creates the guide controls
        #--- take care of the whiteSpaces in the character name
        if ' ' in character:
            character = character.replace(' ','_')
        #--- create guides
        if mirrorGuideObj:
            flip = True
        self.gd = guide.Guide(character = character,
                              mod = mod, 
                              side = side, 
                              name = name, 
                              size = size, 
                              shape = shape, 
                              orientation = orientation,                              
                              color = color, 
                              position = position,
                              rotation = rotation,
                              upVectorOffset = upVectorOffset, 
                              aimVector = aimVector,
                              upVector = upVector,
                              rotateOrder = rotateOrder,
                              flip = flip,
                              mirrorGuideObj = mirrorGuideObj)            
        self.__connect_message()
    #END def guide_setup()

    def __connect_message(self):
        #--- connect the message attribute between the first joint and main mod
        if cmds.objExists(self.gd.main_mod + '.' + self.gd.side + '_connection'):
            cmds.setAttr(self.gd.main_mod + '.' + self.gd.side + '_connection', 
                         lock = False)
            cmds.connectAttr(self.gd.g_jnt[0] + '.message', 
                             self.gd.main_mod + '.' + self.gd.side + '_connection')
    #END def __connect_message()

    def __guide_cleanup(self, 
                          mod = None):
        #--- this method cleans up the guides appropriately
        attr = attribute.Attribute()
        #--- list all objects which shall be locked completely
        obj = cmds.ls('*' + mod + '*_PCN', 
                      '*' + mod + '*_PAC', 
                      '*' + mod + '*_OCN')
        attr.lockAll(node = obj, lock = True)
        #--- lock all transforms of the guide group nodes
        attr.lockAll(node = self.gd.g_grp, lock = True)
        #--- hide isHistoricalInteresting nodes
        for i in cmds.ls('*' + mod + '*Shape*', 
                         '*' + mod + '*_AIM*', 
                         '*' + mod + '*_GRP*', 
                         '*' + mod + '*_CTL*', 
                         '*' + mod + '*_DCM*'):
            cmds.setAttr(i + '.ihi', 0)
        cmds.select(clear = True)
    #END def guide_cleanup()

    def create(self,
                character = None,
                mod  = None,
                side = None,
                name = None,
                suffix = None,
                size = 1,
                shape = 0, 
                orientation = [0,0,0],
                color = 0, 
                position = [0,0,0],
                rotation = [0,0,0],
                upVectorOffset = [0,6,0],
                aimVector = [1,0,0],
                upVector = [0,1,0],
                rotateOrder = 3,
                flip = False,
                mirrorGuideObj = None):
        #--- this method calls all the necessary methods in right order
        self.__guide_setup(character = character,
                           mod = mod, 
                           side = side, 
                           name = name, 
                           size = size,
                           shape = shape, 
                           orientation = orientation,
                           color = color, 
                           position = position,
                           rotation = rotation,
                           upVectorOffset = upVectorOffset, 
                           aimVector = aimVector,
                           upVector = upVector,
                           rotateOrder = rotateOrder,
                           flip = flip,
                           mirrorGuideObj = mirrorGuideObj)
        self.__guide_cleanup(mod = mod)

        print self.gd.side + '_' + self.gd.mod.upper() + ' guide module successfully created!'
    #END def create()
#END class MasterMod()
