'''
Created on 26.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Tail module with different tail classes
'''

from maya import cmds
from fundamentals import attribute, node
from mods import mod
reload(attribute)
reload(mod)
reload(node)


class QuadrupedTailGuide(mod.MasterMod):
    """
    This class creates a quadruped tail guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'tail',
                  side = 'C',
                  name = ['root', 'caudalA', 'caudalB', 
                          'caudalC', 'caudalD', 'caudalE',
                          'caudalF', 'caudalG', 'caudalH'],
                  size = 0.4,
                  shape = 2, 
                  color = 17, 
                  position = [[0, 19, -10],
                              [0, 18, -11],
                              [0, 17, -11.2],
                              [0, 16, -11.4],
                              [0, 15, -11.5],
                              [0, 14, -11.6],
                              [0, 13, -11.6],
                              [0, 12, -11.7],
                              [0, 11, -11.7],],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedTailGuide, self).__init__()
        
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

    def __tail_setup(self,
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
    #end def __tail_setup()

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

    def __tail_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __tail_cleanup()

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
        #--- mod specific setup        
        self.__tail_setup(mod = mod, 
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
        self.__tail_cleanup()
    #end def __main_setup()
#end class QuadrupedTailGuide()
