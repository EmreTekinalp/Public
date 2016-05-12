'''
Created on 01.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Spine module with different spine classes
'''

from maya import cmds
from fundamentals import attribute, node
from functions import control, flexiplane, puppet
from mods import mod
reload(attribute)
reload(control)
reload(flexiplane)
reload(mod)
reload(node)
reload(puppet)


class BipedSpineGuide(mod.MasterMod):
    """
    This class creates a biped spine guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'spine',
                  side = 'C',
                  name = ['pelvis','sternum'],
                  suffix = 'GCTL',
                  size = 0.4,
                  shape = 2,
                  orientation = [0,0,0], 
                  color = 22, 
                  position = [[0,12,0],[0,18,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [-6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedSpineGuide, self).__init__()

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

        #methods
        self.__main_setup()
    #END def __init__()

    def __spine_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()        
        #--- unlock all necessary attributes from specified nodes
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
    #END def __spine_setup()

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
    #END def __connect_message()

    def __spine_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()        
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)              
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['tx','ry','rz'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #END def __spine_cleanup()

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
                    flip = self.flip)
        #--- mod specific setup        
        self.__spine_setup()
        #--- mod specific cleanup
        self.__spine_cleanup()
    #END def __main_setup()
#END class BipedSpineGuide()


class BipedSpinePuppet(puppet.Puppet):
    """
    This class creates a biped spine rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedSpinePuppet, self).__init__(character = character,
                                               guideObj = guideObj)

        #args
        self.character = character
        self.guideObj = guideObj

        #vars
        self.cog_control     = None
        self.pelvis_control  = None
        self.hip_control     = None
        self.ribcage_control = None
        self.sternum_control = None

        self.spine_flexiplane = None
        self.mid_control      = None
        self.vert_up_grp      = None 

        #methods
        self.__create_puppet()
    #END def __init__()

    def __setup_joints(self):
        #--- this method setups the joints
        cmds.parent(self.joints[-1], self.side_jnt_grp)
    #END def __joint_setup()

    def __create_controls(self):
        #--- this method creates the spine controls
        #--- centre of gravity control
        self.cog_control = control.Control(side = self.side, 
                                           name = self.mod + 'CentreOfGravity',
                                           suffix = 'CTL', 
                                           size = self.size + 3, 
                                           shape = 11, 
                                           color = self.color, 
                                           position = self.joint_position[0], 
                                           rotation = [0,0,0],
                                           orientation = [0,0,0],
                                           lockAttrs=['s'])
        cmds.parent(self.cog_control.group, self.side_ctl_grp)

        #--- pelvis control
        self.pelvis_control = control.Control(side = self.side, 
                                              name = self.mod + 'Pelvis',
                                              suffix = 'CTL', 
                                              size = self.size + 2, 
                                              shape = 10, 
                                              color = self.color, 
                                              position = self.joint_position[0], 
                                              rotation = [0,0,0],
                                              orientation = [0,90,0],
                                              lockAttrs=['s'])
        cmds.parent(self.pelvis_control.group, self.cog_control.transform)

        #--- hip control
        self.hip_control = control.Control(side = self.side, 
                                           name = self.mod + 'Hip',
                                           suffix = 'CTL', 
                                           size = self.size + 1, 
                                           shape = 10, 
                                           color = self.color, 
                                           position = self.joint_position[0], 
                                           rotation = [0,0,0],
                                           orientation = [0,0,0],
                                           lockAttrs=['s'])
        cmds.parent(self.hip_control.group, self.cog_control.transform)

        #--- ribcage control
        self.ribcage_control = control.Control(side = self.side, 
                                               name = self.mod + 'Ribcage',
                                               suffix = 'CTL', 
                                               size = self.size + 2, 
                                               shape = 11, 
                                               color = self.color, 
                                               position = self.joint_position[-1], 
                                               rotation = [0,0,0],
                                               orientation = [0,0,0],
                                               lockAttrs=['s'])
        cmds.parent(self.ribcage_control.group, self.pelvis_control.transform)

        #--- sternum control
        self.sternum_control = control.Control(side = self.side, 
                                               name = self.mod + 'Sternum',
                                               suffix = 'CTL', 
                                               size = self.size + 1, 
                                               shape = 10, 
                                               color = self.color, 
                                               position = self.joint_position[-1], 
                                               rotation = [0,0,0],
                                               orientation = [0,0,0],
                                               lockAttrs=['s'])
        cmds.parent(self.sternum_control.group, self.ribcage_control.transform)
    #END def __create_controls()

    def __create_flexiplane(self):
        #--- this method creates the spine flexiplane
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the first flexiplane for the humerus bone
        self.spine_flexiplane = flexiplane.FlexiPlane(character = self.character, 
                                                      mod = self.mod, 
                                                      side = self.side, 
                                                      name = 'vertebrae', 
                                                      color = self.color, 
                                                      size = self.size,
                                                      length = 5,
                                                      rotation = [0,0,90],
                                                      constraintTo = [self.hip_control.transform,
                                                                      self.ribcage_control.transform],
                                                      constraintType = 'point', 
                                                      follow = False,
                                                      parent = self.side_extra_grp,
                                                      inheritsTransform = False)
    #END def __create_flexiplane()

    def __setup_flexiplane(self):
        #--- this method setups the flexiplane properly
        attr = attribute.Attribute()
        nd = node.Node()
        #--- reorient the flexiplane
        attr.setAttr(node = self.spine_flexiplane.control_main.transform, 
                     attribute = 'rz', 
                     value = 90)
        attr.lockAttr(node = self.spine_flexiplane.control_main.group, 
                      attribute = ['t', 'r', 's'], 
                      lock = False, 
                      show = True)
        #--- parent the main control of the flexiplane to the cog control
        cmds.parent(self.spine_flexiplane.control_main.group, 
                    self.pelvis_control.transform)
        #--- get the position of the mid control
        mid_pos = cmds.xform(self.spine_flexiplane.control_mid.transform, 
                             query = True, 
                             rotatePivot = True,
                             worldSpace = True)
        #--- create mid control
        self.mid_control = control.Control(side = self.side, 
                                           name = self.mod + 'MidFK',
                                           suffix = 'CTL', 
                                           size = self.size + 1, 
                                           shape = 0, 
                                           color = self.color, 
                                           position = mid_pos, 
                                           rotation = [0,0,0],
                                           orientation = [0,0,0],
                                           lockAttrs = ['t', 's', 'v'])
        cmds.parent(self.mid_control.group, self.pelvis_control.transform)
        #--- create another group above the mid_control
        self.vert_up_grp = cmds.group(self.mid_control.transform, 
                                      name = self.side + '_' + self.mod + 'MidUpFK_GRP')

        #--- pointConstraint the flexiPlane mid control to the mid control
        nd.pointConstraint(objA = self.mid_control.transform, 
                           objB = self.spine_flexiplane.control_mid.group, 
                           suffix = 'PCN', 
                           maintainOffset = True)

        #--- reposition the pivot of the ribcage group
        cmds.xform(self.ribcage_control.group, 
                   pivots = mid_pos, 
                   worldSpace = True)

        #--- orientConstraint the ribcage control to vert control 
        nd.orientConstraint(objA = self.mid_control.transform, 
                            objB = self.ribcage_control.group, 
                            suffix = 'OCN', 
                            maintainOffset = True)

        #--- create utility nodes
        mid_ctl_pma = nd.plusMinusAverage(name = self.side + '_' + self.mod + 'MidCtl', 
                                          operation = 3)
        mid_cls_pma = nd.plusMinusAverage(name = self.side + '_' + self.mod + 'MidCls', 
                                          operation = 3)
        multi_pma = nd.plusMinusAverage(name = self.side + '_' + self.mod + 'Multi', 
                                        operation = 3)

        mid_cls_mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'MidCls', 
                                        input2X = 2,
                                        input2Y = 2,
                                        lockAttr = ['input2X','input2Y'])

        rot_up_pma = nd.plusMinusAverage(name = self.side + '_' + self.mod + 'RotUpFlp', 
                                         operation = 1)

        #--- connect nodes
        attr.connectAttr(node = [self.ribcage_control.transform, mid_ctl_pma], 
                         attribute = ['ty', 'input1D[0]'])
        attr.connectAttr(node = [self.hip_control.transform, mid_ctl_pma], 
                         attribute = ['ty', 'input1D[1]'])
        attr.connectAttr(node = [mid_ctl_pma, self.vert_up_grp], 
                         attribute = ['output1D', 'ty'])

        attr.connectAttr(node = [self.vert_up_grp, mid_cls_mlt], 
                         attribute = ['ty', 'input1X'])    
        attr.connectAttr(node = [self.mid_control.transform, mid_cls_mlt], 
                         attribute = ['ty', 'input1Y'])

        attr.connectAttr(node = [self.ribcage_control.transform, multi_pma], 
                         attribute = ['ty', 'input1D[0]'])
        attr.connectAttr(node = [self.hip_control.transform, multi_pma], 
                         attribute = ['ty', 'input1D[1]'])
        attr.connectAttr(node = [mid_cls_mlt, multi_pma], 
                         attribute = ['outputX', 'input1D[2]'])
        attr.connectAttr(node = [mid_cls_mlt, multi_pma], 
                         attribute = ['outputY', 'input1D[3]'])

        #--- unlock ty attribute of the mid cluster group
        attr.lockAttr(node = self.spine_flexiplane.clstr_mid_grp, 
                      attribute = ['t'], 
                      lock = False)
        attr.connectAttr(node = [multi_pma, 
                                 self.spine_flexiplane.clstr_mid_grp],
                         attribute = ['output1D', 'tx'])
        attr.connectAttr(node = [self.spine_flexiplane.control_mid.group,
                                 self.spine_flexiplane.clstr_mid_grp],
                         attribute = ['ty', 'ty'])
        attr.connectAttr(node = [self.spine_flexiplane.control_mid.group,
                                 self.spine_flexiplane.clstr_mid_grp],
                         attribute = ['tz', 'tz'])

        attr.connectAttr(node = [self.ribcage_control.transform,
                                 rot_up_pma], 
                         attribute = ['ry', 'input1D[0]'])
        attr.connectAttr(node = [self.mid_control.transform,
                                 rot_up_pma], 
                         attribute = ['ry', 'input1D[1]'])
        attr.connectAttr(node = [rot_up_pma, 
                                 self.spine_flexiplane.control_up.transform], 
                         attribute = ['output1D', 'rx'])
        attr.connectAttr(node = [self.hip_control.transform,
                                 self.spine_flexiplane.control_down.transform], 
                         attribute = ['ry', 'rx'])
    #END def __setup_flexiplane()

    def __setup_controls(self):
        #--- this method setups the centre of gravity control
        nd = node.Node()
        #--- parentConstraint the joints to the controls
        nd.parentConstraint(objA = self.hip_control.transform, 
                            objB = self.joints[0], 
                            suffix = 'PAC', 
                            lock = True)
        nd.parentConstraint(objA = self.sternum_control.transform, 
                            objB = self.joints[-1], 
                            suffix = 'PAC',
                            lock = True)
    #END def __cog_setup()

    def __create_puppet(self):
        #--- this is the main create method
        #--- setup the joints
        self.__setup_joints()
        #--- create the controls
        self.__create_controls()
        #--- create the flexiplanes
        self.__create_flexiplane()
        #--- setup the flexiplanes
        self.__setup_flexiplane()
        #--- setupt the controls
        self.__setup_controls()
    #END def __create_puppet()
#END class BipedSpinePuppet()


class QuadrupedSpineGuide(mod.MasterMod):
    """
    This class creates a quadruped spine guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'spine',
                  side = 'C',
                  name = ['pelvis', 'vertebraeA', 'vertebraeB', 
                          'vertebraeC', 'vertebraeD'],
                  size = 0.4,
                  shape = 2, 
                  color = 17, 
                  position = [[0.0, 18, -3],
                              [0.0, 17.5, -1],
                              [0.0, 17.25, 1],
                              [0.0, 17.5, 3],
                              [0.0, 18, 5]],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedSpineGuide, self).__init__()
        
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
    #END def __init__()

    def __spine_setup(self,
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
    #END def __spine_setup()

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
    #END def __connect_message()

    def __spine_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)              
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['tx','ry','rz'])
        attr.lockAttr(node = self.gd.g_ctl, attribute = ['s', 'v'])
        cmds.select(clear = True)
    #END def __spine_cleanup()

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
        self.__spine_setup(mod = mod, 
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
        self.__spine_cleanup()
    #END def __main_setup()
#END class QuadrupedSpineGuide()

