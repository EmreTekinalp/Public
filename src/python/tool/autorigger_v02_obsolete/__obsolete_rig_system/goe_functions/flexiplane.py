'''
Created on 08.11.2013
@author: Emre Tekinalp
@email: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This class creates a flexiPlane
'''

from maya import cmds

from goe_functions import attribute, controls, curve, deformer, goe, node
from decimal import *

reload(attribute)
reload(controls)
reload(curve)
reload(deformer)
reload(goe)
reload(node)


class FlexiPlane(object):
    """
    This class creates a flexiPlane which is useful for stretchy and bendy
    functionalities in the rig.
    """

    def __init__(self,
                 mod=None,
                 side=None,
                 name=None,
                 color=0,
                 size=1,
                 length=5,
                 position=[0, 0, 0],
                 rotation=[0, 0, 0],
                 constraintTo=[None, None],
                 constraintType=None,
                 follow=False,
                 aimVector=[1, 0, 0],
                 upVector=[0, 1, 0],
                 muscleSystem=False,
                 muscles=1,
                 mesh=None,
                 parent=None,
                 inheritsTransform=True,
                 hideControls=False):
        #--- args
        self._mod = mod
        self._side = side
        self._name = name
        self._color = color
        self._size = size
        self._length = length
        self._position = position
        self._rotation = rotation
        self._constraintTo = constraintTo
        self._constraintType = constraintType
        self._follow = follow
        self._aimVector = aimVector
        self._upVector = upVector
        self._muscleSystem = muscleSystem
        self._muscles = muscles
        self._mesh = mesh
        self._parent = parent
        self._inheritsTransform = inheritsTransform
        self._hideControls = hideControls

        #--- vars
        self.name = None
        self.main = None
        self.global_move = None
        self.follicle_grp = None
        self.extra_nodes = None
        self.cluster_grp = None

        self.surface = None

        self.follicle = list()
        self.volume_up = list()
        self.volume_down = list()
        self.jnt_grp = list()
        self.jnt = list()
        self.locator = list()

        self.control_up = list()
        self.control_down = list()
        self.control_mid = list()
        self.control_main = list()
        self.jnt_ctl = list()
        self.clstr_mid_grp = list()

        self.bsp_surface = None
        self.curve = None
        self.curve_info = None
        self.twist = list()
        self.twist_handle = None

        self.muscle_surface = None
        self.mus_ctl = list()

        #--- methods
        self.__create()
    #END __init__()

    def __create_group_setup(self):
        """ Create a proper group structure """
        #--- create the hierarchical group structure
        self.name = (self._side + '_' + self._mod +
                     self._name[0].upper() + self._name[1:])
        self.main = node.transform(name=self.name, suffix='FLP', parent=self._parent)
        self.global_move = node.transform(name=self.name + '_globalMove',
                                          parent=self.main)
        self.follicle_grp = node.transform(name=self.name + '_follicle',
                                           suffix='GRP', parent=self.main)
        self.extra_nodes = node.transform(name=self.name + '_extraNodes',
                                          parent=self.main)
        self.cluster_grp = node.transform(name=self.name + '_clstr',
                                          suffix='GRP', parent=self.extra_nodes)
    #END __create_group_setup()

    def __create_plane(self):
        """ Create a nurbsPlane based on flag specifications """
        self.surface = cmds.nurbsPlane(degree=3, width=10, lengthRatio=0.2,
                                       patchesU=self._length, patchesV=1,
                                       axis=(0, 1, 0), name=self.name + '_surface')[0]
        #--- parent the surface under the global movement group
        cmds.parent(self.surface, self.global_move)
    #END __create_plane()

    def __follicle_setup(self):
        """ Create the proper follicle, joint and locator setup """
        #--- get the cvs of the surface
        follicle_count = cmds.ls(self.surface + '.cv[*]', flatten=True)
        #--- the begin of the follicle loop setup
        for i in range(len(follicle_count[:self._length])):
            if not i:
                continue
            #--- create a follicle
            follicle = node.follicle(name=self.name + `i`, suffix='FOL',
                                     parent=self.follicle_grp, show=False)
            self.follicle.append(follicle[0])
            #--- connect the follicle to the nurbsSurface
            goe.connectAttr(self.surface + '.local', follicle[1] + '.inputSurface')
            goe.connectAttr(self.surface + '.worldMatrix[0]',
                            follicle[1] + '.inputWorldMatrix')
            #--- connect the follicle scale attributes to the global movement
            node.scaleConstraint(objA=self.global_move, objB=follicle[0],
                                 suffix='SCN', maintainOffset=True)

            #--- reposition the follicles in u and v
            #--- get the U position, V is by default 0.5
            x = (10 / float(self._length))
            p = str(i * x)
            p = p.split('.')
            p = p[0] + p[1]
            if p == '00':
                continue
            u = str('0.') + str(p)
            goe.setAttr(follicle[1] + '.parameterU', float(u))
            goe.setAttr(follicle[1] + '.parameterV', 0.5)

            #--- create a joint with the volumeShift groups
            #--- parent them under the follicle
            vol_up = node.transform(name=self.name + `i` + '_VolumeShiftUp',
                                    suffix='GRP', parent=follicle[0])
            vol_down = node.transform(name=self.name + `i` + '_VolumeShiftDown',
                                      suffix='GRP', parent=vol_up)
            jnt_grp = node.transform(name=self.name + `i`, suffix='JNT_GRP',
                                     parent=vol_down)
            jnt = cmds.joint(name=self.name + `i` + '_JNT', radius=0.5)
            #--- set the correct jointOrientX axis
            if i == len(follicle_count[:self._length]) - 1:
                getRot = cmds.getAttr(follicle[0] + '.rx')
                getInv = getRot * -1
                goe.setAttr(jnt + '.jointOrientX', getInv)
            #--- store the joint/group and the volume groups in lists
            self.volume_up.append(vol_up)
            self.volume_down.append(vol_down)
            self.jnt_grp.append(jnt_grp)
            self.jnt.append(jnt)

            #--- create a locator as the upVector of the joints
            locator = node.locator(name=self.name + 'UpVec' + `i`, suffix='LOC',
                                   position=[0, 0, 6], rotation=[0, 0, 0],
                                   parent=follicle[0])
            self.locator.append(locator)
    #END __follicle_setup()

    def __aim_joints(self):
        """ Aim the joints """
        for i in range(len(self.jnt_grp[:-1])):
            j = i + 1
            node.aimConstraint(target=self.jnt_grp[j], source=self.jnt_grp[i],
                               name=self.name + `i`, aimVector=self._aimVector,
                               upVector=self._upVector, worldUpType='object',
                               worldUpObject=self.locator[i])
            if not j == len(self.jnt_grp[:-1]):
                continue
            #--- create a group on top of the last joint
            cmds.select(self.jnt[-1])
            last_grp = cmds.group(name=self.jnt[-1].split('_JNT')[0]
                                  + 'Last_JNT_GRP')
            #--- set the rotation values of the last joint to zero
            goe.setAttr(self.jnt[-1] + '.r', 0, 0, 0)
            #--- get the mirrored aimVector
            if self._aimVector[0]:
                aimVector = [-1, 0, 0]
            elif aimVector[1]:
                aimVector = [0, -1, 0]
            elif aimVector[2]:
                aimVector = [0, 0, -1]
            node.aimConstraint(target=self.jnt[-2], source=last_grp,
                               name=self.name + `i`, aimVector=aimVector,
                               upVector=self._upVector, worldUpType='object',
                               worldUpObject=self.locator[i])
    #END __aim_joints()

    def __create_controls(self):
        """ Create the flexiPlane controls """
        #--- create main control
        name = self._mod + self._name[0].upper() + self._name[1:]
        self.control_main = controls.Control(side=self._side, name=name + 'Main',
                                             size=self._size + 0.75,
                                             shape=5, color=self._color,
                                             orientation=16, parent=self.main)
        #--- create up control
        self.control_up = controls.Control(side=self._side, name=name + 'Up',
                                           size=self._size + 0.25,
                                           shape=1, color=6, position=[5, 0, 0],
                                           parent=self.global_move)
        #--- create down control
        self.control_down = controls.Control(side=self._side, name=name + 'Down',
                                             size=self._size + 0.25,
                                             shape=1, color=6, position=[-5, 0, 0],
                                             parent=self.global_move)
        #--- create mid control
        self.control_mid = controls.Control(side=self._side, name=name + 'Mid',
                                            size=self._size + 0.25,
                                            shape=2, color=self._color,
                                            parent=self.global_move)
        if self._follow:
            node.pointConstraint(objA=[self.control_down.transform,
                                       self.control_up.transform],
                                 objB=self.control_mid.group, maintainOffset=False)

        #--- create individual joint controls, parented under the follicle
        for i in range(len(self.follicle)):
            j = i + 1
            #--- create main control
            jnt_ctl = controls.Control(side=self._side, name=name + "FlexiJnt" + `j`,
                                       size=self._size / 1.5,
                                       shape=1, color=13, rotation=[90, 0, 0],
                                       parent=self.follicle[i])
            goe.setAttr(jnt_ctl.group + '.t', 0, 0, 0)
            attribute.lock_n_hide(jnt_ctl.transform, ['t'])
            self.jnt_ctl.append(jnt_ctl)
    #END __create_controls()

    def __add_control_attributes(self):
        """ Add attributes to the main control """
        #--- globalScale
        cmds.addAttr(self.control_main.transform, longName='globalScale',
                     attributeType='float', min=0.0, max=10.0, defaultValue=1.0,
                     keyable=True)
        #--- volumeControls
        cmds.addAttr(self.control_main.transform, longName='volumeControls',
                     attributeType='enum', enumName=('__________'))
        cmds.setAttr(self.control_main.transform + '.volumeControls', edit=True,
                     channelBox=True, keyable=False)
        #--- volume
        cmds.addAttr(self.control_main.transform, longName='volume',
                     attributeType='float', min=0, max=1, defaultValue=1,
                     keyable=True)
        #--- volumeShift
        cmds.addAttr(self.control_main.transform, longName='volumeShift',
                     attributeType='float', min=-10, max=10, defaultValue=0,
                     keyable=True)
        #--- volumeDropoff
        cmds.addAttr(self.control_main.transform, longName='volumeDropoff',
                     attributeType='float', min=0, max=10, defaultValue=1,
                     keyable=True)

        #--- controls for the muscle system
        if self._muscleSystem:
            #--- muscle system
            cmds.addAttr(self.control_main.transform, longName='muscleSystem',
                         attributeType='enum', enumName=('__________'),
                         keyable=False, channelBox=True)
            for i in range(self._muscles):
                i = i + 1
                #--- muscle
                cmds.addAttr(self.control_main.transform, longName='muscle' + `i`,
                             attributeType='short', min=0, max=1, defaultValue=0)
                cmds.setAttr(self.control_main.transform + 'muscle' + `i`,
                             edit=True, keyable=False, channelBox=True)
                #--- muscle size
                cmds.addAttr(self.control_main.transform,
                             longName='muscle' + `i` + 'Size',
                             attributeType='float', min=0, max=50,
                             defaultValue=0, keyable=True)
                #--- muscle slide
                cmds.addAttr(self.control_main.transform,
                             longName='muscle' + `i` + 'Slide',
                             attributeType='float', min=0, max=1,
                             defaultValue=0, keyable=True)
                #--- muscle maxDisplace
                cmds.addAttr(self.control_main.transform,
                             longName='muscle' + `i` + 'MaxDisplace',
                             attributeType='float', min=0, max=50,
                             defaultValue=0.5, keyable=True)
                #--- muscle DropOff
                cmds.addAttr(self.control_main.transform,
                             longName='muscle' + `i` + 'DropOff',
                             attributeType='float', min=0.001, max=50,
                             defaultValue=1, keyable=True)

        #--- these are the general display options
        #--- display options
        cmds.addAttr(self.control_main.transform, longName='displayOptions',
                     attributeType='enum', enumName=('__________'))
        cmds.setAttr(self.control_main.transform + '.displayOptions', edit=True,
                     keyable=False, channelBox=True)
        #--- showJoints
        cmds.addAttr(self.control_main.transform, longName='showJoints',
                     attributeType='short', min=0, max=1, defaultValue=0)
        cmds.setAttr(self.control_main.transform + '.showJoints', edit=True,
                     keyable=False, channelBox=True)
        #--- showSurface
        cmds.addAttr(self.control_main.transform, longName='showSurface',
                     attributeType='short', min=0, max=1, defaultValue=0)
        cmds.setAttr(self.control_main.transform + '.showSurface', edit=True,
                     keyable=False, channelBox=True)
        #--- showUpVectors
        cmds.addAttr(self.control_main.transform, longName='showUpVectors',
                     attributeType='short', min=0, max=1, defaultValue=0)
        cmds.setAttr(self.control_main.transform + '.showUpVectors', edit=True,
                     keyable=False, channelBox=True)
        #--- showBspSetup
        cmds.addAttr(self.control_main.transform, longName='showBspSetup',
                     attributeType='short', min=0, max=1, defaultValue=0,)
        cmds.setAttr(self.control_main.transform + '.showBspSetup', edit=True,
                     keyable=False, channelBox=True)
    #END __add_control_attributes()

    def __setup_controls(self):
        """ Setup the controls properly """
        #--- lock and hide unnecessary attributes of the controls
        attribute.lock_attributes([self.control_down.transform,
                                   self.control_up.transform,
                                   self.control_mid.transform],
                                  ['s', 'v'], True, False)
        attribute.lock_all([self.control_down.group, self.control_up.group,
                            self.control_mid.group])

        #--- pointConstraint the joint controls,
        #--- connect the joints' jontOrient and jointGrp scale transforms
        for jnt in range(len(self.jnt_grp)):
            node.pointConstraint(objA=self.jnt_ctl[jnt].transform,
                                 objB=self.jnt_grp[jnt],
                                 maintainOffset=False)
            goe.connectAttr(self.jnt_ctl[jnt].transform + '.s',
                            self.jnt_grp[jnt] + '.s')
            #--- lock rotation and visibility attributes of the joint controls
            attribute.lock_attributes(self.jnt_ctl[jnt].transform, ['r', 'v'])
        #--- connect the globalScale of the main control with the scale one
        goe.connectAttr(self.control_main.transform + '.globalScale',
                        self.control_main.transform + '.sx')
        goe.connectAttr(self.control_main.transform + '.globalScale',
                        self.control_main.transform + '.sy')
        goe.connectAttr(self.control_main.transform + '.globalScale',
                        self.control_main.transform + '.sz')
        #--- parent the global movement group under the main control
        cmds.parent(self.global_move, self.control_main.transform)
    #END def __setup_controls()

    def __create_blendshape_setup(self):
        """ Create the blendShape setup """
        #--- duplicate the surface plane for the blendShape version
        bsp_name = self.surface + 'BlendShape'
        self.bsp_surface = cmds.duplicate(self.surface, name=bsp_name)[0]
        #--- reposition the bsp_plane
        goe.setAttr(self.bsp_surface + '.t', 0, 0, -5)

        #--- create a curve and store it's arcLen info
        crv = curve.Curve(side=self._side, mod=self._mod,
                          name=self._name + 'Wire', suffix='CRV',
                          degree=2, point=[[-5, 0, -5], [0, 0, -5], [5, 0, -5]])
        self.curve = crv
        #--- get the cv of the curve
        cv_start = crv.cv[0]
        cv_mid = crv.cv[1]
        cv_end = crv.cv[2]

        #--- create a cluster on each cv
        clstr_start = deformer.cluster(mod=self._mod, side=self._side,
                                       name=self._name + 'Start', suffix='CLS',
                                       geometry=cv_start, parent=self.cluster_grp)
        clstr_mid = deformer.cluster(mod=self._mod, side=self._side,
                                     name=self._name + 'Mid', suffix='CLS',
                                     geometry=cv_mid, parent=self.cluster_grp)
        clstr_end = deformer.cluster(mod=self._mod, side=self._side,
                                     name=self._name + 'End', suffix='CLS',
                                     geometry=cv_end, parent=self.cluster_grp)

        self.clstr_mid_grp = clstr_mid[0].split('CLS')[0] + 'GRP'
        if self._follow:
            node.pointConstraint(objA=[clstr_start[0], clstr_end[0]],
                                 objB=self.clstr_mid_grp, maintainOffset=False)

        #--- create a wire deformer on the curve affecting the blendShape surface
        wire = deformer.wire(mod=self._mod, side=self._side, name=self._name,
                             suffix='DEF', wire=crv.transform,
                             geometry=self.bsp_surface, dropoffDistance=20,
                             parent=self.extra_nodes)
        #--- create a twist deformer on the blendShape surface, rename them
        twist = deformer.twist(mod=self._mod, side=self._side, name=self._name,
                               suffix='DEF', geometry=self.bsp_surface,
                               rotation=[0, 0, 90], parent=self.extra_nodes)
        #--- reorder the input order properly
        cmds.reorderDeformers(wire[0], twist[0], self.bsp_surface)

        #--- create the blendShape
        deformer.blendshape(mod=self._mod, side=self._side, name=self._name,
                            suffix='BSP', shapes=self.bsp_surface,
                            target=self.surface, shapeAttr=self.bsp_surface,
                            shapeValue=1, lockAttr=self.bsp_surface)

        #--- do the proper control, cluster and deformer connections
        goe.connectAttr(self.control_down.transform + '.t', clstr_start[0] + '.t')
        goe.connectAttr(self.control_up.transform + '.t', clstr_end[0] + '.t')
        goe.connectAttr(self.control_mid.transform + '.t', clstr_mid[0] + '.t')
        goe.connectAttr(self.control_down.transform + '.rx', twist[-1] + '.endAngle')
        goe.connectAttr(self.control_up.transform + '.rx', twist[-1] + '.startAngle')

        #--- parent the nodes to the extra nodes group
        cmds.parent(self.bsp_surface, self.extra_nodes)
    #END __create_blendshape_setup()

    def __squash_stretch(self):
        """ Create the squash and stretch functionality """
        #--- create the necessary multiplyDivide and condition nodes
        mlt_up = node.multiplyDivide(name=self.name + 'SquashStretch', operation=2,
                                     input2X=self.curve.arclen, lockAttr='input2X')
        mlt_down = node.multiplyDivide(name=self.name + 'Divide', operation=2,
                                       input1X=1, lockAttr='input1X')
        cond = node.condition(name=self.name + 'SquashStretch',
                              firstTerm=1, secondTerm=0, operation=1,
                              lockAttr=['firstTerm', 'secondTerm'])
        blc = node.blendColors(name=self.name + 'SquashStretch',
                               color2R=1, lockAttr='color2R')

        #--- create the proper utility node connection setup
        goe.connectAttr(self.curve.info + '.arcLength', mlt_up + '.input1X')
        goe.connectAttr(mlt_up + '.outputX', mlt_down + '.input2X')
        goe.connectAttr(mlt_down + '.outputX', cond + '.colorIfTrueR')
        goe.connectAttr(cond + '.outColorR', blc + '.color1R')
        goe.connectAttr(self.control_main.transform + '.volume', blc + '.blender')

        #--- connect the blender output with the scale of the joints
        for jnt in self.jnt:
            goe.connectAttr(blc + '.outputR', jnt + '.sx')
            goe.connectAttr(blc + '.outputR', jnt + '.sy')
            goe.connectAttr(blc + '.outputR', jnt + '.sz')
    #END __squash_stretch()

    def __volume_system(self):
        """ Create a volume system by creating for every joint a setup to
        shift the volume scale and also change the volume size
        """
        #--- calculate the proper value for the dropOff and the shift amount
        #--- in regards of the specified length value
        step = Decimal(1) / Decimal(self._length)
        off = Decimal(1) / Decimal(self._length)
        for i in range(len(self.jnt_grp)):
            up = step
            down = Decimal(1) - Decimal(step)
            #--- create nodes for the volume setup
            rmv_up = node.remapValue(name=self.name + 'VolumeUpShift' + `i`,
                                     inputMin=1, inputMax=10,
                                     outputMin=1, outputMax=float(up))
            rmv_down = node.remapValue(name=self.name + 'VolumeDownShift' + `i`,
                                       inputMin=-10, inputMax=0,
                                       outputMin=float(down), outputMax=1)
            mlt = node.multiplyDivide(name=self.name + 'VolumeShift' + `i`)
            blc = node.blendColors(name=self.name + 'VolumeShift' + `i`,
                                   color2R=1, color2G=1,
                                   lockAttr=['color2R', 'color2G'])

            #--- create node connections to create a volume shift and dropOff
            goe.connectAttr(self.control_main.transform + '.volumeShift',
                            rmv_up + '.inputValue')
            goe.connectAttr(self.control_main.transform + '.volumeShift',
                            rmv_down + '.inputValue')
            goe.connectAttr(self.control_main.transform + '.volumeDropoff',
                            mlt + '.input1X')
            goe.connectAttr(self.control_main.transform + '.volumeDropoff',
                            mlt + '.input1Y')
            goe.connectAttr(rmv_up + '.outValue', mlt + '.input2X')
            goe.connectAttr(rmv_down + '.outValue', mlt + '.input2Y')
            goe.connectAttr(mlt + '.outputX', blc + '.color1R')
            goe.connectAttr(mlt + '.outputY', blc + '.color1G')
            goe.connectAttr(self.control_main.transform + '.volume',
                            blc + '.blender')
            #--- connect the blc output to the scale values of the joints volGrp
            for axis in 'xyz':
                scale = '.s' + axis
                goe.connectAttr(blc + '.outputR', self.volume_up[i] + scale)
                goe.connectAttr(blc + '.outputG', self.volume_down[i] + scale)
            #--- this part is increasing the steps given by the length value
            step = step + off
    #END __volume_system()

    def __muscle_system(self):
        """ Create a simple muscle system based on sculptDeformers """
        if not self._muscleSystem:
            return
        #--- check if specified mesh is a mesh
        if self._mesh:
            msg = 'Specified mesh: ' + str(self._mesh) + ' does not exist!'
            assert cmds.objExists(self._mesh), msg
            child = cmds.listRelatives(self._mesh, allDescendents=True)
            node_type = cmds.nodeType(child)
            msg = 'Specified mesh: ' + str(self._mesh) + ' is not a mesh!'
            assert node_type == 'mesh', msg
            if not self._muscles < 1:
                #--- create a nurbsPlane
                self.muscle_surface = cmds.nurbsPlane(degree=1, width=10,
                                                      lengthRatio=0.2,
                                                      patchesU=self._length,
                                                      patchesV=1, axis=(0, 1, 0),
                                                      name=self.name + 'Muscle_NRB')[0]
                #--- rotate the muscle surface
                goe.setAttr(self.muscle_surface + '.r', self._rotation)
                #--- parent the muscle surface under extra nodes
                cmds.parent(self.muscle_surface, self.extra_nodes)
                #--- create a follicle by the given amount of the muscles flag
                for i in range(self._muscles):
                    i = i + 1
                    if i == 0:
                        continue
                    #--- MUSCLE FOLLICLE SETUP JUST SCULPT DEFORMER
                    #--- create a follicle on the muscle plane
                    mus_follicle = node.follicle(name=self.name + 'Muscle' + `i`,
                                                 suffix='FOL', parameterU=0,
                                                 parameterV=0.5,
                                                 parent=self.follicle_grp,
                                                 show=False, lockAttr='parameterV')
                    #--- connect the follicle with the muscle surface
                    goe.connectAttr(self.muscle_surface + '.local',
                                    mus_follicle[1] + '.inputSurface')
                    goe.connectAttr(self.muscle_surface + '.worldMatrix[0]',
                                    mus_follicle[1] + '.inputWorldMatrix')
                    #--- connect the main control and the muscle follicle
                    at = '.muscle' + `i` + 'Slide'
                    goe.connectAttr(self.control_main.transform + at,
                                    mus_follicle[1] + '.parameterU')

                    #--- NORMAL FOLLICLE SETUP, MUSCLE CTL DRIVES SCULPT
                    #--- create a follicle on the normal surface
                    norm_follicle = node.follicle(name=self.name + 'MuscleCtl' + `i`,
                                                  suffix='FOL', parameterU=0,
                                                  parameterV=0.5,
                                                  parent=self.follicle_grp,
                                                  show=False, lockAttr='parameterV')
                    #--- connect the follicle with the normal surface
                    goe.connectAttr(self.surface + '.local',
                                    norm_follicle[1] + '.inputSurface')
                    goe.connectAttr(self.surface + '.worldMatrix[0]',
                                    norm_follicle[1] + '.inputWorldMatrix')
                    #--- connect the normal follicle scale attributes to the globalMovement group
                    node.scaleConstraint(objA=self.global_move, objB=norm_follicle[0],
                                         maintainOffset=True)
                    #--- create connections between the main control and the muscle follicle
                    at = '.muscle' + `i` + 'Slide'
                    goe.connectAttr(self.control_main.transform + at,
                                    norm_follicle[1] + '.parameterU')

                    #--- SCULPT DEFORMER
                    #--- create a control for the sculpt deformer and set it up
                    nme = self._mod + self._name[0].upper() + self._name[1:] + 'Muscle' + `i`
                    self.mus_ctl = controls.Control(side=self._side, name=nme,
                                                    suffix='FPCTL',
                                                    size=self._size + 0.1,
                                                    shape=2, color=self._color,
                                                    parent=norm_follicle[0])
                    #--- connect the size attr of the main control with the
                    #--- scale of the muscle controls' group
                    for axis in 'xyz':
                        at = '.muscle' + `i` + 'Size'
                        goe.connectAttr(self.control_main.transform + at,
                                        self.mus_ctl.group + '.s' + axis)
                    #--- connect the visiblity of the control with the
                    #--- muscle attr of the main control
                    goe.connectAttr(self.control_main.transform + '.muscle' + `i`,
                                    self.mus_ctl.transform + '.v')
                    #--- create a sculpt deformer and parent it under the muscle follicle
                    sculpt = deformer.sculpt(mod=self._mod, side=self._side,
                                             name=self._name + 'Muscle',
                                             suffix='DEF', geometry=self._mesh,
                                             dropoffDistance=0.14,
                                             parent=mus_follicle[0])

                    #--- CONNECTION MUSCLE CONTROL WITH SCULPT DEFORMER
                    #--- connect the muscle size attr with the sculpt radius
                    at = '.muscle' + `i` + 'Size'
                    goe.connectAttr(self.control_main.transform + at,
                                    sculpt[1] + '.radius')
                    attribute.lock_attributes(sculpt[0], ['s'], False)
                    #--- connect the muscle controls scale with the sculpt one
                    goe.connectAttr(self.mus_ctl.transform + '.s', sculpt[0] + '.s')
                    #--- connect the muscle MaxDisplacement attr with the sculpt one
                    at = '.muscle' + `i` + 'MaxDisplace'
                    goe.connectAttr(self.control_main.transform + at,
                                    sculpt[2] + '.maximumDisplacement')
                    #--- connect the muscle dropOff attr with the sculpt one
                    at = '.muscle' + `i` + 'DropOff'
                    goe.connectAttr(self.control_main.transform,
                                    sculpt[2] + '.dropoffDistance')
                    #--- connect t and r of the sculpt with the muscle ctl
                    goe.connectAttr(self.mus_ctl.transform + '.t', sculpt[0] + '.t')
                    goe.connectAttr(self.mus_ctl.transform + '.r', sculpt[0] + '.r')
                    #--- lock tx attribute of the muscle ctl
                    attribute.lock_attributes(self.mus_ctl.transform, ['tx'])
                    #--- set the sculpts' transform values to default
                    goe.setAttr(sculpt[-1] + '.t', 0, 0, 0)
                    goe.setAttr(sculpt[-1] + '.r', 0, 0, 0)
                    attribute.lock_attributes(sculpt[-1], ['t', 'r'])
                    cmds.setAttr(sculpt[0] + '.visibility', 0, lock=True)

                #--- COMPUTE PART
                #--- compute the steps to go to locate the cv's translateX position
                step = (10 / float(self._length))
                off = (10 / float(self._length))
                cv_pos = [[-5.0, 0.0, 0.0]]
                for i in range(self._length):
                    res = -5 + step
                    pos = [res, 0.0, 0.0]
                    cv_pos.append(pos)
                    step = +step + off
                #--- create the curves based on the computed position
                #--- and create clusters for each cv
                crv = cmds.curve(degree=2, point=cv_pos)
                mus_crv = cmds.rename(crv, self.name + 'Muscle_CRV')
                mus_cvs = cmds.ls(mus_crv + '.cv[*]', flatten=True)
                cmds.parent(mus_crv, self.extra_nodes)
                #--- create a matrix setup to connect the cvs with the control
                for i in range(len(mus_cvs)):
                    dcm = node.decomposeMatrix(name=self.name + 'Muscle' + `i`)
                    if i == 0:
                        goe.connectAttr(self.control_down.transform + '.worldMatrix[0]',
                                        dcm + '.inputMatrix')
                        goe.connectAttr(dcm + '.outputTranslate',
                                        mus_crv + '.controlPoints[0]')
                    elif i == (len(mus_cvs) - 1):
                        goe.connectAttr(self.control_up.transform + '.worldMatrix[0]',
                                        dcm + '.inputMatrix')
                        at = 'controlPoints[' + str(len(mus_cvs) - 1) + ']'
                        goe.connectAttr(dcm + '.outputTranslate', mus_crv + at)
                    else:
                        goe.connectAttr(self.jnt_ctl[i - 1].transform + '.worldMatrix[0]',
                                        dcm + '.inputMatrix')
                        at = '.controlPoints[' + `i` + ']'
                        goe.connectAttr(dcm + '.outputTranslate', mus_crv + at)
    #END __muscle_system()

    def __reposition_flexiplane(self):
        """ Reposition the flexiPlane """
        p = self._position
        r = self._rotation
        goe.setAttr(self.control_main.transform + '.t', p[0], p[1], p[2])
        goe.setAttr(self.control_main.transform + '.r', r[0], r[1], r[2])
    #END __reposition_flexiplane()

    def __constraint_flexiplane(self):
        """ Constraint the main control by specified nodes """
        #--- check given flags
        if not self._constraintTo == [None, None]:
            msg = 'Specified node: ' + self._constraintTo[0] + 'does not exist!'
            assert cmds.objExists(self._constraintTo[0]), msg
            assert cmds.objExists(self._constraintTo[1]), msg
            #--- constraint the controls to proper positions
            pac = node.parentConstraint(objA=self._constraintTo,
                                        objB=self.control_main.transform,
                                        maintainOffset=False)
            pcn_down = node.pointConstraint(objA=self._constraintTo[0],
                                            objB=self.control_down.transform,
                                            maintainOffset=False)
            pcn_up = node.pointConstraint(objA=self._constraintTo[1],
                                          objB=self.control_up.transform,
                                          maintainOffset=False)
            cmds.delete(pac, pcn_down, pcn_up)

            #--- constraint the controls by given flag constraintType
            #--- parent = parentConstraint
            if self._constraintType == 'parent':
                node.parentConstraint(objA=self._constraintTo[0],
                                      objB=self.control_down.transform,
                                      suffix='PAC', maintainOffset=False)
                node.parentConstraint(objA=self._constraintTo[1],
                                      objB=self.control_up.transform,
                                      suffix='PAC', maintainOffset=False)
                #--- lock constraint attributes
                attribute.lock_attributes([self.control_down.transform,
                                           self.control_up.transform], ['t', 'r'])
            #--- point = pointConstraint
            elif self._constraintType == 'point':
                node.pointConstraint(objA=self._constraintTo[0],
                                     objB=self.control_down.transform,
                                     suffix='PCN', maintainOffset=False)
                node.pointConstraint(objA=self._constraintTo[1],
                                     objB=self.control_up.transform,
                                     suffix='PCN', maintainOffset=False)
                #--- lock constraint attributes
                attribute.lock_attributes([self.control_down.transform,
                                           self.control_up.transform], ['t'])
            #--- orient = orientConstraint
            elif self._constraintType == 'orient':
                node.orientConstraint(objA=self._constraintTo[0],
                                      objB=self.control_down.transform,
                                      suffix='OCN', maintainOffset=False)
                node.orientConstraint(objA=self._constraintTo[1],
                                      objB=self.control_up.transform,
                                      suffix='OCN', maintainOffset=False)
                #--- lock constraint attributes
                attribute.lock_attributes([self.control_down.transform,
                                           self.control_up.transform], ['r'])
    #END __constraint_flexiplane()

    def __inherits_transform(self):
        """ Set the inherits transform attribute of the main group """
        goe.setAttr(self.main + '.inheritsTransform', self._inheritsTransform)
    #END def __inherits_transform

    def __display_options(self):
        """ Connect all specified nodes' visibility attributes """
        #--- joints
        for jnt in self.jnt:
            goe.connectAttr(self.control_main.transform + '.showJoints', jnt + '.v')
        #--- surface plane
        goe.connectAttr(self.control_main.transform + '.showSurface',
                        self.surface + '.v')
        #--- locators
        for loc in self.locator:
            goe.connectAttr(self.control_main.transform + '.showUpVectors', loc + '.v')
        #--- blendShape setup
        goe.connectAttr(self.control_main.transform + '.showBspSetup',
                        self.extra_nodes + '.v')
    #END __display_options()

    def __cleanup(self,):
        """ Cleanup the flexiPlane nodes """
        #--- lock attributes on the controls
        attribute.lock_attributes([self.control_up.transform,
                                   self.control_down.transform], ['ry', 'rz', 's'])
        attribute.lock_attributes(self.control_mid.transform, ['r', 's'])
        attribute.lock_attributes(self.control_main.transform, ['s', 'v'])
        if self._muscleSystem:
            attribute.lock_attributes(self.mus_ctl.transform, ['v'])
        #--- lock all nodes
        attribute.lock_all(self.main)
        attribute.lock_all(self.extra_nodes)
        attribute.lock_all(self.locator)
        attribute.lock_all(self.jnt_grp)
        attribute.lock_all(self.jnt)
        sel = cmds.ls('*GRP*', '*DEF*', '*AIM', '*PAC', '*PCN', '*OCN', '*SCN',
                      '*CLS*', '*FOL*', '*LOC*', '*BLC', '*CND', '*MLT', '*CRV',
                      '*RMV', '*DCM', '*tweak*', '*_Shape*', '*surface', '*NRB',
                      '*BSP', 'makeNurbPlane*', '*FPCTLShape', '*CRVShape',
                      '*ShapeShape', '*NRBShape', '*surfaceShape')
        for i in sel:
            attribute.lock_all(i)
            cmds.setAttr(i + '.ihi', 0)

        if self._hideControls:
            ctl = [self.control_down.transform, self.control_main.transform,
                   self.control_mid.transform, self.control_up.transform]
            for i in ctl:
                attribute.hide(i)
            for i in self.jnt_ctl:
                attribute.hide(i.transform)
    #END __cleanup()

    def __create(self):
        """ Call the methods in a proper order to build a flexiplane """
        #--- create the group setup
        self.__create_group_setup()

        #--- create the plane
        self.__create_plane()

        #--- create the follicle setup()
        self.__follicle_setup()

        #--- aim the joints
        self.__aim_joints()

        #--- create the flexiPlane controls
        self.__create_controls()

        #--- add control attributes
        self.__add_control_attributes()

        #--- setup controls
        self.__setup_controls()

        #--- create the proper blendshape setup
        self.__create_blendshape_setup()

        #--- create the squash and stretch setup
        self.__squash_stretch()

        #--- create a volume system
        self.__volume_system()

        #--- create a simple muscle system
        self.__muscle_system()

        #--- reposition and rotate the main control
        self.__reposition_flexiplane()

        #--- constraint the main, up and down controls
        self.__constraint_flexiplane()

        #--- setup the inheritsTransform attribute of the main group
        self.__inherits_transform()

        #--- setup display option connections of the nodes
        self.__display_options()

        #--- call the cleanup method
        self.__cleanup()
    #END __create()
#END FlexiPlane()
