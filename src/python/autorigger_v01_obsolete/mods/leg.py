'''
Created on 13.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Leg module with different leg classes
'''

from maya import cmds
from fundamentals import api, attribute, duplicate, ikhandle, measure, node
from functions import control, flexiplane, hook, jointchain, puppet
from mods import hip, mod
reload(api)
reload(attribute)
reload(control)
reload(duplicate)
reload(flexiplane)
reload(hip)
reload(hook)
reload(ikhandle)
reload(jointchain)
reload(measure)
reload(mod)
reload(node)
reload(puppet)


class BipedLegGuide(mod.MasterMod):
    """
    This class creates a biped leg guide system based on the specification made 
    in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'leg',
                  side = 'L',
                  name = ['thigh', 'knee', 'ankle'],
                  suffix = 'GCTL',
                  size = 0.75,
                  shape = 2,
                  orientation = [0,0,0],
                  color = 15,
                  position = [[3,11,0], [3,6,1], [3,1,0]],
                  rotation = [0,0,0],
                  upVectorOffset = [6,0,0],
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None,
                  hipEnable = True,
                  hipName = 'pelvis',
                  hipPosition = [1,11,0]):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedLegGuide, self).__init__()

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
        self.hipEnable        = hipEnable
        self.hipName          = hipName
        self.hipPosition      = hipPosition

        #vars
        self.hip = None

        #methods
        self.__main_setup()
    #END def __init__()

    def __leg_setup(self):
        #--- this method is a mod specific setup
        attr = attribute.Attribute()
        nd = node.Node()
        if not self.mirrorGuideObj:
            #--- unlock the proper groups to work with them
            attr.lockAttr(node = self.gd.g_grp, 
                          attribute = ['t', 'r', 's'], 
                          lock = False)
            #--- pointConstraint the kneeGuide to the other ones
            nd.pointConstraint(objA = [self.gd.g_ctl[0], self.gd.g_ctl[2]], 
                               objB = self.gd.g_grp[1],
                               name = (self.side + '_' + self.mod + 
                                       self.name[1][0].upper() + self.name[1][1:]))
            #--- parent the controls to the thigh ctl
            cmds.parent(self.gd.g_grp[1], self.gd.g_grp[2], self.gd.g_ctl[0])
        #--- create the message connection setup
        self.__connect_message()

        #--- create hip setup
        if self.hipEnable:
            self.__leg_hip_setup()
    #END def __leg_setup()        

    def __leg_hip_setup(self):
        #--- this method calls the hip mod
        attr = attribute.Attribute()
        nd = node.Node()
        if self.mirrorGuideObj:
            mirror_hip = self.mirrorGuideObj.hip
        else:
            mirror_hip = None
        #--- create the hip guide
        self.hip = hip.BipedHipGuide(character = self.character,
                                     side = self.side,
                                     name = self.hipName,
                                     size = self.size / 2,
                                     color = self.color,
                                     position = self.hipPosition,
                                     rotation = self.rotation,
                                     flip = self.flip,
                                     mirrorGuideObj = mirror_hip) 
        #--- connect the hip guides properly regarding the flip boolean
        self.__connect_guides(obj = [self.hip.gd.g_jnt[0], self.gd.g_jnt[0]], 
                              position = [self.hip.gd.position, 
                                          self.gd.position[0]])

        #--- unlock the proper groups to work with them
        attr.lockAttr(node = self.hip.gd.g_jnt_off, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)            
        #--- create the proper joint aim constraint
        nd.aimConstraint(target = self.gd.g_jnt[0], 
                         source = self.hip.gd.g_jnt_off[0],
                         aimVector = self.aimVector, 
                         upVector = self.upVector, 
                         worldUpObject = self.hip.gd.g_loc[0], 
                         worldUpType = 'object')            
        if self.mirrorGuideObj:
            #--- hook the leg guide to the hip
            hook.Hook(mod = self.hip, 
                      hookParent = self.hip.gd.g_ctl[0], 
                      hookChild = self.gd.g_grp[0], 
                      hookType = None,
                      hookMessage = True)
        else:
            #--- hook the leg guide to the hip
            hook.Hook(mod = self.hip, 
                      hookParent = self.hip.gd.g_ctl[0], 
                      hookChild = self.gd.g_grp[0], 
                      hookType = 'parentConstraint',
                      hookMessage = True)            
    #END def __leg_hip_setup()   

    def __connect_guides(self,
                           obj = None, 
                           position = [0,0,0]):
        #--- this method creates the curve which connects the guide controls
        attr = attribute.Attribute()
        nd   = node.Node()        
        #--- create the curves
        crv = cmds.curve(degree = 1, point = position)
        cmds.parent(crv, self.gd.extras)
        crvShp = cmds.listRelatives(crv, allDescendents = True)[0]
        crvShp = cmds.rename(crvShp, crv + 'Shape')
        shape = cmds.listRelatives(crv, allDescendents = 1)[0]
        #--- connect the cvs to the controls by matrix
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, shape], 
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
                        cmds.setAttr(self.gd.g_jnt[j] + '.connection', 
                                     lock = False)
                        cmds.connectAttr(self.gd.g_jnt[i] + '.message', 
                                         self.gd.g_jnt[j] + '.connection')
    #END def __connect_message()

    def __cleanup(self):
        #--- this method is a mod specific cleanup
        attr = attribute.Attribute()
        #--- hide unnecessary attributes from the guide controls
        attr.lockAttr(node = [self.gd.g_ctl[1], self.gd.g_ctl[2]], 
                      attribute = ['tx', 'r', 's', 'v'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['s', 'v'], 
                      lock = True, show = False)
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
        self.__leg_setup()
        #--- mod specific cleanup
        self.__cleanup()
    #END def __create()
#END class BipedLegGuide()


class BipedLegPuppet(puppet.Puppet):
    """
    This class creates a biped leg rig system based on the specification made in
    the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self, 
                  character = None,
                  guideObj = None,
                  puppetObj = None,
                  fk = True,
                  ik = True,
                  ikfk = 'Blend',
                  ikStretch = True,
                  ikBend = True,
                  autoHip = True,
                  softHip = True):
        ########################################################################
        #superclass inheritance initialisation
        super(BipedLegPuppet, self).__init__(character = character,
                                             guideObj = guideObj)

        #args
        self.character    = character
        self.guideObj     = guideObj
        self.puppetObj    = puppetObj
        self.fk           = fk
        self.ik           = ik
        self.ikfk         = ikfk
        self.ikStretch    = ikStretch
        self.ikBend       = ikBend
        self.autoHip      = autoHip
        self.softHip      = softHip

        #vars
        self.joints_fk     = []
        self.joints_ik     = []

        self.pac           = []
        self.ocn_fk        = []

        self.hook          = None
        self.hook_fk       = None
        self.hook_ik       = None

        self.controls_fk   = []
        self.controls_ik   = []

        self.ik_handle     = []
        self.ikfk_blend    = None

        self.bend_ctl      = None
        self.upper_leg_flp = None
        self.lower_leg_flp = None

        self.hip           = None
        self.joints_ah     = []
        self.ik_handle_ah  = [] 
        self.mlt           = [] 
        self.scapula       = None

        #methods
        self.__create_puppet()
    #END def __init__()

    def __get_ikfk_joints(self):
        #--- this method gets the skeleton joints and stores them properly
        if self.fk:
            self.joints_fk = duplicate.Duplicate(obj = self.joints[0], 
                                                 replace = ['_JNT', 'FK_JNT']).result
        if self.ik:
            self.joints_ik = duplicate.Duplicate(obj = self.joints[0], 
                                                 replace = ['_JNT', 'IK_JNT']).result
    #END def __get_ikfk_joints()

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

    def __add_hooks(self):
        #--- this method adds in and out hook groups to the leg modules
        nd = node.Node()
        #--- create hook node
        self.hook = nd.transform(name = (self.side + '_' + self.mod + 
                                         self.name[-1][0].upper() +
                                         self.name[-1][1:]), 
                                         suffix = 'HOOK', 
                                         parent = self.joints[-1])         
        if self.fk:
            #--- create fk hook node
            self.hook_fk = nd.transform(name = (self.side + '_' + self.mod + 
                                                self.name[-1][0].upper() +
                                                self.name[-1][1:] + 'FK'), 
                                                suffix = 'HOOK', 
                                                parent = self.joints_fk[-1])        
        if self.ik:
            #--- create ik hook node
            self.hook_ik = nd.transform(name = (self.side + '_' + self.mod + 
                                                self.name[-1][0].upper() +
                                                self.name[-1][1:] + 'IK'), 
                                                suffix = 'HOOK', 
                                                parent = self.joints_ik[-1])         
    #END def __add_hooks()

    def __create_fk_controls(self):
        #--- this method creates the fk controls
        #--- fk controls
        for pos in range(len(self.joint_position)):
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
                #--- orientConstraint the ctl joints to the controls
                ctl_ocn = nd.orientConstraint(objA = ctl[i].transform,
                                              objB = self.joints_fk[i], 
                                              name = (self.side + '_' + self.mod + 
                                                      self.name[i][0].upper() + 
                                                      self.name[i][1:]), 
                                              maintainOffset = False)[0]
                self.ocn_fk.append(ctl_ocn)
            else:
                #--- orientConstraint the side last joint to the control
                ctl_ocn = nd.orientConstraint(objA = ctl[i].transform,
                                              objB = self.joints_fk[i], 
                                              name = (self.side + '_' + self.mod + 
                                                      self.name[i][0].upper() + 
                                                      self.name[i][1:]), 
                                              maintainOffset = False)[0]
                self.ocn_fk.append(ctl_ocn)
    #END def __setup_fk_controls()

    def __create_ik_controls(self):
        #--- this method creates the ik controls
        #--- leg ik control
        leg_ctl = control.Control(side = self.side, 
                                  name = self.mod + 'IK',
                                  suffix = 'CTL', 
                                  size = self.size - 0.25, 
                                  shape = 2, 
                                  color = self.color, 
                                  position = self.joint_position[-1], 
                                  rotation = [0,0,0],
                                  orientation = [0,0,0])
        cmds.parent(leg_ctl.group, self.side_ctl_grp)
        self.controls_ik.append(leg_ctl)

        #--- thigh ik control
        thigh_ctl = control.Control(side = self.side, 
                                    name = self.mod + 'ThighIK',
                                    suffix = 'CTL', 
                                    size = self.size - 0.25, 
                                    shape = 0, 
                                    color = self.color, 
                                    position = self.joint_position[0], 
                                    rotation = [0,0,0],
                                    orientation = [0,0,0])
        cmds.parent(thigh_ctl.group, self.side_ctl_grp)
        self.controls_ik.append(thigh_ctl)
    #END def __create_ik_controls()

    def __setup_ik_handles(self):
        #--- this method setups the ik handles, parents them under the thigh
        ik = ikhandle.IkHandle()
        #--- get the thigh ik controls
        ctl = self.controls_ik[-1]
        self.ik_handle = ik.ikRPsolver(startJoint = self.joints_ik[0], 
                                       endEffector = self.joints_ik[-1], 
                                       side = self.side, 
                                       name = self.mod, 
                                       suffix = 'IK',
                                       parent = ctl.transform,
                                       hide = True)       
    #END def __setup_ik_handles()

    def __setup_ik_controls(self):
        #--- this method setups the ik controls
        nd = node.Node()
        #--- get the ik controls
        ctl = self.controls_ik        
        #--- parent the ik handle to the ankle ik 
        cmds.parent(self.ik_handle[0], ctl[0].transform)
        #--- create a parentConstraint of the thigh ik to the thigh joint
        nd.parentConstraint(objA = ctl[-1].transform, 
                            objB = self.joints_ik[0],
                            suffix = 'PAC', 
                            maintainOffset = False)             
    #END def __setup_ik_controls()

    def __setup_ik_pole_vector(self):
        #--- this method setups the ik pole vector controls
        ap = api.API()
        nd = node.Node()
        #--- get the poleVector position and rotation
        pole_vector = ap.get_pole_vector(jointChain = self.joints_ik)
        pos = pole_vector[0]
        rot = pole_vector[1]
        #--- create the control based on the poleVector position
        self.pole_vector_ctl = control.Control(side = self.side,
                                               name = self.mod + 'KneeIK',
                                               suffix = 'CTL',
                                               size = self.size - 0.5,
                                               shape = 12,
                                               color = self.color,
                                               position = [pos[0], 
                                                           pos[1], 
                                                           pos[2] + 10],
                                               rotation = rot,
                                               orientation = [0,0,0],
                                               parent = self.side_ctl_grp)
        #--- create poleVector constraint
        nd.poleVectorConstraint(objA = self.pole_vector_ctl.transform, 
                                objB = self.ik_handle[0],
                                suffix = 'PVC')       
    #END def __Setup_ik_pole_vector()

    def __setup_ikfk(self):
        #--- this method creates an ikfk blend or ikfk spaceSwitch
        if self.ikfk:
            #--- create a left ikfk switch control
            self.ikfk_blend = control.Control(side = self.side,
                                             name = self.mod + 'IKFK',
                                             suffix = 'CTL',
                                             size = self.size - 0.5,
                                             shape = 9,
                                             color = self.color,
                                             position = [self.joint_position[-1][0] + 1,
                                                         self.joint_position[-1][1] - 1,
                                                         self.joint_position[-1][2]],
                                             rotation = [0,0,0],
                                             orientation = [0,0,0])
            cmds.parent(self.ikfk_blend.group, self.joints[-1])

            if self.ikfk == 'Blend':
                self.__setup_blend()
    #END def __setup_ikfk()

    def __setup_blend(self):
        #--- this method creates a blending setup between ik and fk
        attr = attribute.Attribute()
        nd = node.Node()
        #--- add an fkik blend attribute
        attr.addAttr(node = self.ikfk_blend.transform,
                     attrName = 'fkIk',
                     attrType = 'float',
                     min = 0,
                     max = 10,
                     default = 10)
        #--- create proper utility nodes to setup ikfk Blend
        mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkFkBlend', 
                                operation = 2,
                                input2X = 10,
                                lockAttr = 'input2X')
        rev = nd.reverse(name = self.side + '_' + self.mod + 'IkFkBlend')
        #--- connect nodes properly
        attr.connectAttr(node = [self.ikfk_blend.transform, mlt], 
                         attribute = ['fkIk', 'input1X'])
        attr.connectAttr(node = [mlt, rev], 
                         attribute = ['outputX', 'inputX'])
        #--- connect the nodes with the parentConstraint weights
        for pac in range(len(self.pac)):
            attr.connectAttr(node = [rev, self.pac[pac]], 
                             attribute = ['outputX', 
                                          self.joints_fk[pac] + 'W0'])
            attr.connectAttr(node = [mlt, self.pac[pac]], 
                             attribute = ['outputX', 
                                          self.joints_ik[pac] + 'W1'])
            #--- set the interpType of the parentConstraint to shortest(2)
            attr.setAttr(node = self.pac[pac], 
                         attribute = 'interpType', 
                         value = 2)
        #--- connect the nodes with the controls' visibility
        #--- ik controls
        attr.connectAttr(node = [mlt, self.controls_ik[0].transform], 
                         attribute = ['outputX', 'visibility'])
        attr.connectAttr(node = [mlt, self.controls_ik[-1].transform], 
                         attribute = ['outputX', 'visibility'])
        attr.connectAttr(node = [mlt, self.pole_vector_ctl.transform], 
                         attribute = ['outputX', 'visibility'])   
        #--- fk controls
        for fk in range(len(self.controls_fk)):
            attr.connectAttr(node = [rev, self.controls_fk[fk].transform], 
                             attribute = ['outputX', 'visibility'])            
    #END def __setup_blend()

    def __setup_ik_joint_stretch(self):
        #--- this method creates an ik squash and stretch setup on ik joints
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the ik joint stretch setup
        for jnt in self.joints_ik[:-1]:
            #--- add stretch attribute
            attr.addAttr(node = jnt, 
                         attrName = 'stretch', 
                         attrType = 'float', 
                         min = 0.001, 
                         max = 100, 
                         default = 1)
            #--- create multiplyDivide nodes
            mlt_div = nd.multiplyDivide(name = jnt.split('_JNT')[0] + 'StretchDiv', 
                                        operation = 2, 
                                        input1X = 1,
                                        lockAttr = 'input1X')
            mlt_pow = nd.multiplyDivide(name = jnt.split('_JNT')[0] + 'StretchPow', 
                                        operation = 3, 
                                        input2X = 0.5,
                                        lockAttr = 'input2X')
            #---  connect the utility nodes with the ik joints
            attr.connectAttr(node = [jnt, mlt_div], 
                             attribute = ['stretch', 'input2X'])
            attr.connectAttr(node = [mlt_div, mlt_pow], 
                             attribute = ['outputX', 'input1X'])
            attr.connectAttr(node = [jnt, jnt],
                             attribute = ['stretch', 'sx'])
            for axis in 'zy':
                attr.connectAttr(node = [mlt_pow, jnt], 
                                 attribute = ['outputX', 's' + str(axis)])
    #END def __setup_ik_joint_stretch()

    def __setup_ik_squash_stretch(self):
        #--- this method creates an ik squash and stretch setup on the ik system
        attr = attribute.Attribute()
        nd = node.Node()
        #--- get the ik controls
        ctl = self.controls_ik
        #--- get the full distance length
        distance = measure.Measure(objects = self.joints_ik).distance
        #--- add stretchy attributes to the ikfk controls
        attr.addAttr(node = self.ikfk_blend.transform, 
                     attrName = 'ikStretch', 
                     attrType = 'float', 
                     min = 0, 
                     max = 1, 
                     default = 0)
        #--- create the utility nodes
        dib = nd.distanceBetween(name = self.side + '_' + self.mod + 'IkStretch', 
                                 suffix = 'DIB',
                                 point1 = ctl[-1].transform,
                                 point2 = ctl[0].transform,
                                 inMatrix1 = ctl[-1].transform,
                                 inMatrix2 = ctl[0].transform)
        mlt_scale = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkStretchGlobalScale',
                                      input2X = distance,
                                      lockAttr = 'input2X')
        mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'IkStretch', 
                                suffix = 'MLT', 
                                operation = 2)
        cnd = nd.condition(name = self.side + '_' + self.mod + 'IkStretch', 
                           suffix = 'CND', 
                           secondTerm = 1, 
                           operation = 3, 
                           lockAttr = 'secondTerm')
        blc = nd.blendColors(name = self.side + '_' + self.mod + 'IkStretch', 
                             suffix = 'BLC', 
                             color2R = 1, 
                             lockAttr = 'color2R')
        #--- connect the nodes properly
        attr.connectAttr(node = [dib, mlt], 
                         attribute = ['distance', 'input1X'])
        attr.connectAttr(node = [self.main_ctl, mlt_scale], 
                         attribute = ['scaleY', 'input1X'])
        attr.connectAttr(node = [mlt_scale, mlt], 
                         attribute = ['outputX', 'input2X'])
        attr.connectAttr(node = [mlt, cnd], 
                         attribute = ['outputX', 'firstTerm'])
        attr.connectAttr(node = [mlt, cnd], 
                         attribute = ['outputX', 'colorIfTrueR'])
        attr.connectAttr(node = [cnd, blc], 
                         attribute = ['outColorR', 'color1R'])
        attr.connectAttr(node = [self.ikfk_blend.transform, blc], 
                         attribute = ['ikStretch', 'blender'])
        #--- connect the utility node to the joints
        for jnt in self.joints_ik[:-1]:
            attr.connectAttr(node = [blc, jnt], attribute = ['outputR', 'stretch'])
    #END def __setup_ik_squash_stretch()

    def __setup_ik_bend(self):
        #--- this method setups the bendy ik functionality by using flexiplanes
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create bend control
        self.bend_ctl = control.Control(side = self.side, 
                                        name = self.mod + 'Bend', 
                                        suffix = 'CTL', 
                                        size = self.size - 0.25, 
                                        shape = 10, 
                                        color = self.color, 
                                        position = [0,0,0], 
                                        rotation = [0,0,0],
                                        orientation = [0,90,90], 
                                        parent = self.joints_ik[1])
        cmds.parent(self.bend_ctl.group, self.side_ctl_grp)
        #--- parentConstraint the bend control to the elbow joint
        nd.parentConstraint(objA = self.joints[1], 
                            objB = self.bend_ctl.group, 
                            suffix = 'PCN', 
                            maintainOffset = False,
                            lock = True)        
        #--- create the first flexiplane for the femur bone
        self.upper_leg_flp = flexiplane.FlexiPlane(character = self.character, 
                                                   mod = self.mod, 
                                                   side = self.side, 
                                                   name = 'upperLeg', 
                                                   color = self.color, 
                                                   size = self.size - 0.5,
                                                   length = 5,
                                                   constraintTo = [self.joints[0],
                                                                   self.bend_ctl.transform],
                                                   constraintType = 'point', 
                                                   follow = True,
                                                   parent = self.side_extra_grp,
                                                   inheritsTransform = False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        attr.connectAttr(node = [self.bend_ctl.transform,
                                 self.upper_leg_flp.control_up.transform],
                         attribute = ['rotateX', 'rotateX'])
        #--- parentConstraint the main control to the start joint of the femur
        nd.parentConstraint(objA = self.joints[0], 
                            objB = self.upper_leg_flp.control_main.transform, 
                            suffix = 'PAC', 
                            maintainOffset = True,
                            lock = True)
        #--- create the second flexiplane for the tibia bones
        self.lower_leg_flp = flexiplane.FlexiPlane(character = self.character, 
                                                   mod = self.mod, 
                                                   side = self.side, 
                                                   name = 'lowerLeg', 
                                                   color = self.color, 
                                                   size = self.size - 0.5,
                                                   length = 5,
                                                   constraintTo = [self.bend_ctl.transform,
                                                                   self.joints[-1]],
                                                   constraintType = 'point', 
                                                   follow = True,
                                                   parent = self.side_extra_grp,
                                                   inheritsTransform = False)
        #--- connect the rotateX attr of the flexiplane with the bend control
        attr.connectAttr(node = [self.bend_ctl.transform,
                                 self.lower_leg_flp.control_down.transform],
                         attribute = ['rotateX', 'rotateX'])        
        #--- parentConstraint the main control to the start joint of the tibia
        nd.parentConstraint(objA = self.joints[1], 
                            objB = self.lower_leg_flp.control_main.transform, 
                            suffix = 'PAC', 
                            maintainOffset = True,
                            lock = True)
        #--- connect the globalScale attr of the flexiplane with the main ctl one
        #--- upper flexiPlane
        attr.connectAttr(node = [self.main_ctl,
                                 self.upper_leg_flp.control_main.transform],
                         attribute = ['globalScale', 'globalScale'])
        #--- lower flexiPlane
        attr.connectAttr(node = [self.main_ctl,
                                 self.lower_leg_flp.control_main.transform],
                         attribute = ['globalScale', 'globalScale'])
    #END def __setup_ik_bend()

    def __auto_hip_setup(self):
        #--- this method setups the autoHip
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- create hip puppet
        if self.guideObj.hipEnable:
            hip_puppet = hip.BipedHipPuppet(character = self.character, 
                                            guideObj = self.guideObj.hip,
                                            autoHip = True,
                                            softHip = self.softHip)
            self.hip = hip_puppet
            if self.fk:
                #--- unlock necessary attributes
                attr.lockAttr(node = self.controls_fk[0].group, 
                              attribute = ['t', 'r', 's'], 
                              lock = False, 
                              show = True)
                #--- parent the leg fk to the hip control
                cmds.parent(self.controls_fk[0].group, 
                            self.hip.control.transform)
            if self.ik:
                #--- unlock necessary attributes
                attr.lockAttr(node = self.controls_ik[-1].group,
                              attribute = ['t', 'r', 's'], 
                              lock = False, 
                              show = True)
                #--- parent the leg ik to the hip control
                cmds.parent(self.controls_ik[-1].group, 
                            self.hip.control.transform)
            cmds.select(clear = True)

            #--- create the autoHip joint setup
            auto_hip_joints = jointchain.IkChain(side = self.side, 
                                                 name = [self.mod + 'AutoHipStart',
                                                         self.mod + 'AutoHipEnd'], 
                                                 suffix = 'JNT', 
                                                 position = [self.joint_position[0], 
                                                             self.joint_position[-1]], 
                                                 orientation = [[0.0, 0.0, 0.0,], 
                                                               [0.0, 0.0, 0.0]],
                                                 parentJoint = self.hip.side_extra_grp,
                                                 parentIk = self.hip.side_extra_grp,
                                                 mirror = False)            

            #--- AUTOHIP SETUP
            self.joints_ah = auto_hip_joints.ik_joint_names
            self.ik_handle_ah = auto_hip_joints.ik_handle_names

            #--- create the poleVector setup
            #--- create a locator
            pole_vector = nd.locator(name = (self.side + '_' + 
                                             self.mod + 'AutoHipPoleVector'), 
                                     suffix = 'LOC', 
                                     parent = self.joints_ah[-1])
            cmds.parent(pole_vector, self.hip.side_extra_grp)
            #--- create poleVectorConstraint
            nd.poleVectorConstraint(objA = pole_vector, 
                                    objB = self.ik_handle_ah[0], 
                                    suffix = 'PVC')
            #--- pointConstraint the locator to the ik control
            nd.pointConstraint(objA = self.controls_ik[0].transform, 
                               objB = pole_vector, 
                               suffix = 'PCN', 
                               maintainOffset = False, 
                               lock = True)
            #--- pointConstraint the ikHandle to the ik control
            nd.pointConstraint(objA = self.controls_ik[0].transform, 
                               objB = self.ik_handle_ah[0], 
                               suffix = 'PCN', 
                               maintainOffset = False, 
                               lock = True)

            #--- SETUP rotation automation of the hip
            #--- create a rotation group above the hip control
            rot_grp = cmds.group(self.hip.control.transform, 
                                 name = (self.hip.control.transform.split('_CTL')[0] 
                                         + '_SDK'))
            #--- set the group pivot to the controls pivot
            cmds.xform(rot_grp, 
                       pivots = self.hip.joint_position[0], 
                       worldSpace = True)

            #--- limit rotations of this SDK group
            cmds.transformLimits(rot_grp, 
                                 enableRotationX = (1,1), 
                                 enableRotationY = (1,0), 
                                 enableRotationZ = (1,0), 
                                 rotationX = (-20,20),
                                 rotationY = (-50,45),
                                 rotationZ = (0,45))                                 
            #--- create nodes for the automation setup
            mlt = nd.multiplyDivide(name = self.side + '_' + self.mod + 'AutoHipRot',
                                    input2X = 0.9,
                                    input2Y = 0.9,
                                    input2Z = 0.5)
            blc = nd.blendColors(name = self.side + '_' + self.mod + 'AutoHipEnable',
                                 color2R = 0,
                                 color2G = 0,
                                 color2B = 0,
                                 lockAttr = ['color2R',
                                             'color2G',
                                             'color2B'])
            mlt_ikfk = nd.multiplyDivide(name = (self.side + '_' + self.mod + 
                                                 'AutoHipIkFk'),
                                         input1X = 0.1,
                                         lockAttr = 'input1X')
            blc_ikfk = nd.blendColors(name = (self.side + '_' + self.mod + 
                                              'AutoHipIkFk'),
                                      color2R = 0,
                                      color2G = 0,
                                      color2B = 0,
                                      lockAttr = ['color2R',
                                                  'color2G',
                                                  'color2B'])
            #--- connect attributes for the automation
            attr.connectAttr(node = [self.joints_ah[0], mlt], 
                             attribute = ['rotate', 'input1'])
            attr.connectAttr(node = [mlt, blc], 
                             attribute = ['output', 'color1'])
            attr.connectAttr(node = [blc, rot_grp], 
                             attribute = ['output', 'rotate'])
            #--- connect the hip controls attributes
            attr.connectAttr(node = [self.ikfk_blend.transform, mlt_ikfk], 
                             attribute = ['fkIk', 'input2X'])
            attr.connectAttr(node = [mlt_ikfk, blc_ikfk], 
                             attribute = ['outputX', 'blender'])
            attr.connectAttr(node = [self.hip.control.transform, blc_ikfk], 
                             attribute = ['autoHip', 'color1R'])
            attr.connectAttr(node = [blc_ikfk, blc], 
                             attribute = ['outputR', 'blender'])
            self.mlt = mlt
            self.sdk = rot_grp           

            #--- SOFT HIP SETUP
            if self.softHip:
                self.__soft_hip_setup()
    #END def __auto_hip_setup()

    def __soft_hip_setup(self):
        #--- this method creates and setups the softHip
        attr = attribute.Attribute()
        nd = node.Node()
        #--- connect the softHip joints to the autoHip nodes system

        cmds.disconnectAttr(self.joints_ah[0] + '.rotateX', 
                            self.mlt + '.input1X')
        attr.connectAttr(node = [self.hip.soft_ry_jnt.ik_joint_names[0],
                                 self.mlt], 
                         attribute = ['rotateY', 'input1Y'])
        attr.connectAttr(node = [self.hip.soft_rz_jnt.ik_joint_names[0],
                                 self.mlt], 
                         attribute = ['rotateZ', 'input1Z'])
        #--- constraint the ik control with the translateY and Z locators
        nd.pointConstraint(objA = self.controls_ik[0].transform, 
                           objB = self.hip.ty_loc,
                           suffix = 'PCN')
        nd.pointConstraint(objA = self.controls_ik[0].transform, 
                           objB = self.hip.tz_loc,
                           suffix = 'PCN')
        #--- connect the hip softness attr with the tx of the locators
        attr.connectAttr(node = [self.hip.control.transform,
                                 self.hip.tyIk_loc], 
                         attribute = ['softness', 'tx'])
        attr.connectAttr(node = [self.hip.control.transform,
                                 self.hip.tzIk_loc], 
                         attribute = ['softness', 'tx'])
        #--- relimit rotations of the hip SDK group
        cmds.transformLimits(self.sdk, 
                             enableRotationX = (1,1), 
                             enableRotationY = (0,0), 
                             enableRotationZ = (0,0), 
                             rotationX = (0,0))
        #--- set the multiplyDivide input2 values of the softHip to 1
        attr.setAttr(node = self.mlt, 
                     attribute = ['input2'],
                     value = 1, 
                     lock = True)    
    #END def __soft_hip_setup()

    def __hook_mod_setup(self):
        #--- this method setups the hooks for this module
        attr = attribute.Attribute()
        nd = node.Node()
        #--- unlock necessary groups
        attr.lockAttr(node = self.hip.control.group, 
                      attribute = ['t', 'r'], 
                      lock = False, 
                      show = True)
        #--- parentConstraint the hip control groups to the hip control
        nd.parentConstraint(objA=self.puppetObj.hip_control.transform, 
                            objB=self.hip.control.group , 
                            suffix = 'PAC', 
                            maintainOffset = True, 
                            lock = True)
    #END def __hook_mod_setup()

    def __cleanup(self):
        #--- this is the cleanup method
        attr = attribute.Attribute()
        #--- hide the extranodes group
        #--- leg
        attr.setAttr(node = [self.side_extra_grp,
                             self.joints_fk[0],
                             self.joints_ik[0]],
                     attribute = 'v',
                     value = 0)
        #--- hip
        if self.guideObj.hipEnable:
            attr.setAttr(node = self.hip.side_extra_grp,
                         attribute = 'v', 
                         value = 0)            
    #END def __cleanup()

    def __create_puppet(self):
        #--- this is the main create method
        #--- get the bind, fk and ik joints
        self.__get_ikfk_joints()       
        #--- setup the ik, fk, bind joints
        self.__setup_joints()
        #--- add hooks
        self.__add_hooks()
        if self.fk:
            #--- create fk controls
            self.__create_fk_controls()
            #--- setup fk controls
            self.__setup_fk_controls()
        if self.ik:
            #--- create ik controls
            self.__create_ik_controls()
            #--- setup ik handles
            self.__setup_ik_handles()
            #--- setup ik controls
            self.__setup_ik_controls()
            #--- setup ik pole vectors
            self.__setup_ik_pole_vector()
        if self.ik and self.fk:
            #--- setup the ikfk blend
            self.__setup_ikfk()
        if self.ik:
            if self.ikStretch:
                #--- setup ik squash and stretch
                self.__setup_ik_joint_stretch()
                self.__setup_ik_squash_stretch()
            if self.ikBend:
                #--- setup bendy ik system
                self.__setup_ik_bend()
        if self.autoHip:
            #--- create the autoHip
            self.__auto_hip_setup()
        #--- hook setup
        self.__hook_mod_setup()
        #--- cleanup the mod
        self.__cleanup()
    #END def __create_puppet()
#END class BipedLegPuppet()


class QuadrupedLegGuide(mod.MasterMod):
    """
    This class creates a quadruped leg guide system based on the specification 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = None,
                  mod = 'leg',
                  side = 'L',
                  name = ['femur', 'tibia', 'metatarsus', 'ankle'],
                  size = 1,
                  shape = 2, 
                  color = 6, 
                  position = [[3, 16.5, -7],
                              [3, 12, -7],
                              [3, 8, -9],
                              [3, 2, -8]],
                  hipEnable = True,
                  upVectorOffset = [6,0,0],
                  aimVector = [0,1,0],
                  upVector = [1,0,0],
                  flip = True):
        ########################################################################
        #superclass inheritance initialisation
        super(QuadrupedLegGuide, self).__init__()

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
                          hipEnable = hipEnable,
                          upVectorOffset = upVectorOffset, 
                          aimVector = aimVector,
                          upVector = upVector,
                          flip = flip)
    #END def __init__()

    def __leg_setup(self,
                     character = None,
                     mod = None,
                     side = None,
                     name = None,
                     size = 1,
                     shape = 0, 
                     color = 0, 
                     position = [0,0,0],
                     hipEnable = True,
                     upVectorOffset = [0,6,0],
                     aimVector = [1,0,0],
                     upVector = [0,1,0],
                     flip = True):
        #--- this method is a mod specific setup
        #--- unlock the proper groups to work with them
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_grp, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)
        #--- pointConstraint the kneeGuide to the other ones
        nd = node.Node()
        nd.pointConstraint(objA = [self.gd.g_ctl[0], self.gd.g_ctl[2]], 
                           objB = self.gd.g_grp[1],
                           name = side + '_' + mod + name[1].capitalize())
        #--- parent the controls to the thigh ctl
        cmds.parent(self.gd.g_grp[1:-1], self.gd.g_ctl[0])
        cmds.parent(self.gd.g_grp[-1], self.gd.g_ctl[-2])
        #--- create the message connection setup
        self.__connect_message()        

        #--- create hipEnable setup
        if hipEnable:
            hipEnable_pos = [position[0][0] -2, 
                       position[0][1] +2,
                       position[0][2] +1]
            self.__leg_hipEnable_setup(character = character,
                                 upVectorOffset = upVectorOffset,
                                 aimVector = aimVector,
                                 upVector = upVector,
                                 flip = flip)
    #END def __leg_setup()        

    def __leg_hipEnable_setup(self,
                          character = None,
                          upVectorOffset = [6,0,0],
                          aimVector = [1,0,0],
                          upVector = [0,1,0],                          
                          flip = True):
        #--- this method calls the hipEnable mod
        self.hipEnable = hipEnable.QuadrupedHipGuide(character = character, 
                                         upVectorOffset = upVectorOffset,
                                         aimVector = aimVector,
                                         upVector = upVector)
        #--- connect the mouth guides properly regarding the flip boolean
        self.__connect_guides(mod = self.hipEnable.gd.mod, 
                              side = self.hipEnable.gd.side,
                              obj = [self.hipEnable.gd.g_jnt[0], 
                                     self.gd.g_jnt[0]], 
                              position = [self.hipEnable.gd.position, 
                                          self.gd.position[0]])
        if flip:
            self.__connect_guides(mod = self.hipEnable.gd.mod, 
                                  side = self.hipEnable.gd.flip_side,
                                  obj = [self.hipEnable.gd.flip_ctl[0], 
                                         self.gd.flip_ctl[0]], 
                                  position = [self.hipEnable.gd.flip_pos[0],
                                              self.gd.flip_pos[0]])
        #--- unlock the proper groups to work with them
        attr = attribute.Attribute()
        attr.lockAttr(node = self.hipEnable.gd.g_jnt_off, 
                      attribute = ['t', 'r', 's'], 
                      lock = False)            
        #--- create the proper joint aim constraint
        nd = node.Node()
        nd.aimConstraint(target = self.gd.g_jnt[0], 
                         source = self.hipEnable.gd.g_jnt_off[0],
                         aimVector = aimVector, 
                         upVector = upVector, 
                         worldUpObject = self.hipEnable.gd.g_loc[0], 
                         worldUpType = 'object')
        #--- hook the leg guide to the hipEnable
        hook.Hook(mod = self.hip, 
                  hookParent = self.hip.gd.g_ctl[0], 
                  hookChild = self.gd.g_grp[0], 
                  hookType = 'parentConstraint')
    #END def __leg_hipEnable_setup()

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
        shape = cmds.listRelatives(crv, allDescendents = 1)[0]

        #--- connect the cvs to the controls by matrix
        attr = attribute.Attribute()
        nd   = node.Node()
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, shape], 
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

    def __leg_cleanup(self):
        #--- this method is a mod specific cleanup
        #--- hide unnecessary attributes from the guide controls
        attr = attribute.Attribute()
        attr.lockAttr(node = self.gd.g_ctl[1:], 
                      attribute = ['tx', 'r', 's', 'v'], 
                      lock = True, show = False)
        attr.lockAttr(node = self.gd.g_ctl[0], 
                      attribute = ['s', 'v'], 
                      lock = True, show = False)
        cmds.select(clear = True)
    #END def leg_cleanup()

    def __main_setup(self,
                      character = None,
                      mod = None,
                      side = None,
                      name = None,
                      size = 1,
                      shape = 0, 
                      color = 0, 
                      position = [0,0,0],
                      hipEnable = True,
                      upVectorOffset = [0,6,0],
                      aimVector = [1,0,0],
                      upVector = [0,1,0],
                      flip = True):
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
                    flip = flip)
        #--- mod specific setup
        self.__leg_setup(character = character,
                         mod = mod, 
                         side = side,
                         name = name, 
                         size = size, 
                         shape = shape, 
                         color = color,
                         position = position,
                         hipEnable = hipEnable,
                         upVectorOffset = upVectorOffset, 
                         aimVector = aimVector,
                         upVector = upVector,
                         flip = flip)
        #--- mod specific cleanup
        self.__leg_cleanup()
    #END def __create()
#END class QuadrupedLegGuide()