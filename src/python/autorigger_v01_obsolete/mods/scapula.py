'''
Created on 17.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Scapula module with different scapula classes
'''

from maya import cmds
from fundamentals import attribute, node
from functions import control, puppet
from mods import mod
reload(attribute)
reload(control)
reload(mod)
reload(node)
reload(puppet)


class BipedScapulaGuide(mod.MasterMod):
    
    """
    This class creates a biped scapula guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'scapula',
                  side = 'L',
                  name = ['acromion', 'inferiorAngle'],
                  suffix = 'GCTL',                  
                  size = 0.75,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 6, 
                  position = [[4,20,-1],[1,16,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [0,6,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedScapulaGuide, self).__init__()

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

    def __scapula_setup(self):
        #--- this method setups the scapula
        #--- unlock all necessary attributes from specified nodes
        attr = attribute.Attribute()
        if not self.mirrorGuideObj:
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
    #end def __scapula_setup()

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
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', 
                                     lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #end def __connect_message()

    def __scapula_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)
    #end def __scapula_cleanup()        

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
        #--- this method is a mod specific setup
        self.__scapula_setup()
        #--- this method is a mod specific cleanup
        self.__scapula_cleanup()
    #end def __main_setup
#end class BipedScapulaGuide()


class BipedScapulaPuppet(puppet.Puppet):
    """
    This class prepares a biped scapula rig system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).       
    """

    def __init__(self, 
                  character = None,
                  guideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedScapulaPuppet, self).__init__(character = character,
                                                 guideObj = guideObj)

        self.character = character
        self.guideObj  = guideObj

        #methods
        self.__create_puppet(character = character,
                             guideObj = guideObj)
    #end def __init__()

    def __create_puppet(self,
                          character = None,
                          guideObj = None):
        #--- this is the main create method
        pass
    #end def __create_puppet()
#end class BipedScapulaPuppet()


class QuadrupedScapulaGuide(mod.MasterMod):
    
    """
    This class creates a quadruped scapula guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'scapula',
                  side = 'L',
                  name = 'acromion',
                  size = 0.75,
                  shape = 2, 
                  color = 6, 
                  position = [1.5, 16, 6],
                  upVectorOffset = [0,6,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedScapulaGuide, self).__init__()

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

    def __scapula_setup(self):
        #--- this method setups the scapula
        #--- create the message connection setup
        self.__connect_message()  
    #end def __scapula_setup()

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

    def __scapula_cleanup(self):
        #--- this method is a mod specific cleanup
        pass
    #end def __scapula_cleanup()        

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
        #--- this method is a mod specific setup
        self.__scapula_setup()
        #--- this method is a mod specific cleanup
        self.__scapula_cleanup()
    #end def __main_setup
#end class QuadrupedScapulaGuide()