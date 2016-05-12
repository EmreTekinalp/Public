'''
Created on 13.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Foot module with different foot classes
'''

from maya import cmds
from fundamentals import api, attribute, duplicate, ikhandle, joint, measure, node
from functions import control, flexiplane, hook, jointchain, puppet
from mods import hip, mod
reload(api)
reload(attribute)
reload(control)
reload(duplicate)
reload(flexiplane)
reload(joint)
reload(hip)
reload(hook)
reload(ikhandle)
reload(jointchain)
reload(measure)
reload(mod)
reload(node)
reload(puppet)


class BipedFootGuide(mod.MasterMod):
    """
    This class creates a biped foot guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'foot',
                  side = 'L',
                  name = ['ankle', 'ball', 'toe'],
                  suffix = 'GCTL',
                  size = 0.5,
                  shape = 2,
                  orientation = [0,0,0], 
                  color = 15,
                  position = [[3, 1, 0],[3, 0, 2],[3, 0, 3]],
                  rotation = [0,0,0],
                  upVectorOffset = [6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None,
                  heel = 'heel',
                  heelPosition = [0,0,-3],
                  inBank = 'inBank',
                  inBankPosition = [-1.5,0,0],
                  outBank = 'outBank',
                  outBankPosition = [1.5,0,0]):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedFootGuide, self).__init__()

        #args
        self.character       = character
        self.mod             = mod
        self.side            = side
        self.name            = name
        self.suffix          = suffix
        self.size            = size
        self.shape           = shape
        self.orientation     = orientation
        self.color           = color
        self.position        = position
        self.rotation        = rotation        
        self.upVectorOffset  = upVectorOffset
        self.aimVector       = aimVector
        self.upVector        = upVector
        self.rotateOrder     = rotateOrder
        self.flip            = flip
        self.mirrorGuideObj  = mirrorGuideObj
        self.heel            = heel
        self.heelPosition    = heelPosition
        self.inBank          = inBank
        self.inBankPosition  = inBankPosition
        self.outBank         = outBank
        self.outBankPosition = outBankPosition

        #vars
        self.heel_ctl     = None
        self.in_bank_ctl  = None
        self.out_bank_ctl = None

        #methods
        self.__main_setup()
    #END def __init__()

    def __foot_setup(self):
        #--- this method is a self.mod specific setup
        attr = attribute.Attribute()
        if not self.mirrorGuideObj:
            #--- unlock the proper groups to work with them
            attr.lockAttr(node = self.gd.g_grp, 
                          attribute = ['t', 'r', 's'], 
                          lock = False)
            #--- parent the controls fk style
            for i in range(len(self.gd.g_grp)):
                j = i + 1
                if not j == len(self.gd.g_grp):
                    cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i])
        #--- create the message connection setup
        self.__connect_message()                 
        #--- create the footroll_setup
        self.__foot_roll_setup()
    #END def __foot_setup()        

    def __foot_roll_setup(self):
        #--- this method creates the proper guides for the footRollSetup
        if self.mirrorGuideObj:
            parent = self.gd.side_mod
            ori = [[0,0,0], [0,180,0]]
        else:
            parent = self.gd.g_ctl[1]
            ori = [[0,180,0], [0,0,0]]
        #--- create the heel guide ctl
        self.heel_ctl = self.__create_foot_roll_guide(side = self.side, 
                                                      name = self.heel, 
                                                      suffix = self.suffix,
                                                      size = self.size, 
                                                      shape = 1, 
                                                      color = self.color, 
                                                      position = self.heelPosition,
                                                      orientation = [90,0,0],
                                                      parent = parent)
        #--- create the innerBank guide ctl
        self.in_bank_ctl = self.__create_foot_roll_guide(side = self.side, 
                                                         name = self.inBank, 
                                                         suffix = self.suffix,
                                                         size = self.size * 0.5, 
                                                         shape = 4, 
                                                         color = self.color, 
                                                         position = self.inBankPosition,
                                                         orientation = ori[0],
                                                         parent = parent)
        #--- create the outerBank guide ctl
        self.out_bank_ctl = self.__create_foot_roll_guide(side = self.side, 
                                                          name = self.outBank, 
                                                          suffix = self.suffix,
                                                          size = self.size * 0.5, 
                                                          shape = 4, 
                                                          color = self.color, 
                                                          position = self.outBankPosition,
                                                          orientation = ori[1],
                                                          parent = parent)
    #END def __foot_roll_setup()

    def __create_foot_roll_guide(self,
                                    side = None,
                                    name = None,
                                    suffix = None,
                                    size = 1,
                                    shape = 0,
                                    color = 0,
                                    position = [0,0,0],
                                    orientation = [0,0,0],
                                    parent = None):
        #--- this method creates a foot roll guide
        attr = attribute.Attribute()
        #--- create the foot roll guide ctl
        roll_guide = control.Control(side = side, 
                                     name = self.gd.mod + 
                                            'Roll' +
                                            name[0].upper() + 
                                            name[1:], 
                                     suffix = suffix, 
                                     size = size, 
                                     shape = shape, 
                                     color = color, 
                                     position = position,
                                     orientation = orientation,
                                     parent = parent)
        #--- create the foot roll joint
        jnt = joint.Joint(side = side, 
                          name = self.gd.mod + 
                                 'Roll' +
                                 name[0].upper() + 
                                 name[1:], 
                          suffix = 'GJNT', 
                          radius = size * 0.9)
        #--- parent the joint under the foot roll control
        cmds.parent(jnt.name, roll_guide.transform)
        #--- zero out the joint's self.position
        attr.setAttr(node = jnt.name, attribute = 't', value = [0,0,0])
        #--- hide joint
        cmds.setAttr(jnt.name + '.v', 0)

        #--- add a message attribute to the guide joints
        if jnt.name:
            cmds.addAttr(jnt.name, 
                         longName = 'connection', 
                         shortName = 'connection', 
                         attributeType = 'message')
            cmds.addAttr(jnt.name, 
                         longName = 'footRoll', 
                         shortName = 'footRoll', 
                         attributeType = 'message')
        #--- connect the message to the ball joint
        cmds.connectAttr(self.gd.g_jnt[1] + '.message', 
                         jnt.name + '.connection')
        cmds.connectAttr(jnt.name + '.message', 
                         jnt.name + '.footRoll')
        #--- lock all attributes of the joint
        attr.lockAll(node = jnt.name)
        return roll_guide
    #END def __create_foot_roll_guide()

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
    #END def __connect_message()

    def __mirror_foot_setup(self):
        #--- this method mirrors the guides properly and set them up
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the mirror node and the proper connections
        guides = [self.mirrorGuideObj.heel_ctl, 
                  self.mirrorGuideObj.in_bank_ctl, 
                  self.mirrorGuideObj.out_bank_ctl]
        footroll = [self.heel_ctl, self.in_bank_ctl, self.out_bank_ctl]
        guide_names = [self.heel, self.inBank, self.outBank]
        mirrors = []
        for obj in range(len(guides)):
            mirror = nd.mirrorSwitch(name = (self.side + '_' + self.mod + 
                                             guide_names[obj][0].upper() + 
                                             guide_names[obj][1:]))
            attr.connectAttr(node = [guides[obj].transform, mirror], 
                             attribute = ['worldMatrix', 'inputMatrix'])
            for axis in 'xyz':
                attr.lockAttr(node = [guides[obj].group], 
                              attribute = ['t', 'r'], lock = False, show = True)
                #--- connect outPos and outRot with translate and rotate
                attr.connectAttr(node = [mirror, footroll[obj].group], 
                                 attribute = ['op' + axis, 't' + axis])
                attr.connectAttr(node = [mirror, footroll[obj].group], 
                                 attribute = ['or' + axis, 'r' + axis])
            cmds.setAttr(mirror + '.ihi', 0)
            mirrors.append(mirror)
        self.mirrors = mirrors
    #END def __mirror_foot_setup()

    def __add_mirror_attributes(self):
        #--- this method adds mirror attributes to the main mod
        attr = attribute.Attribute()
        #--- get the mirror guides
        footroll = [self.heel_ctl, self.in_bank_ctl, self.out_bank_ctl]
        #--- check if attribute exists
        if cmds.objExists(self.gd.main_mod + '.mirror'):
            #--- connect the mirror attributes properly with the main mod
            for i in self.mirrors:
                attr.connectAttr(node = [self.gd.main_mod, i], 
                                 attribute = ['mirror', 'mirror'])
        if cmds.objExists(self.gd.main_mod + '.mirrorLock'):
            for i in footroll:
                attr.connectAttr(node = [self.gd.main_mod, i.shape], 
                                 attribute = ['mirrorLock', 
                                              'drawOverride.overrideDisplayType'])
    #END def __add_mirror_attributes()

    def __cleanup(self):
        #--- this method is a self.mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAttr(node = [self.gd.g_ctl[1], self.gd.g_ctl[2]], 
                      attribute = ['tx', 'r', 's', 'v'], 
                      lock = True, show = False)
        #--- lock attributes on first guide
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['rx', 'rz', 's', 'v'], 
                      lock = True, show = False)

        #--- lock unnecessary attributes on the heel guide
        attr.lockAttr(node = self.heel_ctl.transform, 
                      attribute = ['tx','ty','r','s','v'])
        attr.lockAll(node = self.heel_ctl.group)
        #--- lock unnecessary attributes on the outBank guide
        attr.lockAttr(node = self.out_bank_ctl.transform, 
                      attribute = ['ty','tz','r','s','v'])
        attr.lockAll(node = self.out_bank_ctl.group)
        #--- lock unnecessary attributes on the innerBank guide
        attr.lockAttr(node = self.in_bank_ctl.transform, 
                      attribute = ['ty','tz','r','s','v'])
        attr.lockAll(node = self.in_bank_ctl.group)

        #--- hide isHistoricalInteresting nodes
        for i in cmds.ls('*' + self.mod + '*Shape*', 
                         '*' + self.mod + '*_AIM*', 
                         '*' + self.mod + '*_GRP*', 
                         '*' + self.mod + '*_CTL*', 
                         '*' + self.mod + '*_DCM*'):
            cmds.setAttr(i + '.ihi', 0)
        cmds.select(clear = True)
    #END def __cleanup()

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
        self.__foot_setup()
        #--- mirror setup
        if self.mirrorGuideObj:
            #--- mirror mode on this node
            self.__mirror_foot_setup()
            #--- add mirror attribute to the main mod
            self.__add_mirror_attributes()
        #--- mod specific cleanup
        self.__cleanup()
    #END def __main_setup()
#END class BipedFootGuide()


class BipedFootPuppet(puppet.Puppet):
    """
    This class creates a biped foot rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None,
                  fk = True,
                  ik = True,
                  ikfk = 'Blend'):
        ########################################################################
        #superclass inheritance initialisation        
        super(BipedFootPuppet, self).__init__(character = character,
                                              guideObj = guideObj)

        #--- args
        self.character  = character
        self.guideObj   = guideObj
        self.puppetObj  = puppetObj
        self.fk         = fk
        self.ik         = ik
        self.ikfk       = ikfk

        #--- vars
        self.heel      = None
        self.in_bank   = None
        self.out_bank  = None

        self.heel_pos      = None
        self.in_bank_pos   = None
        self.out_bank_pos  = None

        self.controls_fk  = []
        self.controls_ik  = []
        self.ocn_fk       = []

        self.heel_grp     = None
        self.out_bank_grp = None
        self.in_bank_grp  = None
        self.toe_grp      = None
        self.ball_grp     = None
        self.ankle_grp    = None

        #--- methods
        self.__create_puppet()
    #END def __init__()

    def __filter_joints(self):
        #--- this method filters the main joint bones from the helper ones
        for jnt in self.joints:
            rel = cmds.listRelatives(jnt, children = True)
            if rel:
                for i in rel:
                    if cmds.objExists(i + '.footRoll'):
                        cmds.parent(i, world = True)
                        attr = cmds.listConnections(i + '.footRoll')
                        if attr:
                            attr = attr[0]
                            #--- get the filterNames of the footRoll
                            heel = (self.guideObj.heel[0].upper() + 
                                    self.guideObj.heel[0][1:])
                            inBank = (self.guideObj.inBank[0][0].upper() + 
                                      self.guideObj.inBank[0][1:])
                            outBank = (self.guideObj.outBank[0][0].upper() + 
                                       self.guideObj.outBank[0][1:])
                            #--- get the positions
                            pos = cmds.xform(attr, query = True, 
                                             translation = True,
                                             worldSpace = True)
                            if heel in attr:
                                if self.side in attr:
                                    self.heel = attr
                                    self.heel_pos = pos
                            if inBank in attr:
                                if self.side in attr:
                                    self.in_bank = attr
                                    self.in_bank_pos = pos
                            if outBank in attr:
                                if self.side in attr:
                                    self.out_bank = attr
                                    self.out_bank_pos = pos
    #END def __filter_joints()

    def __get_joints(self):
        #--- this method gets the skeleton joints and stores them properly
        self.joints = self.joints
        if self.fk:
            self.joints_fk = duplicate.Duplicate(obj = self.joints[0], 
                                                      replace = ['_JNT', 'FK_JNT']).result
        if self.ik:
            self.joints_ik = duplicate.Duplicate(obj = self.joints[0], 
                                                      replace = ['_JNT', 'IK_JNT']).result
    #END def __get_joints()

    def __setup_joints(self):
        #--- this method connects the ik fk joints with the bind one
        attr = attribute.Attribute()
        nd = node.Node()
        if self.fk:
            #--- constraint fk joints to the bind ones
            self.pac = nd.parentConstraint(objA = self.joints_fk,
                                           objB = self.joints,
                                           maintainOffset = False)
            #--- disable skin tag
            for fk in self.joints_fk:
                attr.setAttr(fk, ['SKIN'], 0)
        if self.ik:
            #--- constraint ik joints to the bind ones
            self.pac = nd.parentConstraint(objA = self.joints_ik,
                                           objB = self.joints, 
                                           maintainOffset = False)
            #--- disable skin tag
            for ik in self.joints_ik:
                attr.setAttr(ik, ['SKIN'], 0)
    #END def __setup_joints()

    def __create_fk_controls(self):
        #--- this method creates the fk controls
        #--- fk controls
        for pos in range(len(self.joint_position) - 1):
            fk_ctl = control.Control(side = self.side, 
                                     name = (self.mod 
                                             + self.name[pos][0].upper()
                                             + self.name[pos][1:] + 'FK'), 
                                     suffix = 'CTL', 
                                     size = self.size, 
                                     shape = 15, 
                                     color = self.color, 
                                     position = [0,0,0], 
                                     rotation = [0,0,0],
                                     orientation = [0,0,90], 
                                     parent = self.joints_fk[pos])
            cmds.parent(fk_ctl.group, self.side_ctl_grp) 
            self.controls_fk.append(fk_ctl)
    #END def __create_fk_controls()

    def __setup_fk_controls(self):
        #--- this method setups the fk controls
        nd = node.Node()
        #--- parent the fk controls properly
        ctl = self.controls_fk
        for i in range(len(ctl)):
            j = i + 1
            if not j == len(ctl):
                cmds.parent(ctl[j].group, ctl[i].transform)
                #--- orientConstraint the joints to the controls
                ocn = nd.orientConstraint(objA = ctl[i].transform,
                                          objB = self.joints_fk[i], 
                                          name = (self.side + '_' + self.mod + 
                                                  self.name[i][0].upper() + 
                                                  self.name[i][1:]), 
                                          maintainOffset = False)[0]
                self.ocn_fk.append(ocn)
            else:
                #--- orientConstraint the last joint to the control
                ocn = nd.orientConstraint(objA = ctl[i].transform,
                                          objB = self.joints_fk[i], 
                                          name = (self.side + '_' + self.mod + 
                                                  self.name[i][0].upper() + 
                                                  self.name[i][1:]), 
                                          maintainOffset = False)[0]
                self.ocn_fk.append(ocn)
    #END def __setup_fk_controls()

    def __create_ik_controls(self):
        #--- this method creates the ik controls
        self.controls_ik = control.Control(side = self.side, 
                                           name = self.mod + 'IK',
                                           suffix = 'CTL', 
                                           size = self.size, 
                                           shape = 16, 
                                           color = self.color, 
                                           position = self.joint_position[0], 
                                           rotation = [0,0,0],
                                           offset = [0,-1,1],
                                           orientation = [0,0,0],
                                           parent = self.side_ctl_grp)
    #END def __create_ik_controls()

    def __create_foot_roll_groups(self):
        #--- this method creates the ik controls
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create footRoll groups
        heelRoll = nd.transform(name = (self.side + '_' + self.mod + 
                                        self.guideObj.heel[0].upper() + 
                                        self.guideObj.heel[1:] + 'Roll'),
                                suffix = 'GRP', 
                                position = self.heel_pos)
        heel = nd.transform(name = (self.side + '_' + self.mod + 
                                    self.guideObj.heel[0].upper() + 
                                    self.guideObj.heel[1:]),
                            suffix = 'GRP', 
                            position = self.heel_pos)
        outBank = nd.transform(name = (self.side + '_' + self.mod + 
                                       self.guideObj.outBank[0].upper() + 
                                       self.guideObj.outBank[1:]),
                               suffix = 'GRP',
                               position = self.out_bank_pos)
        inBank = nd.transform(name = (self.side + '_' + self.mod + 
                                      self.guideObj.inBank[0].upper() + 
                                      self.guideObj.inBank[1:]),
                              suffix = 'GRP',
                              position = self.in_bank_pos)
        ballRaise = nd.transform(name = (self.side + '_' + self.mod + 
                                       self.name[-2][0].upper() + 
                                       self.name[-2][1:] + 'Raise'),
                                suffix = 'GRP',
                                position = self.joint_position[-2])        
        toeRoll = nd.transform(name = (self.side + '_' + self.mod + 
                                       self.name[-1][0].upper() + 
                                       self.name[-1][1:] + 'Roll'),
                               suffix = 'GRP',
                               position = self.joint_position[-1])
        toe = nd.transform(name = (self.side + '_' + self.mod + 
                                   self.name[-1][0].upper() + 
                                   self.name[-1][1:]),
                           suffix = 'GRP',
                           position = self.joint_position[-1])
        ballRoll = nd.transform(name = (self.side + '_' + self.mod + 
                                        self.name[-2][0].upper() + 
                                        self.name[-2][1:] + 'Roll'),
                                suffix = 'GRP',
                                position = self.joint_position[-2])
        ball = nd.transform(name = (self.side + '_' + self.mod + 
                                    self.name[-2][0].upper() + 
                                    self.name[-2][1:]),
                            suffix = 'GRP',
                            position = self.joint_position[-2])
        ankle = nd.transform(name = (self.side + '_' + self.mod + 
                                     self.name[0][0].upper() + 
                                     self.name[0][1:]),
                             suffix = 'GRP',
                             position = self.joint_position[0])

        #--- parent the footRollSetup properly
        cmds.parent(heelRoll, self.controls_ik.transform)
        cmds.parent(heel, heelRoll)        
        cmds.parent(outBank, heel)
        cmds.parent(inBank, outBank)
        cmds.parent(ballRaise, inBank)
        cmds.parent(toeRoll, ballRaise)
        cmds.parent(toe, toeRoll)
        cmds.parent(ballRoll, toe)
        cmds.parent(ball, ballRoll)
        cmds.parent(ankle, ball)        

        #--- pointConstraint the ankle group to the leg ik
        nd.pointConstraint(objA = ankle, 
                           objB = self.puppetObj.ik_handle[0],
                           suffix = 'PCN', 
                           maintainOffset = False)

        self.heel_roll_grp  = heelRoll
        self.heel_grp       = heel
        self.out_bank_grp   = outBank
        self.in_bank_grp    = inBank
        self.ball_raise_grp = ballRaise
        self.toe_roll_grp   = toeRoll
        self.toe_grp        = toe
        self.ball_roll_grp  = ballRoll
        self.ball_grp       = ball
        self.ankle_grp      = ankle
    #END def __create_foot_roll_groups()

    def __add_foot_roll_attributes(self):
        #--- this method adds the foot roll attributes
        attr = attribute.Attribute()
        #--- rockAndRoll
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'rockAndRoll',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- heelPivot
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'heelSwivel',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- heelRaise
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'heelRaise',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- heelTwist
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'heelTwist',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- bank
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'bank',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- ballPivot
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'ballSwivel',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- ballRaise
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'ballRaise',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- ballTwist
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'ballTwist',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- toePivot
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'toeSwivel',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- toeRaise
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'toeRaise',
                     attrType = 'float',
                     min = -10,
                     max = 10)
        #--- toeTwist
        attr.addAttr(node = self.controls_ik.transform,
                     attrName = 'toeTwist',
                     attrType = 'float',
                     min = -10,
                     max = 10)
    #END def __add_foot_roll_attributes()

    def __setup_foot_roll_system(self):
        #--- this method setups the foot roll system
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create utility nodes for the rockAndRoll setup
        neg_heel_roll_rmv = nd.remapValue(name = (self.side + '_' + self.mod + 
                                                  'NegativeHeelRoll'), 
                                          inputMin = 0, 
                                          inputMax = -10, 
                                          outputMin = 0, 
                                          outputMax = -90)
        neg_ball_roll_rmv = nd.remapValue(name = (self.side + '_' + self.mod + 
                                                  'NegativeBallRoll'), 
                                          inputMin = -5, 
                                          inputMax = -10, 
                                          outputMin = 0, 
                                          outputMax = -60)
        pos_ball_A_roll_rmv = nd.remapValue(name = (self.side + '_' +
                                                    self.mod + 
                                                    'PositiveBallRollA'), 
                                            inputMin = 5, 
                                            inputMax = 10, 
                                            outputMin = 22.5, 
                                            outputMax = -100)    
        pos_ball_B_roll_rmv = nd.remapValue(name = (self.side + '_' +
                                                    self.mod + 
                                                    'PositiveBallRollB'), 
                                            inputMin = 0, 
                                            inputMax = 10, 
                                            outputMin = 0, 
                                            outputMax = 45)
        pos_toe_roll_rmv = nd.remapValue(name = (self.side + '_' +
                                                 self.mod + 
                                                 'PositiveToeRoll'), 
                                         inputMin = 3, 
                                         inputMax = 10, 
                                         outputMin = 0, 
                                         outputMax = 150)
        pos_ball_roll_cnd = nd.condition(name = (self.side + '_' +
                                                 self.mod + 
                                                 'PositiveBallRoll'),
                                         secondTerm = 5,
                                         operation = 4)

        #--- connect the rockAndRoll attributes with the necessary nodes
        attr.connectAttr(node = [self.controls_ik.transform, neg_heel_roll_rmv], 
                         attribute = ['rockAndRoll', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, neg_ball_roll_rmv], 
                         attribute = ['rockAndRoll', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, pos_ball_A_roll_rmv], 
                         attribute = ['rockAndRoll', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, pos_ball_B_roll_rmv], 
                         attribute = ['rockAndRoll', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, pos_toe_roll_rmv], 
                         attribute = ['rockAndRoll', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, pos_ball_roll_cnd], 
                         attribute = ['rockAndRoll', 'firstTerm'])

        attr.connectAttr(node = [neg_heel_roll_rmv, self.heel_roll_grp], 
                         attribute = ['outValue', 'rx'])
        attr.connectAttr(node = [neg_ball_roll_rmv, self.ball_raise_grp], 
                         attribute = ['outValue', 'rx'])        
        attr.connectAttr(node = [pos_toe_roll_rmv, self.toe_roll_grp], 
                         attribute = ['outValue', 'rx'])        
        attr.connectAttr(node = [pos_ball_A_roll_rmv, pos_ball_roll_cnd], 
                         attribute = ['outValue', 'colorIfFalseR'])
        attr.connectAttr(node = [pos_ball_B_roll_rmv, pos_ball_roll_cnd], 
                         attribute = ['outValue', 'colorIfTrueR'])
        attr.connectAttr(node = [pos_ball_roll_cnd, self.ball_roll_grp], 
                         attribute = ['outColorR', 'rx'])

        #--- create utility nodes for the bank setup
        in_bank_roll_rmv = nd.remapValue(name = (self.side + '_' +
                                                  self.mod + 
                                                  'InBankRoll'), 
                                         inputMin = 0, 
                                         inputMax = 10, 
                                         outputMin = 0, 
                                         outputMax = 100)
        out_bank_roll_rmv = nd.remapValue(name = (self.side + '_' +
                                                  self.mod + 
                                                  'OutBankRoll'), 
                                          inputMin = 0, 
                                          inputMax = -10, 
                                          outputMin = 0, 
                                          outputMax = -100)

        #--- connect the bank attributes with the necessary nodes
        attr.connectAttr(node = [self.controls_ik.transform, in_bank_roll_rmv], 
                         attribute = ['bank', 'inputValue'])
        attr.connectAttr(node = [self.controls_ik.transform, out_bank_roll_rmv], 
                         attribute = ['bank', 'inputValue'])
        attr.connectAttr(node = [in_bank_roll_rmv, self.in_bank_grp], 
                         attribute = ['outValue', 'rz'])
        attr.connectAttr(node = [out_bank_roll_rmv, self.out_bank_grp], 
                         attribute = ['outValue', 'rz'])

        #--- create utility nodes for the heel, ball and toe setup
        heel_mlt = nd.multiplyDivide(name = (self.side + '_' + self.mod + 'Heel'), 
                                     input2X = 10, 
                                     input2Y = 10,
                                     input2Z = 10)
        ball_mlt = nd.multiplyDivide(name = (self.side + '_' + self.mod + 'Ball'), 
                                     input2X = 10, 
                                     input2Y = 10,
                                     input2Z = 10)
        toe_mlt = nd.multiplyDivide(name = (self.side + '_' + self.mod + 'Toe'), 
                                    input2X = 10, 
                                    input2Y = 10,
                                    input2Z = 10)

        #--- connect the heel, ball and toe attributes with the necessary nodes
        attr.connectAttr(node = [self.controls_ik.transform, heel_mlt], 
                         attribute = ['heelRaise', 'input1X'])
        attr.connectAttr(node = [self.controls_ik.transform, heel_mlt], 
                         attribute = ['heelSwivel', 'input1Y'])
        attr.connectAttr(node = [self.controls_ik.transform, heel_mlt], 
                         attribute = ['heelTwist', 'input1Z'])
        attr.connectAttr(node = [heel_mlt, self.heel_grp], 
                         attribute = ['outputX', 'rx'])
        attr.connectAttr(node = [heel_mlt, self.heel_grp], 
                         attribute = ['outputY', 'ry'])
        attr.connectAttr(node = [heel_mlt, self.heel_grp], 
                         attribute = ['outputZ', 'rz'])

        attr.connectAttr(node = [self.controls_ik.transform, ball_mlt], 
                         attribute = ['ballRaise', 'input1X'])
        attr.connectAttr(node = [self.controls_ik.transform, ball_mlt], 
                         attribute = ['ballSwivel', 'input1Y'])
        attr.connectAttr(node = [self.controls_ik.transform, ball_mlt], 
                         attribute = ['ballTwist', 'input1Z'])
        attr.connectAttr(node = [ball_mlt, self.ball_grp], 
                         attribute = ['outputX', 'rx'])
        attr.connectAttr(node = [ball_mlt, self.ball_grp], 
                         attribute = ['outputY', 'ry'])
        attr.connectAttr(node = [ball_mlt, self.ball_grp], 
                         attribute = ['outputZ', 'rz'])

        attr.connectAttr(node = [self.controls_ik.transform, toe_mlt], 
                         attribute = ['toeRaise', 'input1X'])
        attr.connectAttr(node = [self.controls_ik.transform, toe_mlt], 
                         attribute = ['toeSwivel', 'input1Y'])
        attr.connectAttr(node = [self.controls_ik.transform, toe_mlt], 
                         attribute = ['toeTwist', 'input1Z'])
        attr.connectAttr(node = [toe_mlt, self.toe_grp], 
                         attribute = ['outputX', 'rx'])
        attr.connectAttr(node = [toe_mlt, self.toe_grp], 
                         attribute = ['outputY', 'ry'])
        attr.connectAttr(node = [toe_mlt, self.toe_grp], 
                         attribute = ['outputZ', 'rz'])
    #END def __setup_foot_roll_system()

    def __setup_ik_handles(self):
        #--- this method setups the ik handles, parents them under the thigh
        ik = ikhandle.IkHandle()
        #--- create the foot ik controls
        self.ball_grp = ik.ikRPsolver(startJoint = self.joints_ik[0], 
                                      endEffector = self.joints_ik[1], 
                                      side = self.side, 
                                      name = self.mod + 'Ball', 
                                      suffix = 'IK',
                                      parent = self.ball_grp,
                                      hide = True)

        self.toe_grp = ik.ikRPsolver(startJoint = self.joints_ik[1], 
                                     endEffector = self.joints_ik[2], 
                                     side = self.side, 
                                     name = self.mod + 'Toe', 
                                     suffix = 'IK',
                                     parent = self.toe_grp,
                                     hide = True)
    #END def __setup_ik_handles()

    def __setup_ik_controls(self):
        #--- this method setups the ik controls
        attr = attribute.Attribute()
        nd = node.Node()
        #--- get the ik controls
        ctl = self.controls_ik
        #--- create a parentConstraint of the thigh ik to the thigh joint
        self.pac_ik = nd.parentConstraint(objA = ctl.transform, 
                                          objB = self.joints_ik[0],
                                          suffix = 'PAC',
                                          maintainOffset = False)

        #--- if there is leg setup create the same attributes as on the leg
        if self.puppetObj.ikfk_blend.transform:
            if cmds.objExists(self.puppetObj.ikfk_blend.transform + '.fkIk'):
                #--- add an fkik blend attribute
                attr.addAttr(node = ctl.transform,
                             attrName = 'fkIk',
                             attrType = 'float',
                             min = 0,
                             max = 10,
                             default = 10)
            if cmds.objExists(self.puppetObj.ikfk_blend.transform + '.ikStretch'):
                #--- add an ikStretch attribute
                attr.addAttr(node = ctl.transform,
                             attrName = 'ikStretch',
                             attrType = 'float',
                             min = 0,
                             max = 1,
                             default = 0)
    #END def __setup_ik_controls()

    def __setup_ikfk(self):
        #--- this method creates an ikfk blend or ikfk spaceSwitch
        nd = node.Node()
        attr = attribute.Attribute()
        #--- delete constraints
        cmds.delete(self.ocn_fk[0], self.pac_ik)
        #--- constraint the fk and ik joints
        nd.parentConstraint(objA = self.controls_fk[0].transform, 
                            objB = self.joints_fk[0], 
                            suffix = 'PAC')        
        nd.parentConstraint(objA = self.puppetObj.hook_ik, 
                            objB = self.joints_ik[0], 
                            suffix = 'PAC')
        nd.parentConstraint(objA = self.puppetObj.hook_fk, 
                            objB = self.controls_fk[0].group, 
                            suffix = 'PAC')
        attr.lockAttr(node = self.puppetObj.controls_ik[0].group, 
                      attribute = ['t', 'r'], lock = False, show = True)
        nd.parentConstraint(objA = self.controls_ik.transform, 
                            objB = self.puppetObj.controls_ik[0].group, 
                            suffix = 'PAC')        
        if self.ikfk == 'Blend':
            self.__setup_blend()
    #END def __setup_ikfk()

    def __setup_blend(self):
        #--- this method creates a blending setup between ik and fk
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create proper utility nodes to setup ikfk Blend
        mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkFkBlend', 
                                operation = 2,
                                input2X = 10,
                                lockAttr = 'input2X')
        rev = nd.reverse(name = self.side + '_' + self.mod + 'IkFkBlend')
        #--- connect nodes properly
        attr.connectAttr(node = [self.controls_ik.transform, mlt], 
                         attribute = ['fkIk', 'input1X'])
        attr.connectAttr(node = [mlt, rev], 
                         attribute = ['outputX', 'inputX'])
        #--- connect the nodes with the parentConstraint weights
        for pac in range(len(self.pac)):
            attr.connectAttr(node = [rev, self.pac[pac]], 
                             attribute = ['outputX', self.joints_fk[pac] + 'W0'])
            attr.connectAttr(node = [mlt, self.pac[pac]], 
                             attribute = ['outputX', self.joints_ik[pac] + 'W1'])
            #--- set the interpType of the parentConstraint to shortest(2)
            attr.setAttr(node = self.pac[pac], 
                         attribute = 'interpType', 
                         value = 2)
        #--- connect the nodes with the controls' visibility
        #--- fk controls
        for fk in range(len(self.controls_fk)):
            attr.connectAttr(node = [rev, self.controls_fk[fk].transform], 
                             attribute = ['outputX', 'visibility'])
        #--- connect ikfk blend attributes
        attr.connectAttr(node = [self.controls_ik.transform,
                                 self.puppetObj.ikfk_blend.transform], 
                         attribute = ['fkIk', 'fkIk'])
        #--- connect ikStretch attributes
        attr.connectAttr(node = [self.controls_ik.transform,
                                 self.puppetObj.ikfk_blend.transform], 
                         attribute = ['ikStretch', 'ikStretch'])
    #END def __setup_blend()

    def __cleanup(self):
        #--- this is the cleanup method
        attr = attribute.Attribute()
        #--- hide the extranodes group
        attr.setAttr(node = [self.side_extra_grp,
                             self.joints_fk[0],
                             self.joints_ik[0]],
                     attribute = 'v', 
                     value = 0)
        #--- delete the footRoll system joints
        cmds.delete(self.heel, self.in_bank, self.out_bank)
        #--- lock and hide leg_ikfk controls
        if self.puppetObj.ikfk_blend.transform:
            #--- hide the leg ikfk control and lock the attributes
            attr.setAttr(node = self.puppetObj.ikfk_blend.transform, 
                         attribute = ['v'], value = 0)
            attr.lockAll(node = self.puppetObj.ikfk_blend.transform)
    #END def __cleanup()

    def __create_puppet(self):
        #--- this is the main create method
        #--- filter the main joints
        self.__filter_joints()
        #--- get the bind, fk and ik joints
        self.__get_joints()
        #--- setup the ik, fk, bind joints
        self.__setup_joints()
        if self.fk:
            #--- create fk controls
            self.__create_fk_controls()
            #--- setup fk controls
            self.__setup_fk_controls()
        if self.ik:
            #--- create ik controls
            self.__create_ik_controls()
        #--- create foot roll groups
        self.__create_foot_roll_groups()
        #--- add foot roll attributes
        self.__add_foot_roll_attributes()
        #--- setup foot roll system
        self.__setup_foot_roll_system()
        if self.ik:
            #--- setup ik handles
            self.__setup_ik_handles()
            #--- setup ik controls
            self.__setup_ik_controls()
        if self.ik and self.fk:
            #--- setup the ikfk blend
            self.__setup_ikfk()
        #--- cleanup the mod
        self.__cleanup()
    #END def __create_puppet()
#END class BipedFootPuppet()


class QuadrupedFootGuide(mod.MasterMod):
    """
    This class creates a quadruped foot guide system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'foot',
                  side = 'L',
                  name = ['fetlock', 'pastern', 'hoof'],
                  size = 0.5,
                  shape = 2, 
                  color = 6, 
                  position = [[3.0, 2, -8],
                              [3.0, 1, -7.5],
                              [3.0, 0, -7]],
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  mirror = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedFootGuide, self).__init__()

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
                          hip = hip,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
    #END def __init__()

    def __foot_setup(self,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      hip = True,
                      upVectorOffset = [0,6,0],
                      aimVector = [1,0,0],
                      upVector = [0,1,0],
                      mirror = True):
        #--- this method is a mod specific setup
        #--- unlock the proper groups to work with them
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)
        #--- parent the controls fk style
        for i in range(len(self.gd.g_grp)):
            j = i + 1
            if not j == len(self.gd.g_grp):
                cmds.parent(self.gd.g_grp[j], self.gd.g_ctl[i]) 
        #--- create the message connection setup
        self.__connect_message()                
        #--- create the footroll_setup
        self.__foot_roll_setup(mod = mod,
                               side = side,
                               size =size,
                               shape =shape,
                               color = color)
    #END def __foot_setup()        

    def __foot_roll_setup(self, 
                            mod = None,
                            side = None,
                            size = 1,
                            shape = 0,
                            color = 0):
        #--- this method creates the proper guides for the footRollSetup
        #--- create the heel guide ctl
        self.heel = control.Control(side = side, 
                                    name = self.gd.mod + 'heel'.capitalize(), 
                                    suffix = 'GCTL', 
                                    size = size, 
                                    shape = 1, 
                                    color = color, 
                                    position = [0,0,-3],
                                    orientation = [90,0,0],
                                    parent = self.gd.g_ctl[-1])
        #--- create the outerBank guide ctl
        self.out_bank = control.Control(side = side, 
                                        name = self.gd.mod + 'outBank'.capitalize(), 
                                        suffix = 'GCTL', 
                                        size = size * 0.5, 
                                        shape = 4, 
                                        color = color, 
                                        position = [1.5,0,0],
                                        orientation = [0,180,0],
                                        parent = self.gd.g_ctl[-1])
        #--- create the innerBank guide ctl
        self.in_bank = control.Control(side = side, 
                                       name = self.gd.mod + 'inBank'.capitalize(), 
                                       suffix = 'GCTL', 
                                       size = size * 0.5, 
                                       shape = 4, 
                                       color = color, 
                                       position = [-1.5,0,0],
                                       orientation = [0,0,0],
                                       parent = self.gd.g_ctl[-1])        
    #END def __foot_roll_setup()

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

    def __foot_cleanup(self, 
                         mod = None):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_ctl[1:], 
                      attribute = ['tx', 'r', 's', 'v'], 
                      lock = True, show = False)
        #--- lock attributes on first guide
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['rx', 'rz', 's', 'v'], 
                      lock = True, show = False)

        #--- lock unnecessary attributes on the heel guide
        attr.lockAttr(node = self.heel.transform, 
                      attribute = ['tx','ty','r','s','v'])
        attr.lockAll(node = self.heel.group)
        #--- lock unnecessary attributes on the outBank guide
        attr.lockAttr(node = self.out_bank.transform, 
                      attribute = ['ty','tz','r','s','v'])
        attr.lockAll(node = self.out_bank.group)
        #--- lock unnecessary attributes on the innerBank guide
        attr.lockAttr(node = self.in_bank.transform, 
                      attribute = ['ty','tz','r','s','v'])
        attr.lockAll(node = self.in_bank.group)

        #--- hide isHistoricalInteresting nodes
        for i in cmds.ls('*' + mod + '*Shape*', 
                         '*' + mod + '*_AIM*', 
                         '*' + mod + '*_GRP*', 
                         '*' + mod + '*_CTL*', 
                         '*' + mod + '*_DCM*'):
            cmds.setAttr(i + '.ihi', 0)
        cmds.select(clear = True)
    #END def __foot_cleanup()

    def __main_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      hip = True,
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
        self.__foot_setup(mod = mod, 
                          side = side,
                          name = name, 
                          size = size, 
                          shape = shape, 
                          color = color,
                          position = position,
                          hip = hip,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          mirror = mirror)
        #--- mod specific cleanup
        self.__foot_cleanup(mod = mod)
    #END def __main_setup()
#END class QuadrupedFootGuide()
