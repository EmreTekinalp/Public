'''
Created on 19.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Head module with different head classes
'''

from maya import cmds
from fundamentals import attribute, duplicate, ikhandle, node
from functions import control, hook, puppet
from mods import ear, eye, jaw, mod
reload(attribute)
reload(control)
reload(duplicate)
reload(ear)
reload(eye)
reload(ikhandle)
reload(jaw)
reload(hook)
reload(mod)
reload(node)
reload(puppet)


class BipedHeadGuide(mod.MasterMod):
    """
    This class creates a biped head guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'head',
                  side = 'C',
                  name = ['skull','jawBase','jawTip'],
                  suffix = 'GCTL',
                  size = 0.25,
                  shape = 2, 
                  orientation = [0,0,0],
                  color = 22, 
                  position = [[0,24,-1],[0,25,0],[0,22,2]],
                  rotation = [0,0,0],
                  upVectorOffset = [-6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  mirrorGuideObj = None):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedHeadGuide, self).__init__()

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
        self.mirrorGuideObj = mirrorGuideObj

        #vars

        #methods
        self.__main_setup()
    #END def __init__()

    def __head_setup(self):
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
        #--- create the message connection setup
        self.__connect_message()
    #END def __head_setup()

    def __connect_guides(self, 
                           mod = None, 
                           side = None,
                           obj = None, 
                           position = [0,0,0]):
        #--- this method creates the curve which connects the guide controls        
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- create curves
        crv = cmds.curve(degree = 1, point = self.position)
        cmds.parent(crv, self.gd.extras)      
        crvShp = cmds.listRelatives(crv, allDescendents = True)[0]
        crvShp = cmds.rename(crvShp, crv + 'Shape')
        rel = cmds.listRelatives(crv, allDescendents = 1)[0]

        #--- connect the cvs to the controls by matrix
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, rel], 
                             attribute = ['outputTranslate', 
                                          'controlPoints[' + `i` + ']'])
        #--- set the displayType of the curve Shape to template
        attr.setColor(node = crvShp, displayType = 1)
    #END def __connect_guides()

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

    def __head_cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAll(node = self.gd.g_grp)         
        attr.lockAttr(node = self.gd.g_ctl, 
                      attribute = ['tx', 'ry', 'rz','s', 'v'])
        for i in cmds.ls('*DCM*', '*PAC*', '*Constraint*', '*curve*'):
            cmds.setAttr(i + '.ihi', 0)
        cmds.select(clear = True)
    #END def __head_cleanup()

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
                    rotateOrder = self.rotateOrder)
        #--- mod specific setup         
        self.__head_setup()
        #--- mod specific cleanup        
        self.__head_cleanup()
    #END def __main_setup
#END class BipedHeadGuide()


class BipedHeadPuppet(puppet.Puppet):
    """
    This class creates a biped head rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedHeadPuppet, self).__init__(character = character,
                                             guideObj = guideObj)

        #args
        self.character = character
        self.guideObj  = guideObj
        self.puppetObj = puppetObj

        #vars
        self.control_head = None
        self.control_jaw  = None

        #methods
        self.__create_puppet()
    #end def __init__()

    def __create_head_controls(self):
        #--- this method creates the head controls
        attr = attribute.Attribute()
        #--- head control
        name = self.mod + self.name[0][0].upper() + self.name[0][1:]                
        ctl = control.Control(side = self.side, 
                              name = name, 
                              suffix = 'CTL', 
                              size = self.size, 
                              shape = 2, 
                              color = self.guideObj.color, 
                              position = [0,0,0], 
                              rotation = [0,0,0],
                              offset = [0,2,0],
                              orientation = [0,0,0], 
                              parent = self.joints[0],
                              lockAttrs = ['s'])
        cmds.parent(ctl.group, world = True)
        cmds.setAttr(ctl.group + '.r', 0,0,0)
        cmds.parent(ctl.group, self.puppetObj.controls_neck[-1].transform) 
        self.control_head = ctl

        #--- jaw control
        name = self.mod + self.name[1][0].upper() + self.name[1][1:]                
        ctl = control.Control(side = self.side, 
                              name = name, 
                              suffix = 'CTL', 
                              size = self.size, 
                              shape = 2, 
                              color = self.guideObj.color, 
                              position = [0,0,0], 
                              rotation = [0,0,0],
                              offset = [3,0,0],
                              orientation = [0,0,0], 
                              parent = self.joints[1],
                              lockAttrs = ['t','s'])
        cmds.parent(ctl.group, self.control_head.transform) 
        self.control_jaw = ctl
    #END def __create_head_controls()

    def __setup_head_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- parentConstraint the ctl joints to the controls
        nd.parentConstraint(objA = self.control_head.transform,
                            objB = self.joints[0], 
                            name = (self.side + '_' + self.mod + 
                                    self.name[0][0].upper() + 
                                    self.name[0][1:]), 
                            maintainOffset = True)
        nd.parentConstraint(objA = self.control_jaw.transform,
                            objB = self.joints[1], 
                            name = (self.side + '_' + self.mod + 
                                    self.name[1][0].upper() + 
                                    self.name[1][1:]), 
                            maintainOffset = True)
    #END def __setup_head_controls()

    def __add_space_switch_attribute(self):
        #--- this method adds a space switch control
        attr = attribute.Attribute()
        #--- follow
        attr.addAttr(node = self.control_head.transform,
                     attrName = 'follow',
                     attrType = 'float',
                     min = 0,
                     max = 1)
    #END def __add_space_switch_attribute()

    def __setup_space_switch(self):
        #--- this method setups a space switch
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create a world node and pointConstraint it
        world_grp = nd.transform(name = self.side + '_' + self.mod + 'WORLD', 
                                 suffix = 'OFF', 
                                 parent = self.joints[0])
        cmds.parent(world_grp, self.side_extra_grp)
        nd.pointConstraint(objA = self.joints[0], 
                           objB = world_grp, 
                           suffix = 'PCN', 
                           maintainOffset = False, 
                           lock = True)

        #--- create a local node and parentConstraint it
        local_grp = nd.transform(name = self.side + '_' + self.mod + 'LOCAL', 
                                 suffix = 'OFF', 
                                 parent = self.joints[0])
        cmds.parent(local_grp, self.side_extra_grp)
        nd.parentConstraint(objA = self.puppetObj.joints[-1], 
                            objB = local_grp,
                            suffix = 'PAC', 
                            maintainOffset = True, 
                            lock = True)

        #--- orientConstraint the control group of the head
        ocn = nd.orientConstraint(objA = [world_grp, local_grp], 
                                  objB = self.control_head.group, 
                                  suffix = 'OCN', 
                                  maintainOffset = True)
        #--- create switch ori setup
        rev = nd.reverse(name = self.side + '_' + self.mod + 'Follow')
        attr.connectAttr(node = [self.control_head.transform, rev], 
                         attribute = ['follow', 'inputX'])
        attr.connectAttr(node = [rev, ocn],
                         attribute = ['outputX', world_grp + 'W0'])
        attr.connectAttr(node = [self.control_head.transform, ocn],
                         attribute = ['follow', local_grp + 'W1'])
    #END def__setup_space_switch()

    def __create_puppet(self):
        #--- this is the main create method
        #--- create head controls
        self.__create_head_controls()
        #--- setup head controls
        self.__setup_head_controls()
        #--- add space swich attribute
        self.__add_space_switch_attribute()
        #--- setip space switch()
        self.__setup_space_switch()
    #END def __create_puppet()
#END class BipedHeadPuppet()


class QuadrupedHeadGuide(mod.MasterMod):
    """
    This class creates a quadruped head guide system based on the specifications 
    defined in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'head',
                  side = 'C',
                  name = ['backSkull', 'frontSkull'],
                  size = 0.5,
                  shape = 2, 
                  color = 22, 
                  position = [[0.0, 24, 14.5],
                              [0.0, 18.5, 18]],
                  eye = True,
                  eyesAmount = 1,
                  jaw = True,
                  mouth = False,
                  ear = True,
                  earsAmount = 1,
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = False):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedHeadGuide, self).__init__()

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
                          eye = eye,
                          eyesAmount = eyesAmount,
                          jaw = jaw,
                          mouth = mouth, 
                          ear = ear,
                          earsAmount = earsAmount,                                                   
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #END def __init__()

    def __head_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      eye = True,
                      eyesAmount = 1,
                      jaw = True,
                      mouth = True,
                      ear = True,
                      earsAmount = 1,              
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

        #--- mouth setup
        if mouth:
            self.__head_mouth_setup(character = character,
                                    mirror = mirror)
        #--- jaw setup
        if jaw:
            self.__head_jaw_setup(character = character,
                                  mirror = mirror)
        #--- eye setup
        if eye:
            self.__head_eye_setup(character = character,
                                  eyesAmount = eyesAmount, 
                                  mouth = mouth, 
                                  mirror = True)
        #--- ear setup
        if ear:
            self.__head_ear_setup(character = character,
                                  earsAmount = earsAmount, 
                                  mirror = True)            
    #END def __head_setup()

    def __head_mouth_setup(self,
                             character = None,
                             mirror = False):
        #--- this method creates the eye setup
        self.mouth = mouth.QuadrupedMouthGuide(character = character)

        #--- connect the mouth guides properly regarding the mirror boolean
        self.__connect_guides(mod = self.mouth.gd.mod, 
                              side = self.mouth.gd.side,
                              obj = [self.gd.g_jnt[0], 
                                     self.mouth.gd.g_jnt[0]], 
                              position = [self.gd.position[0],
                                          self.mouth.gd.position[0]])
        if mirror:
            self.__connect_guides(mod = self.mouth.gd.mod, 
                                  side = self.mouth.gd.mirror_side,
                                  obj = [self.mouth.gd.mirror_ctl[0], 
                                         self.gd.g_jnt[0]], 
                                  position = [self.gd.position[0],
                                              self.mouth.gd.mirror_pos[0]])          
        #--- hook the mouth guides to the midSkull
        hook.Hook(mod = self.mouth, 
                  hookParent = self.gd.g_ctl[0], 
                  hookChild = self.mouth.gd.g_grp[0], 
                  hookType = 'parentConstraint')
        #--- lock unnecessary attributes on guide controls
        attr = attribute.Attribute()
        attr.lockAttr(node = self.mouth.gd.g_ctl, attribute = ['tx', 'r'])        
    #END def __head_mouth_setup()

    def __head_jaw_setup(self,
                           character = None,
                           mirror = True):
        #--- this method creates the eye setup
        self.jaw = jaw.QuadrupedJawGuide(character = character)

        #--- connect the mouth guides properly regarding the mirror boolean
        self.__connect_guides(mod = self.jaw.gd.mod, 
                              side = self.jaw.gd.side,
                              obj = [self.gd.g_jnt[0],
                                     self.jaw.gd.g_jnt[0]], 
                              position = [self.gd.position[0],
                                          self.jaw.gd.position[0]])
        if mirror:
            self.__connect_guides(mod = self.jaw.gd.mod, 
                                  side = self.jaw.gd.mirror_side,
                                  obj = [self.gd.g_jnt[0],
                                         self.jaw.gd.mirror_ctl[0]], 
                                  position = [self.gd.position[0],
                                              self.jaw.gd.mirror_pos[0]])
        #--- hook the jaw guides to the midSkull
        hook.Hook(mod = self.jaw, 
                  hookParent = self.gd.g_ctl[0], 
                  hookChild = self.jaw.gd.g_grp[0], 
                  hookType = 'parentConstraint')     
    #END def __head_jaw_setup()

    def __head_eye_setup(self,
                           character = None,
                           eyesAmount = 1,
                           mouth = True,
                           mirror = True):
        #--- this method creates the eye setup
        self.eye = eye.QuadrupedEyeGuide(character = character,
                                     eyesAmount = eyesAmount, 
                                     mirror = mirror)

        #--- get the attr and nd tools
        nd = node.Node()
        attr = attribute.Attribute()
        #--- setup the connection lines of the guides
        if eyesAmount:
            for iter in range(eyesAmount):
                #--- connect the eye guides properly
                if mouth:
                    self.__connect_guides(mod = self.eye.gd.mod, 
                                          side = self.eye.gd.side,
                                          obj = [self.mouth.gd.g_jnt[0],
                                                 self.eye.jnt[iter][0]], 
                                          position = [self.mouth.gd.position[0],
                                                      self.eye.position[iter][0]])
                    if mirror:
                        self.__connect_guides(mod = self.eye.gd.mod, 
                                              side = self.eye.gd.mirror_side,
                                              obj = [self.mouth.gd.g_jnt[0], 
                                                     self.eye.mirror_ctl[iter][0]], 
                                              position = [self.mouth.gd.position[0],
                                                          self.eye.mirror_pos[iter][0]])
                    #--- hook the eye guides to the mouth
                    hook.Hook(mod = self.eye, 
                              hookParent = self.mouth.gd.g_ctl[0], 
                              hookChild = self.eye.grp[iter][0], 
                              hookType = 'parentConstraint')
                else:
                    self.__connect_guides(mod = self.eye.gd.mod, 
                                          side = self.eye.gd.side,
                                          obj = [self.gd.g_jnt[0],
                                                 self.eye.jnt[iter][0]], 
                                          position = [self.gd.position[0],
                                                      self.eye.position[iter][0]])
                    if mirror:
                        self.__connect_guides(mod = self.eye.gd.mod, 
                                              side = self.eye.gd.mirror_side,
                                              obj = [self.gd.g_jnt[0], 
                                                     self.eye.mirror_ctl[iter][0]], 
                                              position = [self.gd.position[0],
                                                          self.eye.mirror_pos[iter][0]])
                    #--- hook the eye guides to the midSkull
                    hook.Hook(mod = self.eye, 
                              hookParent = self.gd.g_ctl[0], 
                              hookChild = self.eye.grp[iter][0], 
                              hookType = 'parentConstraint')
    #END def __head_eye_setup()

    def __head_ear_setup(self,
                           character = None,
                           earsAmount = 1,
                           mirror = True):
        #--- this method creates the ear setup
        self.ear = ear.QuadrupedEarGuide(character = character,
                                         earsAmount = earsAmount, 
                                         mirror = mirror)

        #--- setup the connection lines of the guides
        if earsAmount:
            for iter in range(earsAmount):
                #--- connect the ear guides properly
                self.__connect_guides(mod = self.ear.gd.mod, 
                                      side = self.ear.gd.side,
                                      obj = [self.gd.g_jnt[0],
                                             self.ear.jnt[iter][0]], 
                                      position = [self.gd.position[0],
                                                  self.ear.position[iter][0]])
                if mirror:
                    self.__connect_guides(mod = self.ear.gd.mod, 
                                          side = self.ear.gd.mirror_side,
                                          obj = [self.gd.g_jnt[0], 
                                                 self.ear.mirror_ctl[iter][0]], 
                                          position = [self.gd.position[0],
                                                      self.ear.mirror_pos[iter][0]])
                #--- hook the ear guides to the midSkull
                hook.Hook(mod = self.ear, 
                          hookParent = self.gd.g_ctl[0], 
                          hookChild = self.ear.grp[iter][0], 
                          hookType = 'parentConstraint')
    #END def __head_ear_setup()

    def __connect_guides(self, 
                           mod = None, 
                           side = None,
                           obj = None, 
                           position = [0,0,0]):
        #--- this method creates the curve which connects the guide controls        
        crv = cmds.curve(degree = 1, point = position)
        cmds.parent(crv, self.gd.extras)      
        crvShp = cmds.listRelatives(crv, allDescendents = True)[0]
        crvShp = cmds.rename(crvShp, crv + 'Shape')
        rel = cmds.listRelatives(crv, allDescendents = 1)[0]

        #--- connect the cvs to the controls by matrix
        attr = attribute.Attribute()
        nd   = node.Node()
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, rel], 
                             attribute = ['outputTranslate', 
                                          'controlPoints[' + `i` + ']'])
        #--- set the displayType of the curve Shape to template
        attr.setColor(node = crvShp, displayType = 1)
    #END def __connect_guides()

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

    def __head_cleanup(self, 
                         mouth = True,
                         jaw = True,
                         eye = True,
                         ear = True):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls        
        attr = attribute.Attribute()
        attr.lockAll(node = self.gd.g_grp)
        if mouth:
            attr.lockAll(node = self.mouth.gd.g_grp)
        if jaw:
            attr.lockAll(node = self.jaw.gd.g_grp)
        if eye:
            attr.lockAll(node = self.eye.gd.g_grp)
        if ear:
            attr.lockAll(node = self.ear.gd.g_grp)            
        attr.lockAttr(node = self.gd.g_ctl, 
                      attribute = ['tx', 'ry', 'rz','s', 'v'])
        for i in cmds.ls('*DCM*', '*PAC*', '*Constraint*', '*curve*'):
            cmds.setAttr(i + '.ihi', 0)
        cmds.select(clear = True)
    #END def __head_cleanup()

    def __main_setup(self,
                       character = None,
                       mod = None,
                       side = None,
                       name = None,
                       size = 1,
                       shape = 0, 
                       color = 0, 
                       position = [0,0,0],
                       eye = True,
                       eyesAmount = 1,
                       jaw = True,
                       mouth = True, 
                       ear = True,
                       earsAmount = 1,                                             
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
        self.__head_setup(character = character,
                          mod = mod,
                          side = side,
                          name = name,
                          size = size,
                          shape = shape,
                          color = color,
                          position = position,
                          eye = eye,
                          eyesAmount = eyesAmount,
                          jaw = jaw,
                          mouth = mouth,
                          ear = ear,
                          earsAmount = earsAmount,                           
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
        #--- mod specific cleanup        
        self.__head_cleanup(mouth = mouth,
                            jaw = jaw,
                            eye = eye,
                            ear = ear)
    #END def __main_setup
#END class QuadrupedHeadGuide()