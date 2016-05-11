'''
Created on 08.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This class creates a flexiPlane
'''

from maya import cmds
from fundamentals import attribute, curve, deformer, joint, node
from functions import control
from decimal import *
reload(attribute)
reload(control)
reload(deformer)
reload(curve)
reload(joint)
reload(node)


class FlexiPlane(object):
    '''
    This class creates a flexiPlane which is useful for 
    stretchy and bendy functionalities in the rig.

    @DONE: globalScale fix on main control
    @DONE: translation, rotation feature on muscle control eventually
    @DONE: cleanup of all the nodes = ihi flag
    @DONE: general cleanup of the flexiPlane system
    @DONE: position and rotation flags
    @DONE: constraintTo flag
    @DONE: constraintType flag
    @DONE: follow flag
    @DONE: size flag
    @DONE: parent flag
    @DONE: inheritsTransform flag
    '''

    def __init__(self,
                  character = None,
                  mod = None,
                  side = None,
                  name = None,
                  color = 0,
                  size = 1,
                  length = 5,
                  position = [0,0,0],
                  rotation = [0,0,0],
                  constraintTo = [None, None],
                  constraintType = None,
                  follow = False,
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  muscleSystem = False,
                  muscles = 1,
                  mesh = None,
                  parent = None,
                  inheritsTransform = True):
        ########################################################################
        #vars
        self.name           = None
        self.main           = None
        self.global_move    = None
        self.follicle_grp   = None
        self.extra_nodes    = None
        self.cluster_grp    = None

        self.surface        = None

        self.follicle       = []
        self.volume_up      = []
        self.volume_down    = []
        self.jnt_grp        = []
        self.jnt            = []
        self.locator        = []

        self.control_up     = []
        self.control_down   = []
        self.control_mid    = []
        self.control_main   = []
        self.jnt_ctl        = []
        self.clstr_mid_grp  = []

        self.bsp_surface    = None
        self.curve          = None
        self.curve_info     = None
        self.twist          = []
        self.twist_handle   = None

        self.muscle_surface = None
        self.mus_ctl        = []

        #methods
        self.__create(character = character,
                      mod = mod,
                      side = side,
                      name = name,
                      color = color,
                      size = size,
                      length = length,
                      position = position,
                      rotation = rotation,
                      constraintTo = constraintTo,
                      constraintType = constraintType,
                      follow = follow,
                      aimVector = aimVector,
                      upVector = upVector,
                      muscleSystem = muscleSystem,
                      muscles = muscles,
                      mesh = mesh,
                      parent = parent,
                      inheritsTransform = inheritsTransform)
    #END def __init__()

    def __create_group_setup(self,
                                mod = None,
                                side = None,
                                name = None,
                                parent = None):
        #--- this method creates a proper group structure
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the hierarchical group structure
        self.name = side + '_' + mod + name[0].upper() + name[1:]
        self.main = nd.transform(name = self.name, 
                                 suffix = 'FLP',
                                 parent = parent)
        self.global_move = nd.transform(name = self.name + '_globalMove',
                                        parent = self.main)
        self.follicle_grp = nd.transform(name = self.name + '_follicle',
                                         suffix = 'GRP',
                                         parent = self.main)
        self.extra_nodes = nd.transform(name = self.name + '_extraNodes',
                                        parent = self.main)
        self.cluster_grp = nd.transform(name = self.name +'_clstr',
                                        suffix = 'GRP',
                                        parent = self.extra_nodes)
    #END def __create_group_setup()

    def __create_plane(self,
                         length = 5):
        #--- this method creates a nurbsPlane based on flag specification
        surface = cmds.nurbsPlane(degree = 3,
                                  width = 10,
                                  lengthRatio = 0.2,
                                  patchesU = length,
                                  patchesV = 1,
                                  axis = (0,1,0),
                                  name = self.name +'_surface')
        self.surface = surface[0]
        #--- parent the surface under the global movement group
        cmds.parent(self.surface, self.global_move)
    #END def __create_plane()

    def __follicle_setup(self,
                           length = 5):
        #--- this method creates the proper follicle, joint and locator setup
        attr = attribute.Attribute()
        nd = node.Node()
        #--- get the cvs of the surface
        follicle_count = cmds.ls(self.surface + '.cv[*]', flatten = True)
        #--- the begin of the follicle loop setup
        for i in range(len(follicle_count[:length])):
            if i:
                #--- create a follicle
                follicle = nd.follicle(name = self.name + `i`, 
                                       suffix = 'FOL',
                                       parent = self.follicle_grp,
                                       show = False)
                self.follicle.append(follicle[0])
                #--- connect the follicle to the nurbsSurface
                attr.connectAttr(node = [self.surface, follicle[1]],
                                 attribute = ['local', 'inputSurface'])
                attr.connectAttr(node = [self.surface, follicle[1]], 
                                 attribute = ['worldMatrix[0]', 'inputWorldMatrix'])
                #--- connect the follicle scale attributes to the global movement
                nd.scaleConstraint(objA = self.global_move,
                                   objB = follicle[0],
                                   suffix = 'SCN',
                                   maintainOffset = True)
                #--- reposition the follicles in u and v
                #--- get the U position, V is by default 0.5
                x = (10 / float(length))
                p = str(i * x)
                p = p.split('.')
                p = p[0] + p[1]
                if not p == '00':
                    u = str('0.') + str(p)
                    attr.setAttr(node = follicle[1],
                                 attribute = 'parameterU', 
                                 value = float(u))
                    attr.setAttr(node = follicle[1],
                                 attribute = 'parameterV', 
                                 value = 0.5)

                    #--- create a joint with the volumeShift groups
                    #--- parent them under the follicle
                    vol_up = nd.transform(name = (self.name + `i` + 
                                                  '_VolumeShiftUp'),
                                          suffix = 'GRP', 
                                          parent = follicle[0])
                    vol_down = nd.transform(name = (self.name + `i` + 
                                                    '_VolumeShiftDown'),
                                            suffix = 'GRP',
                                            parent = vol_up)                    
                    jnt_grp = nd.transform(name = self.name + `i`,
                                           suffix = 'JNT_GRP',
                                           parent = vol_down)
                    jnt = joint.Joint(name = self.name + `i`,
                                      suffix = 'JNT',
                                      radius = 0.5).name
                    #--- set the correct jointOrientX axis
                    if i == len(follicle_count[:length]) - 1:
                        getRot = attr.getAttr(node = follicle[0], 
                                              attribute = 'rx')
                        getInv = getRot * -1
                        attr.setAttr(node = jnt, 
                                     attribute = 'jointOrientX', 
                                     value = getInv)
                    #--- store the joint/group and the volume groups in lists
                    self.volume_up.append(vol_up)
                    self.volume_down.append(vol_down)
                    self.jnt_grp.append(jnt_grp)
                    self.jnt.append(jnt)

                    #--- create a locator as the upVector of the joints
                    locator = nd.locator(name = self.name + 'UpVec' + `i`,
                                         suffix = 'LOC', 
                                         position = [0,0,6],
                                         rotation = [0,0,0],
                                         parent = follicle[0])
                    self.locator.append(locator)
    #END def __follicle_setup()

    def __aim_joints(self,
                      aimVector = [1,0,0],
                      upVector = [0,1,0]):
        #--- this method aims the joints
        attr = attribute.Attribute()
        nd = node.Node()
        for i in range(len(self.jnt_grp[:-1])):
            j = i + 1
            nd.aimConstraint(target = self.jnt_grp[j], 
                             source = self.jnt_grp[i],
                             name = self.name + `i`,
                             suffix = 'AIM',
                             aimVector = aimVector,
                             upVector = upVector,
                             worldUpType = 'object',
                             worldUpObject = self.locator[i])
            if j == len(self.jnt_grp[:-1]):
                #--- create a group on top of the last joint
                cmds.select(self.jnt[-1])
                last_grp = cmds.group(name = self.jnt[-1].split('_JNT')[0] 
                                      + 'Last_JNT_GRP')
                #--- set the rotation values of the last joint to zero
                attr.setAttr(node = self.jnt[-1], 
                             attribute = 'r', 
                             value = [0,0,0])
                #--- get the mirrored aimVector
                if aimVector[0]:
                    aimVector = [-1,0,0]
                elif aimVector[1]:
                    aimVector = [0,-1,0]
                elif aimVector[2]:
                    aimVector = [0,0,-1]
                nd.aimConstraint(target = self.jnt[-2], 
                                 source = last_grp,
                                 name = self.name + `i`,
                                 suffix = 'AIM',
                                 aimVector = aimVector,
                                 upVector = upVector,
                                 worldUpType = 'object',
                                 worldUpObject = self.locator[i])            
    #END def __aim_joints()

    def __create_controls(self, 
                            mod = None,
                            side = None,
                            name = None,
                            color = 0,
                            size = 1,
                            follow = False):
        #--- this method creates the flexiPlane controls
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- create main control
        self.control_main = control.Control(side = side, 
                                            name = (mod + name[0].upper() + 
                                                    name[1:] + 'Main'), 
                                            suffix = 'FPCTL', 
                                            size = size + 0.75, 
                                            shape = 5, 
                                            color = color, 
                                            orientation = [0,90,0],
                                            parent = self.main)
        #--- create up control
        self.control_up = control.Control(side = side, 
                                          name = (mod + name[0].upper() + 
                                                  name[1:] + 'Up'), 
                                          suffix = 'FPCTL', 
                                          size = size + 0.25, 
                                          shape = 1, 
                                          color = 6, 
                                          position = [5,0,0],
                                          parent = self.global_move)
        #--- create down control
        self.control_down = control.Control(side = side, 
                                            name = (mod + name[0].upper() + 
                                                    name[1:] + 'Down'), 
                                            suffix = 'FPCTL', 
                                            size = size + 0.25, 
                                            shape = 1, 
                                            color = 6, 
                                            position = [-5,0,0],
                                            parent = self.global_move)
        #--- create mid control
        self.control_mid = control.Control(side = side, 
                                           name = (mod + name[0].upper() + 
                                                   name[1:] + 'Mid'), 
                                           suffix = 'FPCTL', 
                                           size = size + 0.25, 
                                           shape = 2, 
                                           color = color, 
                                           parent = self.global_move)
        if follow:
            nd.pointConstraint(objA = [self.control_down.transform,
                                       self.control_up.transform], 
                               objB = self.control_mid.group, 
                               suffix = 'PCN', 
                               maintainOffset = False)

        #--- create individual joint controls, parented under the follicle
        for i in range(len(self.follicle)):
            j = i + 1
            #--- create main control
            jnt_ctl = control.Control(side = side, 
                                      name = (mod + name[0].upper() + 
                                              name[1:] + "FlexiJnt" + `j`), 
                                      suffix = 'FPCTL', 
                                      size = size/1.5, 
                                      shape = 1, 
                                      color = 13,
                                      rotation = [90,0,0], 
                                      parent = self.follicle[i])            
            attr.setAttr(node = jnt_ctl.transform, 
                         attribute = 't', 
                         value = 0, 
                         lock = True)
            self.jnt_ctl.append(jnt_ctl)         
    #END def __create_controls()

    def __add_control_attributes(self, 
                                    muscleSystem = False,
                                    muscles = 1):
        #--- this method adds attributes to the main control
        attr = attribute.Attribute()
        #--- globalScale
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'globalScale', 
                     attrType = 'float', 
                     min = 0, 
                     max = 10,
                     default = 1)
        #--- volumeControls
        attr.addAttr(node = self.control_main.transform, 
                     attrName= 'volumeControls', 
                     attrType = 'enum', 
                     enum = ['__________'],
                     keyable = False,
                     channelBox = True)
        #--- volume
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'volume', 
                     attrType = 'float', 
                     min = 0, 
                     max = 1,
                     default = 1)
        #--- volumeShift
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'volumeShift', 
                     attrType = 'float', 
                     min = -10,
                     max = 10, 
                     default = 0)
        #--- volumeDropoff
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'volumeDropoff', 
                     attrType = 'float', 
                     min = 0, 
                     max = 10,
                     default = 1)

        #--- controls for the muscle system
        if muscleSystem:
            #--- muscle system
            attr.addAttr(node = self.control_main.transform, 
                         attrName= 'muscleSystem', 
                         attrType = 'enum', 
                         enum = ['__________'],
                         keyable = False,
                         channelBox = True)
            for i in range(muscles):
                i = i + 1
                #--- muscle
                attr.addAttr(node = self.control_main.transform, 
                             attrName = 'muscle' + `i`, 
                             attrType = 'short', 
                             min = 0, 
                             max = 1,
                             default = 0,
                             channelBox = True)
                #--- muscle size
                attr.addAttr(node = self.control_main.transform, 
                             attrName = 'muscle' + `i` + 'Size', 
                             attrType = 'float', 
                             min = 0, 
                             max = 50,
                             default = 0)
                #--- muscle slide
                attr.addAttr(node = self.control_main.transform, 
                             attrName = 'muscle' + `i` + 'Slide', 
                             attrType = 'float', 
                             min = 0, 
                             max = 1,
                             default = 0)                
                #--- muscle maxDisplace
                attr.addAttr(node = self.control_main.transform, 
                             attrName = 'muscle' + `i` + 'MaxDisplace', 
                             attrType = 'float', 
                             min = 0, 
                             max = 50,
                             default = 0.5)                
                #--- muscle DropOff
                attr.addAttr(node = self.control_main.transform, 
                             attrName = 'muscle' + `i` + 'DropOff', 
                             attrType = 'float', 
                             min = 0.001, 
                             max = 50,
                             default = 1)

        #--- these are the general display options
        #--- display options
        attr.addAttr(node = self.control_main.transform, 
                     attrName= 'displayOptions', 
                     attrType = 'enum', 
                     enum = ['__________'],
                     keyable = False,
                     channelBox = True)        
        #--- showJoints
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'showJoints', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1,
                     default = 0,
                     channelBox = True)
        #--- showSurface
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'showSurface', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1,
                     default = 0,
                     channelBox = True)        
        #--- showUpVectors
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'showUpVectors', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1,
                     default = 0,
                     channelBox = True)
        #--- showBspSetup
        attr.addAttr(node = self.control_main.transform, 
                     attrName = 'showBspSetup', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1,
                     default = 0,
                     channelBox = True)       
    #END def __add_control_attributes()

    def __setup_controls(self):
        #--- this method setups the controls properly
        attr = attribute.Attribute()
        nd = node.Node()
        #--- lock and hide unnecessary attributes of the controls
        attr.lockAttr(node = [self.control_down.transform, 
                              self.control_up.transform,
                              self.control_mid.transform], 
                      attribute = ['s', 'v'], 
                      lock = True, 
                      show = False)
        attr.lockAll(node = [self.control_down.group, 
                             self.control_up.group,
                             self.control_mid.group])
        #--- pointConstraint the joint controls, 
        #--- connect the joints' jontOrient and jointGrp scale transforms
        for jnt in range(len(self.jnt_grp)):
            nd.pointConstraint(objA = self.jnt_ctl[jnt].transform, 
                               objB = self.jnt_grp[jnt], 
                               maintainOffset = False)
            attr.connectAttr(node = [self.jnt_ctl[jnt].transform, 
                                     self.jnt_grp[jnt]], 
                             attribute = ['s', 's'])
            #--- lock rotation and visibility attributes of the joint controls
            attr.lockAttr(node = self.jnt_ctl[jnt].transform, 
                          attribute = ['r', 'v'])
        #--- connect the globalScale of the main control with the scale one
        attr.connectAttr(node = [self.control_main.transform, 
                                 self.control_main.transform], 
                         attribute = ['globalScale', 'sx'])
        attr.connectAttr(node = [self.control_main.transform, 
                                 self.control_main.transform], 
                         attribute = ['globalScale', 'sy'])
        attr.connectAttr(node = [self.control_main.transform, 
                                 self.control_main.transform], 
                         attribute = ['globalScale', 'sz'])
        #--- parent the global movement group under the main control
        cmds.parent(self.global_move, self.control_main.transform)    
    #END def __setup_controls()

    def __create_blendshape_setup(self,
                                     character = None,
                                     mod = None,
                                     side = None,
                                     name = None,
                                     follow = False):
        #--- this method creates the blendShape setup
        attr = attribute.Attribute()
        dfm  = deformer.Deformer()
        nd   = node.Node()
        #--- duplicate the surface plane for the blendShape version
        self.bsp_surface = cmds.duplicate(self.surface, 
                                          name = self.surface + 'BlendShape')[0]
        #--- reposition the bsp_plane
        attr.setAttr(node = self.bsp_surface, 
                     attribute = 't', 
                     value = [0,0,-5])

        #--- create a curve and store it's arcLen info
        crv = curve.Curve(character = character, 
                          mod = mod, 
                          side = side, 
                          name = name + 'Wire', 
                          suffix = 'CRV', 
                          degree = 2, 
                          point = [[-5,0,-5], [0,0,-5], [5,0,-5]])
        self.curve = crv
        #--- get the cv of the curve
        cv_start = crv.cv[0]
        cv_mid   = crv.cv[1]
        cv_end   = crv.cv[2]

        #--- create a cluster on each cv
        clstr_start = dfm.cluster(mod = mod, 
                                  side = side, 
                                  name = name + 'Start', 
                                  suffix = 'CLS', 
                                  geometry = cv_start,
                                  parent = self.cluster_grp)
        clstr_mid = dfm.cluster(mod = mod, 
                                side = side, 
                                name = name + 'Mid', 
                                suffix = 'CLS', 
                                geometry = cv_mid,
                                parent = self.cluster_grp)
        clstr_end = dfm.cluster(mod = mod, 
                                side = side, 
                                name = name + 'End', 
                                suffix = 'CLS', 
                                geometry = cv_end,
                                parent = self.cluster_grp)

        self.clstr_mid_grp = clstr_mid[0].split('CLS')[0] + 'GRP'
        if follow:
            nd.pointConstraint(objA = [clstr_start[0],
                                       clstr_end[0]], 
                               objB = self.clstr_mid_grp, 
                               suffix = 'PCN', 
                               maintainOffset = False)

        #--- create a wire deformer on the curve affecting the blendShape surface
        wire = dfm.wire(mod = mod,
                        side = side, 
                        name = name,
                        suffix = 'DEF',
                        wire = crv.transform,
                        geometry = self.bsp_surface,
                        dropoffDistance = 20,
                        parent = self.extra_nodes)
        #--- create a twist deformer on the blendShape surface, rename them
        twist = dfm.twist(mod = mod, 
                          side = side, 
                          name = name, 
                          suffix = 'DEF', 
                          geometry = self.bsp_surface, 
                          rotation = [0,0,90],  
                          parent = self.extra_nodes)
        #--- reorder the input order properly
        cmds.reorderDeformers(wire[0], twist[0], self.bsp_surface)

        #--- create the blendShape
        bsp = dfm.blendShape(mod = mod, 
                             side = side, 
                             name = name, 
                             suffix = 'BSP', 
                             shapes = self.bsp_surface, 
                             target = self.surface, 
                             shapeAttr = self.bsp_surface,
                             shapeValue = 1,
                             lockAttr = self.bsp_surface)

        #--- do the proper control, cluster and deformer connections
        attr.connectAttr(node = [self.control_down.transform, 
                                 clstr_start[0]], 
                         attribute = ['t', 't'])
        attr.connectAttr(node = [self.control_up.transform, 
                                 clstr_end[0]],
                         attribute = ['t', 't'])
        attr.connectAttr(node = [self.control_mid.transform, 
                                 clstr_mid[0]],
                         attribute = ['t', 't'])
        attr.connectAttr(node = [self.control_down.transform, 
                                 twist[-1]],
                         attribute = ['rx', 'endAngle'])
        attr.connectAttr(node = [self.control_up.transform, 
                                 twist[-1]],
                         attribute = ['rx', 'startAngle'])

        #--- parent the nodes to the extra nodes group
        cmds.parent(self.bsp_surface, self.extra_nodes)
    #END def __create_blendshape_setup()

    def __squash_stretch(self):
        #--- this method creates the squash and stretch functionality
        attr = attribute.Attribute()
        nd = node.Node()

        #--- create the necessary multiplyDivide and condition nodes
        mlt_up = nd.multiplyDivide(name = self.name + 'SquashStretch',
                                   operation = 2,
                                   input2X = self.curve.arclen,
                                   lockAttr = 'input2X')
        mlt_down = nd.multiplyDivide(name = self.name + 'Divide',
                                     operation = 2,
                                     input1X = 1,
                                     lockAttr = 'input1X')
        cond = nd.condition(name = self.name +'SquashStretch',
                            firstTerm = 1,
                            secondTerm = 0,
                            operation = 1,
                            lockAttr = ['firstTerm', 'secondTerm'])        
        blc = nd.blendColors(name = self.name +'SquashStretch',
                             color2R = 1,
                             lockAttr = 'color2R')        

        #--- create the proper utility node connection setup
        attr.connectAttr(node = [self.curve.info, mlt_up],
                         attribute = ['arcLength', 'input1X'])
        attr.connectAttr(node = [mlt_up, mlt_down],
                         attribute = ['outputX', 'input2X'])
        attr.connectAttr(node = [mlt_down, cond], 
                         attribute = ['outputX', 'colorIfTrueR'])
        attr.connectAttr(node = [cond, blc], 
                         attribute = ['outColorR', 'color1R'])
        attr.connectAttr(node = [self.control_main.transform, blc],
                         attribute = ['volume', 'blender'])

        #--- connect the blender output with the scale of the joints
        for jnt in self.jnt:
            attr.connectAttr(node = [blc, jnt], attribute = ['outputR', 'sx'])
            attr.connectAttr(node = [blc, jnt], attribute = ['outputR', 'sy'])
            attr.connectAttr(node = [blc, jnt], attribute = ['outputR', 'sz'])
    #END def __squash_stretch()

    def __volume_system(self, 
                          length = 10):
        #--- this method creates a volume system by creating
        #--- for every joint a setup to shift the volume scale 
        #--- and also change the volume size
        attr = attribute.Attribute()
        nd = node.Node()
        #--- calculate the proper value for the dropOff and the shift amount
        #--- in regards of the specified length value
        step = Decimal(1) / Decimal(length)
        off  = Decimal(1) / Decimal(length)
        for i in range(len(self.jnt_grp)):
            up   = step
            down = Decimal(1) - Decimal(step) 
            #--- create nodes for the volume setup
            rmv_up = nd.remapValue(name = self.name + 'VolumeUpShift' + `i`,
                                   inputMin = 1,
                                   inputMax = 10,
                                   outputMin = 1,
                                   outputMax = float(up))
            rmv_down = nd.remapValue(name = self.name + 'VolumeDownShift' + `i`,
                                     inputMin = -10,
                                     inputMax = 0,
                                     outputMin = float(down),
                                     outputMax = 1)           
            mlt = nd.multiplyDivide(name = self.name + 'VolumeShift' + `i`)
            blc = nd.blendColors(name = self.name + 'VolumeShift' + `i`,
                                 color2R = 1,
                                 color2G = 1, 
                                 lockAttr = ['color2R', 'color2G'])

            #--- create node connections to create a volume shift and dropOff
            attr.connectAttr(node = [self.control_main.transform, 
                                     rmv_up],
                             attribute = ['volumeShift', 'inputValue'])
            attr.connectAttr(node = [self.control_main.transform, 
                                     rmv_down],
                             attribute = ['volumeShift', 'inputValue'])
            attr.connectAttr(node = [self.control_main.transform, 
                                     mlt],
                             attribute = ['volumeDropoff', 'input1X'])
            attr.connectAttr(node = [self.control_main.transform, 
                                     mlt], 
                             attribute = ['volumeDropoff', 'input1Y'])
            attr.connectAttr(node = [rmv_up, mlt],
                             attribute = ['outValue', 'input2X'])
            attr.connectAttr(node = [rmv_down, mlt],
                             attribute = ['outValue', 'input2Y'])
            attr.connectAttr(node = [mlt, blc],
                             attribute = ['outputX', 'color1R'])
            attr.connectAttr(node = [mlt, blc],
                             attribute = ['outputY', 'color1G'])
            attr.connectAttr(node = [self.control_main.transform, blc],
                             attribute = ['volume', 'blender'])
            #--- connect the blc output to the scale values of the joints volGrp
            for axis in 'xyz':
                scale = 's' + axis
                attr.connectAttr(node = [blc, self.volume_up[i]], 
                                 attribute = ['outputR', scale])
                attr.connectAttr(node = [blc, self.volume_down[i]], 
                                 attribute = ['outputG', scale])
            #--- this part is increasing the steps given by the length value
            step  = step + off
    #END def __volume_system()

    def __muscle_system(self,
                          mod = None,
                          side = None,
                          name = None,
                          color = 0,
                          size = 1,
                          length = 10,
                          rotation = [0,0,0],
                          muscles = 1,
                          mesh = None):
        #--- this method creates a simple muscle system based on sculptDeformers
        attr = attribute.Attribute()
        nd = node.Node()
        dfm = deformer.Deformer()
        #--- check if specified mesh is a mesh
        if mesh:
            if cmds.objExists(mesh):
                node_type = cmds.nodeType(cmds.listRelatives(mesh, allDescendents = True))
                if not node_type == 'mesh':
                    raise Exception('Specified mesh: ' + mesh + ' is not a mesh!')
            else:
                raise Exception('Specified mesh: ' + mesh + ' does not exist!')
            if not muscles < 1:
                #--- create a nurbsPlane
                self.muscle_surface = cmds.nurbsPlane(degree = 1, 
                                                      width = 10, 
                                                      lengthRatio = 0.2, 
                                                      patchesU = length, 
                                                      patchesV = 1, 
                                                      axis = (0,1,0), 
                                                      name = self.name + 
                                                      'Muscle_NRB')[0]
                #--- rotate the muscle surface
                attr.setAttr(node = self.muscle_surface, 
                             attribute = 'r', 
                             value = rotation)
                #--- parent the muscle surface under extra nodes
                cmds.parent(self.muscle_surface, self.extra_nodes)
                #--- create a follicle by the given amount of the muscles flag
                for i in range(muscles):
                    i = i + 1
                    if not i == 0:
                        #--- MUSCLE FOLLICLE SETUP JUST SCULPT DEFORMER
                        #--- create a follicle on the muscle plane
                        mus_follicle = nd.follicle(name = (self.name + 
                                                           'Muscle' + `i`), 
                                                   suffix = 'FOL', 
                                                   parameterU = 0,
                                                   parameterV = 0.5,
                                                   parent = self.follicle_grp,
                                                   show = False,
                                                   lockAttr= 'parameterV')
                        #--- connect the follicle with the muscle surface
                        attr.connectAttr(node = [self.muscle_surface, 
                                                 mus_follicle[1]],
                                         attribute = ['local', 
                                                      'inputSurface'])
                        attr.connectAttr(node = [self.muscle_surface, 
                                                 mus_follicle[1]],
                                         attribute = ['worldMatrix[0]', 
                                                      'inputWorldMatrix'])
                        #--- connect the main control and the muscle follicle
                        attr.connectAttr(node = [self.control_main.transform,
                                                 mus_follicle[1]],
                                         attribute = ['muscle' + `i` + 'Slide', 
                                                      'parameterU'])

                        #--- NORMAL FOLLICLE SETUP, MUSCLE CTL DRIVES SCULPT
                        #--- create a follicle on the normal surface
                        norm_follicle = nd.follicle(name = (self.name + 
                                                           'MuscleCtl' + `i`), 
                                                    suffix = 'FOL',
                                                    parameterU = 0,
                                                    parameterV = 0.5,
                                                    parent = self.follicle_grp,
                                                    show = False,
                                                    lockAttr= 'parameterV')
                        #--- connect the follicle with the normal surface
                        attr.connectAttr(node = [self.surface, 
                                                 norm_follicle[1]],
                                         attribute = ['local', 
                                                      'inputSurface'])
                        attr.connectAttr(node = [self.surface, 
                                                 norm_follicle[1]],
                                         attribute = ['worldMatrix[0]', 
                                                      'inputWorldMatrix'])
                        #--- connect the normal follicle scale attributes to the globalMovement group
                        nd.scaleConstraint(objA = self.global_move, 
                                           objB = norm_follicle[0], 
                                           maintainOffset = True)
                        #--- create connections between the main control and the muscle follicle
                        attr.connectAttr(node = [self.control_main.transform,
                                                 norm_follicle[1]],
                                         attribute = ['muscle' + `i` + 'Slide', 
                                                      'parameterU'])                            

                        #--- SCULPT DEFORMER
                        #--- create a control for the sculpt deformer and set it up
                        self.mus_ctl = control.Control(side = side, 
                                                       name = (mod + name[0].upper() + 
                                                               name[1:] + 'Muscle' + `i`), 
                                                       suffix = 'FPCTL', 
                                                       size = size + 0.1, 
                                                       shape = 2, 
                                                       color = color,
                                                       parent = norm_follicle[0])
                        #--- connect the size attr of the main control with the 
                        #--- scale of the muscle controls' group
                        for axis in 'xyz':
                            attr.connectAttr(node = [self.control_main.transform,
                                                     self.mus_ctl.group],
                                             attribute = ['muscle' + `i` + 
                                                          'Size', 's' + axis])
                        #--- connect the visiblity of the control with the 
                        #--- muscle attr of the main control
                        attr.connectAttr(node = [self.control_main.transform,
                                                 self.mus_ctl.transform],
                                         attribute = ['muscle' + `i`, 'v'])
                        #--- create a sculpt deformer and parent it under the muscle follicle
                        sculpt = dfm.sculpt(mod = mod, 
                                            side = side, 
                                            name = name + 'Muscle', 
                                            suffix = 'DEF', 
                                            geometry = mesh, 
                                            dropoffDistance = 0.14, 
                                            parent = mus_follicle[0])

                        #--- CONNECTION MUSCLE CONTROL WITH SCULPT DEFORMER
                        #--- connect the muscle size attr with the sculpt radius
                        attr.connectAttr(node = [self.control_main.transform,
                                                 sculpt[1]],
                                         attribute = ['muscle' + `i` + 'Size', 'radius'])                                
                        attr.lockAttr(node = sculpt[0], 
                                      attribute = ['s'],
                                      lock = False)
                        #--- connect the muscle controls scale with the sculpt one
                        attr.connectAttr(node = [self.mus_ctl.transform, sculpt[0]], 
                                         attribute = ['s', 's'])
                        #--- connect the muscle MaxDisplacement attr with the sculpt one
                        attr.connectAttr(node = [self.control_main.transform,
                                                 sculpt[2]],
                                         attribute = ['muscle' + `i` + 'MaxDisplace', 
                                                      'maximumDisplacement']) 
                        #--- connect the muscle dropOff attr with the sculpt one
                        attr.connectAttr(node = [self.control_main.transform,
                                                 sculpt[2]],
                                         attribute = ['muscle' + `i` + 'DropOff', 
                                                      'dropoffDistance'])  
                        #--- connect t and r of the sculpt with the muscle ctl
                        attr.connectAttr(node = [self.mus_ctl.transform,
                                                 sculpt[0]], 
                                         attribute = ['t', 't'])
                        attr.connectAttr(node = [self.mus_ctl.transform,
                                                 sculpt[0]], 
                                         attribute = ['r', 'r'])
                        #--- lock tx attribute of the muscle ctl
                        attr.lockAttr(node = self.mus_ctl.transform, 
                                      attribute = ['tx'])
                        #--- set the sculpts' transform values to default
                        attr.setAttr(node = sculpt[-1], 
                                     attribute = ['t', 'r'], 
                                     value = [0,0,0],
                                     lock = True)
                        cmds.setAttr(sculpt[0] + '.visibility', 0, lock = True)

                #--- COMPUTE PART
                #--- compute the steps to go to locate the cv's translateX position
                step = (10 / float(length))
                off  = (10 / float(length))
                cv_pos = [[-5.0, 0.0, 0.0]]
                for i in range(length):
                    res  = -5 + step
                    pos = [res, 0.0, 0.0]
                    cv_pos.append(pos)
                    step = +step + off
                #--- create the curves based on the computed position 
                #--- and create clusters for each cv
                crv = cmds.curve(degree = 2, point = cv_pos)
                mus_crv = cmds.rename(crv, self.name + 'Muscle_CRV')
                mus_cvs = cmds.ls(mus_crv + '.cv[*]', flatten = True)
                cmds.parent(mus_crv, self.extra_nodes)
                #--- create a matrix setup to connect the cvs with the control
                for i in range(len(mus_cvs)):
                    dcm = nd.decomposeMatrix(name = self.name + 'Muscle' + `i`)
                    if i == 0:
                        attr.connectAttr(node = [self.control_down.transform,
                                                 dcm],
                                         attribute = ['worldMatrix[0]', 
                                                      'inputMatrix'])
                        attr.connectAttr(node = [dcm, mus_crv],
                                         attribute = ['outputTranslate',
                                                      'controlPoints[0]'])
                    elif i == (len(mus_cvs)-1):
                        attr.connectAttr(node = [self.control_up.transform,
                                                 dcm],
                                         attribute = ['worldMatrix[0]', 
                                                      'inputMatrix'])
                        attr.connectAttr(node = [dcm, mus_crv],
                                         attribute = ['outputTranslate', 
                                                      'controlPoints[' + 
                                                      str(len(mus_cvs) - 1) + ']'])
                    else:
                        attr.connectAttr(node = [self.jnt_ctl[i - 1].transform,
                                                 dcm],
                                         attribute = ['worldMatrix[0]', 
                                                      'inputMatrix'])
                        attr.connectAttr(node = [dcm, mus_crv],
                                         attribute = ['outputTranslate', 
                                                      'controlPoints[' + `i` + ']'])
    #END def __muscle_system()

    def __reposition_flexiplane(self,
                                   position = [0,0,0],
                                   rotation = [0,0,0]):
        #--- this method repositions the flexiPlane
        attr = attribute.Attribute()
        attr.setAttr(node = self.control_main.transform, 
                     attribute = 't', 
                     value = position)
        attr.setAttr(node = self.control_main.transform, 
                     attribute = 'r', 
                     value = rotation)
    #END def __reposition_flexiplane()

    def __constraint_flexiplane(self,
                                   constraintTo = [None, None],
                                   constraintType = None):
        #--- this method constraints the main control by specified nodes
        attr = attribute.Attribute()
        nd = node.Node()
        #--- check given flags
        if not constraintTo == [None, None]:
            if cmds.objExists(constraintTo[0]):
                if cmds.objExists(constraintTo[1]):
                    #--- constraint the controls to proper positions
                    pac = nd.parentConstraint(objA = constraintTo, 
                                              objB = self.control_main.transform, 
                                              maintainOffset = False)
                    pcn_down = nd.pointConstraint(objA = constraintTo[0], 
                                                  objB = self.control_down.transform, 
                                                  maintainOffset = False)
                    pcn_up = nd.pointConstraint(objA = constraintTo[1], 
                                                objB = self.control_up.transform, 
                                                maintainOffset = False)
                    cmds.delete(pac, pcn_down, pcn_up)

                    #--- constraint the controls by given flag constraintType
                    #--- parent = parentConstraint
                    if constraintType == 'parent':
                        nd.parentConstraint(objA = constraintTo[0], 
                                            objB = self.control_down.transform,
                                            suffix = 'PAC', 
                                            maintainOffset = False)
                        nd.parentConstraint(objA = constraintTo[1], 
                                            objB = self.control_up.transform,
                                            suffix = 'PAC',
                                            maintainOffset = False)
                        #--- lock constraint attributes
                        attr.lockAttr(node = [self.control_down.transform,
                                              self.control_up.transform], 
                                      attribute = ['t', 'r'])                        
                    #--- point = pointConstraint
                    elif constraintType == 'point':
                        nd.pointConstraint(objA = constraintTo[0], 
                                           objB = self.control_down.transform,
                                           suffix = 'PCN', 
                                           maintainOffset = False)                        
                        nd.pointConstraint(objA = constraintTo[1], 
                                           objB = self.control_up.transform,
                                           suffix = 'PCN',
                                           maintainOffset = False)
                        #--- lock constraint attributes
                        attr.lockAttr(node = [self.control_down.transform,
                                              self.control_up.transform], 
                                      attribute = 't')
                    #--- orient = orientConstraint                    
                    elif constraintType == 'orient':
                        nd.orientConstraint(objA = constraintTo[0], 
                                            objB = self.control_down.transform,
                                            suffix = 'OCN', 
                                            maintainOffset = False)                        
                        nd.orientConstraint(objA = constraintTo[1], 
                                            objB = self.control_up.transform,
                                            suffix = 'OCN',
                                            maintainOffset = False)
                        #--- lock constraint attributes
                        attr.lockAttr(node = [self.control_down.transform,
                                              self.control_up.transform], 
                                      attribute = 'r')                        
                else:
                    raise Exception('Specified node: ' + constraintTo[1] +
                                    'does not exist!')
            else:
                raise Exception('Specified node: ' + constraintTo[0] +
                                'does not exist!')
    #END def __constraint_flexiplane()

    def __inherits_transform(self,
                               inheritsTransform = True):
        #--- this method sets the inherits transform attribute of the main group
        attr = attribute.Attribute()
        attr.setAttr(node = self.main, 
                     attribute = 'inheritsTransform', 
                     value = inheritsTransform)
    #END def __inherits_transform

    def __display_options(self):
        #--- this method connects all specified nodes' visibility attributes
        attr = attribute.Attribute()
        #--- joints
        for jnt in self.jnt:
            attr.connectAttr(node = [self.control_main.transform, jnt], 
                             attribute = ['showJoints', 'v'])
        #--- surface plane
        attr.connectAttr(node = [self.control_main.transform, 
                                 self.surface], 
                         attribute = ['showSurface', 'v'])            
        #--- locators
        for loc in self.locator:
            attr.connectAttr(node = [self.control_main.transform, loc], 
                             attribute = ['showUpVectors', 'v'])
        #--- blendShape setup
        attr.connectAttr(node = [self.control_main.transform, 
                                 self.extra_nodes], 
                         attribute = ['showBspSetup', 'v'])
    #END def __display_options()

    def __cleanup(self,
                   muscleSystem = False):
        #--- this method cleans up the flexiPlane nodes
        attr = attribute.Attribute()
#        attr.setAttr(node = self.extra_nodes, attribute = 'v', value = 0)
#        attr.setAttr(node = self.locator, attribute = 'v', value = 0)
        #--- lock attributes on the controls
        attr.lockAttr(node = [self.control_up.transform,
                              self.control_down.transform], 
                      attribute = ['ry', 'rz', 's'])
        attr.lockAttr(node = self.control_mid.transform, 
                      attribute = ['r', 's'])
        attr.lockAttr(node = self.control_main.transform, 
                      attribute = ['s', 'v'])
#        attr.setAttr(node = self.surface, attribute = 'v', value = 0)
        if muscleSystem:
            attr.lockAttr(node = self.mus_ctl.transform, 
                          attribute = ['v'])
        #--- lock all nodes
        attr.lockAll(node = self.main)
        attr.lockAll(node = self.extra_nodes)        
        attr.lockAll(node = self.locator)
        attr.lockAll(node = self.jnt_grp)
        attr.lockAll(node = self.jnt)
        sel = cmds.ls('*GRP*', '*DEF*', '*AIM', '*PAC', '*PCN', '*OCN', '*SCN',
                      '*CLS*', '*FOL*', '*LOC*', '*BLC', '*CND', '*MLT', '*CRV',
                      '*RMV', '*DCM', '*tweak*', '*_Shape*', '*surface', '*NRB', 
                      '*BSP', 'makeNurbPlane*', '*FPCTLShape', '*CRVShape', 
                      '*ShapeShape', '*NRBShape', '*surfaceShape')
        for i in sel:
            attr.lockAll(node = i)
            cmds.setAttr(i + '.ihi', 0)
        #--- print self.main + ' setup successfully created!'
    #END def __cleanup()

    def __create(self,
                  character = None,
                  mod = None,
                  side = None,
                  name = None,
                  color = 0,
                  size = 1,
                  length = 5,
                  position = [0,0,0],
                  rotation = [0,0,0],
                  constraintTo = [None, None],
                  constraintType = None,
                  follow = False,
                  aimVector = [1,0,0],
                  upVector = [0,1,0],
                  muscleSystem = False,
                  muscles = 1,
                  mesh = None,
                  parent = None,
                  inheritsTransform = True):
        #--- this is the main create method
        #--- create the group setup
        self.__create_group_setup(mod = mod,
                                  side = side,
                                  name = name,
                                  parent = parent)
        #--- create the plane
        self.__create_plane(length = length)
        #--- create the follicle setup()
        self.__follicle_setup(length = length)
        #--- aim the joints
        self.__aim_joints(aimVector = aimVector,
                          upVector = upVector)
        #--- create the flexiPlane controls
        self.__create_controls(mod = mod,
                               side = side,
                               name = name,
                               color = color,
                               size = size,
                               follow = follow)
        #--- add control attributes
        self.__add_control_attributes(muscleSystem = muscleSystem,
                                      muscles = muscles)
        #--- setup controls
        self.__setup_controls()
        #--- create the proper blendshape setup
        self.__create_blendshape_setup(character = character,
                                       mod = mod,
                                       side = side,
                                       name = name,
                                       follow = follow)
        #--- create the squash and stretch setup
        self.__squash_stretch()
        #--- create a volume system
        self.__volume_system(length = length)
        if muscleSystem:
            #--- create a simple muscle system
            self.__muscle_system(mod = mod,
                                 side = side,
                                 name = name,
                                 color = color,
                                 size = size,
                                 length = length,
                                 rotation = rotation,
                                 muscles = muscles,
                                 mesh = mesh)
        #--- reposition and rotate the main control
        self.__reposition_flexiplane(position = position,
                                     rotation = rotation)
        #--- constraint the main, up and down controls
        self.__constraint_flexiplane(constraintTo = constraintTo,
                                     constraintType = constraintType)
        #--- setup the inheritsTransform attribute of the main group
        self.__inherits_transform(inheritsTransform = inheritsTransform)
        #--- setup display option connections of the nodes
        self.__display_options()
        #--- call the cleanup method
        self.__cleanup(muscleSystem = muscleSystem)       
    #END def __create()
#END class FlexiPlane()

