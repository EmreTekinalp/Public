'''
Created on 26.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Ear module with different ear classes
'''

from maya import cmds
from fundamentals import attribute, node
from mods import mod
reload(attribute)
reload(mod)
reload(node)


class BipedEarGuide(mod.MasterMod):
    """
    This class creates a biped ear guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'ear',
                  side = 'L',
                  name = ['pinnaRoot', 'pinnaEnd'],
                  suffix = 'GCTL',
                  size = 0.20,
                  shape = 2,
                  orientation = [0,0,0],
                  color = 6, 
                  position = [[1,25,0],[1.5,25,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedEarGuide, self).__init__()

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

        #vars

        #methods
        self.__main_setup()
    #end def __init__()

    def __ear_offset(self):
        #--- this method creates an earsAmount offset
        self.pos = []
        for e in range(self.earsAmount):
            tmp = []
            for p in range(len(self.position)):
                pos = [self.position[p][0], self.position[p][1] + e, self.position[p][2]]
                tmp.append(pos)
            self.pos.append(tmp)
    #end def ___ear_offset()

    def __ear_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()
        #--- unlock all necessary attributes from specified nodes              
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
    #end def __ear_setup()

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

    def __ear_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)
        attr.lockAttr(node = self.gd.g_ctl[-1], attribute = ['r'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __ear_cleanup()

    def __main_setup(self):
        #--- this method makes use of the MasterMod inheritance
        self.__ear_offset()
        if self.earsAmount:
            for iter in range(self.earsAmount):
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
                            rotateOrder = self.rotateOrder)
                self.jnt.append(self.gd.g_jnt)
                self.ctl.append(self.gd.g_ctl)
                self.grp.append(self.gd.g_grp)
                #--- mod specific setup         
                self.__ear_setup()
                self.__ear_cleanup()
        else:
            print 'EarsAmount is 0. You have to specify at least an amount of 1!'
    #end def __main_setup
#end class BipedEarGuide()


class QuadrupedEarGuide(mod.MasterMod):
    """
    This class creates a quadruped ear guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'ear',
                  side = 'L',
                  name = ['pinnaRoot', 'pinnaMid', 'pinnaEnd'],
                  size = 0.20,
                  shape = 2, 
                  color = 6, 
                  position = [[1,24.5,14.5],
                              [1.25,25,15],
                              [1.5,25.5,15.5]],
                  earsAmount = 1,
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedEarGuide, self).__init__()

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
                          earsAmount = earsAmount,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #end def __init__()

    def __ear_offset(self,
                      position = [0,0,0],
                      earsAmount = 1):
        #--- this method creates an earsAmount offset
        self.position = []
        for e in range(earsAmount):
            tmp = []
            for p in range(len(position)):
                pos = [position[p][0], position[p][1] + e, position[p][2]]
                tmp.append(pos)
            self.position.append(tmp)
    #end def ___ear_offset()

    def __ear_setup(self,
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
    #end def __ear_setup()

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

    def __ear_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls        
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #end def __ear_cleanup()

    def __main_setup(self,
                       character = None,
                       mod = None,
                       side = None,
                       name = None,
                       size = 1,
                       shape = 0, 
                       color = 0, 
                       position = [0,0,0],
                       earsAmount = 1,
                       upVectorOffset = [6,0,0],
                       aimVector = [0,1,0],
                       upVector = [1,0,0],
                       mirror = True):
        #--- this method makes use of the MasterMod inheritance
        self.__ear_offset(earsAmount = earsAmount, 
                          position = position)
        if earsAmount:
            for iter in range(earsAmount):
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
                #--- mod specific setup         
                self.__ear_setup(mod = mod, 
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
                self.__ear_cleanup()
        else:
            print 'EarsAmount is 0. You have to specify at least an amount of 1!'
    #end def __main_setup
#end class QuadrupedEarGuide()