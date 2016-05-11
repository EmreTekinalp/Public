'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Neck module with different neck classes
'''

import string
from maya import cmds
from fundamentals import attribute, node
from functions import control, hook
from mods import hand, mod
reload(attribute)
reload(control)
reload(hand)
reload(hook)
reload(mod)
reload(node)


class BipedNeckGuide(mod.MasterMod):
    """
    This class creates a biped neck guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  mod = 'neck',
                  side = 'C',
                  name = ['cervicalVertebraeA', 
                          'cervicalVertebraeB', 
                          'cervicalVertebraeC'],
                  size = 0.25,
                  shape = 2, 
                  color = 17, 
                  position = [[0,21,0],[0,22,0],[0,23,0]],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedNeckGuide, self).__init__()
        
        #vars

        #methods
        self.__main_setup(mod = mod, 
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
    #end def __neck_setup()

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
        self.create(mod = mod, 
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
#end class BipedNeckGuide()


BipedNeckGuide()