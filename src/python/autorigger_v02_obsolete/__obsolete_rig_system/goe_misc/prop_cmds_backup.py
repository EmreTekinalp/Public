'''
@author:  etekinalp
@date:    Sep 12, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates prop rigs
'''

from maya import cmds
from goe_functions import controls, attribute, node
from goe_functions import rigs
reload(controls)
reload(attribute)
reload(node)
reload(rigs)


class PropCmds(rigs.RigCmds):
    def __init__(self,
                 side='C',
                 moduleName=None,
                 controlName=None,
                 guides=[],
                 meshes=None,
                 shape=14,
                 size=1,
                 color=None,
                 offsetGroups=0,
                 controlChain=True,
                 withGimbal=False,
                 useJoints=False,
                 jointChain=False,
                 addIk=[],
                 ikSolver='ikSCsolver',
                 rotateOrder='xyz',
                 addScaleToMeshes=[],
                 addScaleToControl=[],
                 addSpaceSwitch=[{'driven':None, 'drivers':None,
                                  'attrName':None, 'attrHolder':None,
                                  'withTranslation':None}],
                 limitTransforms=[{'node':None, 'attr':None,
                                   'min':None, 'max':None}],
                 lockAttrs={},
                 hideControls=False,
                 hide=None,
                 hookLastControl=None,
                 hook=None,
                 version=1.0):
        """
        @type  assetType:        string
        @param assetType:        specify the character type! (ie."HUMAN","FISH")

        @type  moduleName:       string
        @param moduleName:       specify the name of the module

        @type  controlName:      string
        @param controlName:      specify the controller name

        @type  side:             string
        @param side:             specify the side! (ie. 'C', 'L', 'R')

        @type  shape:            integer
        @param shape:            specify the number of the shape, default is 1

        @type  size:             float
        @param size:             specify the size of the control, default is 1

        @type  color:            integer
        @param color:            specify the number of the color, default is 17

        @type  guides:           list
        @param guides:           specify a list with the guideJoint names

        @type  meshes:           list
        @param meshes:           specify meshes which will be parentConstrained

        @type  useJoints:        bool
        @param useJoints:        define if meshes shall be constrained/skinBind
                                 if set to True you are creating joints

        @type  jointChain:       bool
        @param jointChain:       create a jointChain or separate joints

        @type  addIk:            list
        @param addIk:            specify the startJoint, endEffector and control
                                 under which the ik and joint shall be parented.
                                 You can specify one list with two elements ie.:
                                 ['jointA', 'jointB', controlA]
                                 Or you can specify lists in a list, ie.:
                                 [['jointA','jointB',controlA], 
                                 ['jointD','jointC',controlB],...])

        @type  ikSolver:         string
        @param ikSolver:         specify the ikSolver, default is ikRPsolver

        @type  controlChain:     bool
        @param controlChain:     create a controlChain or independent controls

        @type  offsetGroups:     integer
        @param offsetGroups:     specify the amount of control offsetGroups groups

        @type  addScaleToMeshes: list
        @param addScaleToMeshes: specify the mesh offsetGroups to add globalScale

        @type  addScaleToControl:list
        @param addScaleToControl:specify the controls to add a globalScale to

        @type  addSpaceSwitch:   dictionary in a list
        @param addSpaceSwitch:   specify a dictionary in a list which includes 
                                 the driven object, two drivers, the attrName, 
                                 the attribute Holder and the withTranslation.
                                 (ie: [{'driven':obj_GRP, 'drivers':[objA,objB], 
                                        'attrName':"world", 'attrHolder':obj_CTL,
                                        'withTranslation':True}])

        @type  withGimbal:       bool
        @param withGimbal:       specify if gimbal control shall be created

        @type  rotateOrder:      string/integer
        @param rotateOrder:      specify the rotateOrder as string or as integer

        @type  limitTransforms:  dictionary in a list
        @param limitTransforms:  specify a dictionary in a list which includes 
                                 the object name, one attribute, the min and the
                                 max keys storing the defined limitation values.
                                 (ie: [{'node': 'C_bla_CTL', 'attr': 'tx', 
                                        'min': -2, 'max': 2}])

        @type  lockAttrs:        dictionary
        @param lockAttrs:        specify a dictionary including the object name
                                 as key and a list of attributes as value. 
                                 (ie: {controlA:['t','rx'], controlB:['v','s']})

        @type  hideControl:      bool
        @param hideControl:      hide all the controls

        @type  hide:             string/list
        @param hide:             hide anything specified as string or list

        @type  hookLastControl:  string
        @param hookLastControl:  parent the last control under the specified node

        @type  hook:             string
        @param hook:             specify the parent under the control group 
                                 should be parented to. None is C_localGimbal_CTL

        @type  version:          float
        @param version:          this specifies the version number

        @type  outHooks:         dictionary
        @param outHooks:         this argument will be returned. To use it you
                                 have to specify as a key the description of
                                 the control you want to hook to. This basically
                                 consists of the following:

                                 modulename + Controlname + index
                                 moduleName  = 'test'
                                 controlName = 'obj'
                                 === >  outHooks['testObj0']
                                 
                                 with that you get the controlName, 
                                 if withGimbal is True, than you get the gimbal
        """
        super(PropCmds, self).__init__()

        #--- args
        self._side               = side
        self._shape              = shape
        self._size               = size
        self._color              = color
        self._moduleName         = moduleName
        self._controlName        = controlName
        self._guides             = guides
        self._meshes             = meshes
        self._useJoints          = useJoints
        self._jointChain         = jointChain
        self._addIk              = addIk
        self._ikSolver           = ikSolver
        self._controlChain       = controlChain
        self._offsetGroups       = offsetGroups
        self._addScaleToMeshes   = addScaleToMeshes
        self._addScaleToControl  = addScaleToControl
        self._addSpaceSwitch     = addSpaceSwitch
        self._withGimbal         = withGimbal
        self._rotateOrder        = rotateOrder
        self._limitTransforms    = limitTransforms
        self._lockAttrs          = lockAttrs
        self._hideControls       = hideControls
        self._hide               = hide
        self._hookLastControl    = hookLastControl
        self._hook               = hook

        #--- vars
        self.guides      = list()
        self.controls    = list()
        self.joints      = list()
        self.ik          = list()
        self.arrow       = list()
        self.pac         = list()
        self.scn         = list()
        self.lock        = list()
        self.outHooks    = dict()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        #--- check moduleName
        assert self._moduleName, ("moduleName: Please specify a string")
        assert isinstance(self._moduleName, str),("moduleName: Please specify a string")

        #--- check side
        assert self._side, ("side: Please specify 'C','L' or 'R'!")

        #--- check guideJoints
        assert self._guides,("guideJoints: No guides specified")
        assert isinstance(self._guides, list),("guideJoints: Please specify a list!")

        #--- check meshes
        if self._meshes:
            assert isinstance(self._meshes, list),('meshes: Please specify a list!')
            for mesh in self._meshes:
                if isinstance(mesh, list):
                    for m in mesh:
                        assert cmds.objExists(m),('meshes: Specified object ' 
                                                  + m + ' does not exist!')
                else:
                    assert cmds.objExists(mesh),('meshes: Specified object ' 
                                                 + mesh + ' does not exist!')

        #--- check addIk
        if self._addIk:
            assert isinstance(self._addIk, list),("addIk: Please specify a list!")
            self._useJoints = True
            self._jointChain= True

        #--- check addScaleToMeshes
        if self._addScaleToMeshes:
            assert isinstance(self._addScaleToMeshes, list),("addScaleToMeshes: "
                                                            "Please specify a list "
                                                            "with transforms!")

        #--- check addScaleToControl
        if self._addScaleToControl:
            assert isinstance(self._addScaleToControl, list),("addScaleToControl: "
                                                             "Please specify a list "
                                                             "with controls!")

        #--- check rotateOrder
        assert self._rotateOrder,("rotateOrder: Please specify a valid string "
                                 "or an integer!")

        #--- check limitTransforms
        if self._limitTransforms:
            assert isinstance(self._limitTransforms, list),("limitTransforms: "
                                                           "Please specify a list!")
            for d in self._limitTransforms:
                node = None
                attr = None
                for i in d.items():
                    if i[0] == 'node':
                        node = i
                    elif i[0] == 'attr':
                        attr = i
                    elif i[0] == 'min':
                        pass
                    elif i[0] == 'max':
                        pass
                    else:
                        raise Exception("limitTransforms: Please define 'node', "
                                        "'attr', 'min', 'max' as keys!")
                if not node[1]:
                    if attr[1]:
                        raise Exception("limitTransforms: Please specify a node!")
                else:
                    if not attr[1]:
                        raise Exception("limitTransforms: Please specify attribute!")
                    if not isinstance(attr[1], str):
                        raise Exception("limitTransforms: Please specify only one"
                                       " valid attribute per dictionary!")
        #--- check lockAttrs
        if self._lockAttrs:
            assert isinstance(self._lockAttrs, dict),("lockAttrs: Please specify"
                                                     " a dictionary!")

        #--- hook
        if self._hook:
            assert cmds.objExists(self._hook),("hook: Specified hook does not exist: " 
                                              + self._hook)
    #END __check_parameters()

    def __prepare_guides(self):
        to_delete = list()
        for gd in self._guides:
            shapes = cmds.ls(type='goe_locator')
            if not shapes:
                continue
            for shp in shapes:
                trn = cmds.listRelatives(shp, parent=True, type='transform')[0]
                grp = cmds.listRelatives(trn, parent=True, type='transform')[0]
                if cmds.objExists(trn + '.guideID'):
                    if cmds.getAttr(trn + '.side') == self._side:
                        if cmds.getAttr(trn + '.guideID') == gd:
                            nme = cmds.getAttr(trn + '.name')
                            pos = cmds.xform(trn, query=True, translation=True, 
                                             worldSpace=True)
                            rot = cmds.xform(trn, query=True, rotation=True, 
                                             worldSpace=True)
                            self.guides.append([nme, pos, rot])
                            to_delete.append(grp)
        for d in to_delete:
            if cmds.objExists(d):
                cmds.delete(d)

        if not self._color:
            if self._side == 'L':
                self._color= 6
            elif self._side == 'R':
                self._color= 13
            elif self._side == 'C':
                self._color= 17
    #END __prepare_guides()

    def __create_mod_group(self):
        self.mod_grp = self._side + '_' + self.guides[0][0] + '_MOD'
        if self._moduleName:
            self.mod_grp = self._side + '_' + self._moduleName + '_MOD'
        if not cmds.objExists(self.mod_grp):
            self.mod_grp = cmds.createNode('transform', name=self.mod_grp,
                                            parent=self.rig_grp)
        attribute.lock_all(self.mod_grp)
    #END __create_mod_group()

    def __setup_mod_group(self):
        #--- showJoints
        if not cmds.objExists(self.mod_grp + '.showJoints'):
            cmds.addAttr(self.mod_grp, longName='showJoints', 
                         attributeType='float', defaultValue=0, min=0, max=1)
            cmds.setAttr(self.mod_grp + '.showJoints', 
                         edit=True, channelBox=True)
    #END __setup_mod_group()

    def __create_controls(self):
        for num, i in enumerate(self.guides):
            name = None
            pos = i[1]
            rot = i[2]
            if self._controlName:
                n = self._controlName[0].upper() + self._controlName[1:] + `num`
                name = self._moduleName + n
            else:
                name = self._moduleName + `num`
            ctl = controls.Control(side=self._side, 
                                   name=name, 
                                   shape=self._shape,
                                   size=self._size,
                                   color=self._color,
                                   position=pos,
                                   rotation=rot,
                                   withGimbal=self._withGimbal,
                                   rotateOrder=self._rotateOrder,
                                   offsetGroups=self._offsetGroups,
                                   parent=self.mod_grp)
            #--- append to a list
            self.controls.append(ctl)
    #END __create_controls()

    def __setup(self):
        if not self._hook:
            self._hook = self.main_control.gimbal
        for i, ctl in enumerate(self.controls):
            if self._controlChain:
                j = i + 1
                if not i:
                    if self._hookLastControl:
                        if ctl == self.controls[-1]:
                            return
                    attribute.lock_n_hide(self.controls[i].group, ['t', 'r', 's'], True)
                    if self._hook:
                        cmds.parent(self.controls[i].group, self._hook)
                    attribute.lock_n_hide(self.controls[i].group, ['t', 'r', 's'])
                if not j == len(self.controls):
                    try:
                        if self._hookLastControl:
                            if ctl == self.controls[-1]:
                                return
                        attribute.lock_n_hide(self.controls[j].group, ['t', 'r', 's'], True)
                        cmds.parent(self.controls[j].group, ctl.transform)
                        attribute.lock_n_hide(self.controls[j].group, ['t', 'r', 's'])
                    except:
                        pass
            else:
                if self._hookLastControl:
                    if ctl == self.controls[-1]:
                        return
                attribute.lock_n_hide(ctl.group,['t', 'r', 's'], True)
                if self._hook:
                    cmds.parent(ctl.group, self._hook)
                attribute.lock_n_hide(ctl.group,['t', 'r', 's'])
    #END __setup()

    def __prepare_constraints(self):
        if not self._meshes:
            return
        if not len(self.controls) == len(self._meshes):
            #--- controls = [ctlA], meshes = [meshA, meshB]
            if len(self._meshes) == 1: 
                ctl = self.controls[-1].transform
                #--- meshes = [meshA] OR meshes = [[meshC, meshD]]
                if self._withGimbal:
                    ctl = self.controls[-1].gimbal
                mesh = self._meshes[0]
                if isinstance(mesh, list):
                    #--- meshes = [[meshC, meshD]], controls = [..,ctlLast]
                    for m in mesh:
                        self.__create_constraints(m, ctl)
                else:
                    #--- meshes = [meshA], controls = [..,ctlLast]
                    self.__create_constraints(mesh, ctl)
            elif len(self.controls) == 1:
                ctl = self.controls[0].transform
                #--- controls = [ctlA]
                if self._withGimbal:
                    ctl = self.controls[0].gimbal
                for mesh in self._meshes:
                    if isinstance(mesh, list):
                        #--- controls = [ctlA], meshes = [[meshC, meshD]]
                        for m in mesh:
                            self.__create_constraints(m, ctl)
                    else:
                        #--- controls = [ctlA], meshes = [meshA, meshB]
                        self.__create_constraints(mesh, ctl)
        else:
            #--- controls = [ctlA, ctlB], meshes = [meshA, meshB]
            for ctl, mesh in zip(self.controls, self._meshes):
                ctrl = ctl.transform
                if self._withGimbal:
                    ctrl = ctl.gimbal
                if isinstance(mesh, list):
                    #--- controls = [ctlA, ctlB], meshes = [[meshC, meshD]]
                    for m in mesh:
                        self.__create_constraints(m, ctrl)
                else:
                    #--- meshes = [meshA, meshB]
                    self.__create_constraints(mesh, ctrl)
    #END __prepare_constraints()

    def __create_constraints(self, mesh, ctl):
        """
        @type  mesh: string
        @param mesh: specify the mesh

        @type  ctl: string
        @param ctl: specify the control
        """
        attribute.lock_all(mesh, True)
        pac = node.parentConstraint(ctl, mesh)
        scn = node.scaleConstraint(ctl, mesh)

        self.lock.append(pac)
        self.lock.append(scn)
        if self._addScaleToControl:
            for c in self._addScaleToControl:
                if c == ctl:
                    scn = node.scaleConstraint(ctl, mesh)
                    self.lock.append(scn)
        attribute.lock_all(mesh)
    #END __create_constraints()

    def __prepare_joint_setup(self):
        for num, i in enumerate(self.guides):
            cmds.select(clear = True)
            pos = i[1]
            rot = i[2]
            self.__createJointSetup(num, pos, rot)
    #END __prepare_joint_setup()

    def __createJointSetup(self, num, pos, rot):
        """
        @type  num: int
        @param num: specify the index num

        @type  pos: list
        @param pos: specify the position values

        @type  rot: list
        @param rot: specify the rotation values
        """
        ctl = self.controls[num].transform
        if self._withGimbal:
            ctl = self.controls[num].gimbal
        jnt_name = (self._side + '_' + self._moduleName + `num` + '_JNT')
        if self._controlName:
            jnt_name = (self._side + '_' + self._moduleName + 
                        self._controlName[0].upper() + 
                        self._controlName[1:] + `num` + '_JNT')
        jnt = cmds.joint(name = jnt_name)
        cmds.xform(jnt, translation = pos, worldSpace = True)
        cmds.setAttr(jnt + '.rotate', rot[0], rot[1], rot[2])

        if self._jointChain:
            if not num:
                #--- parent the joint under the control
                cmds.parent(jnt, ctl)
                cmds.setAttr(jnt + '.t', 0,0,0)
                cmds.setAttr(jnt + '.r', 0,0,0)
                cmds.setAttr(jnt + '.jo', 0,0,0)
        else:
            #--- parent the joint under the control
            cmds.parent(jnt, ctl)
            cmds.setAttr(jnt + '.t', 0,0,0)
            cmds.setAttr(jnt + '.r', 0,0,0)
            cmds.setAttr(jnt + '.jo', 0,0,0)
        #--- connect visibility of joints with main group
        cmds.connectAttr(self.mod_grp + '.showJoints', jnt + '.v')
        main = self.main_control.transform + '.globalScale'
        cmds.connectAttr(main, jnt + '.radius')

        #--- change draw style
        cmds.setAttr(jnt + '.drawStyle', 0)
        self.joints.append(jnt)
    #END __createJointSetup()

    def __create_joint_chain(self):
        for i, jnt in enumerate(self.joints):
            j = i + 1
            if not j == len(self.joints):
                cmds.parent(self.joints[j], jnt)
                cmds.setAttr(self.joints[j] + '.r', 0,0,0)
                cmds.setAttr(self.joints[j] + '.jo', 0,0,0)
                cmds.setAttr(jnt + '.r', 0,0,0)
                cmds.setAttr(jnt + '.jo', 0,0,0)
        cmds.setAttr(self.joints[-1] + '.r', 0,0,0)
        cmds.setAttr(self.joints[-1] + '.jo', 0,0,0)
    #END __create_joint_chain()

    def __create_ik_setup(self):
        if not self._addIk:
            return
        name = self._controlName[0].upper() + self._controlName[1:]
        if type(self._addIk[0]).__name__ == 'list':
            for i, jnt in enumerate(self._addIk):
                for j in jnt:
                    if not cmds.nodeType(j) == 'joint':
                        nt = cmds.nodeType(j)
                        raise Exception('addIk: Please specify a joint! '
                                       'You have specified this nodeType: ' + nt)
                ik_name = self._side + '_' + self._moduleName + name + `i` + '_IKH'
                ik_eff = self._side + '_' + self._moduleName + name + `i` + '_EFF'
                ik = cmds.ikHandle(startJoint = jnt[0], 
                                   endEffector = jnt[1], 
                                   solver = self._ikSolver, 
                                   name = ik_name)
                eff = cmds.rename(ik[1], ik_eff)
                ik = [ik[0], eff]
                cmds.parent(ik[0], jnt[2])
                cmds.setAttr(ik[0] + '.v', 0)
                cmds.setAttr(ik[0] + '.t', 0,0,0)
                #--- cleanup the ik
                for l in ik:
                    attribute.lock_all(l)
                    cmds.setAttr(l + '.ihi', 0)
                self.ik.append(ik[0])
        else:
            ik_name = self._side + '_' + self._moduleName + name + '_IKH'
            ik_eff = self._side + '_' + self._moduleName + name + '_EFF'
            ik = cmds.ikHandle(startJoint = self._addIk[0], 
                               endEffector = self._addIk[1], 
                               solver = self._ikSolver, 
                               name = ik_name)
            eff = cmds.rename(ik[1], ik_eff)
            ik = [ik[0], eff]
            cmds.parent(ik[0], self._addIk[2])
            cmds.setAttr(ik[0] + '.v', 0)
            cmds.setAttr(ik[0] + '.t', 0,0,0)
            #--- cleanup the ik
            for l in ik:
                attribute.lock_all(l)
                cmds.setAttr(l + '.ihi', 0)
            self.ik.append(ik[0])
    #END __create_ik_setup()

    def __add_scale_to_meshes(self):
        #--- add the globalScale setup to the specified mesh offset groups
        if self._addScaleToMeshes:
            for mesh in self._addScaleToMeshes:
                attribute.lock_all(mesh, True)
                for axis in 'xyz':
                    main = self.baseNodes["mainControl"] + '.globalScale'
                    if not cmds.isConnected(main, mesh + '.s' + axis):
                        cmds.connectAttr(main, mesh + '.s' + axis)
                attribute.lock_all(mesh)
    #END __add_scale_to_meshes()

    def __add_scale_to_control(self):
        if not self._addScaleToControl:
            return
        for ctl in self._addScaleToControl:
            msg = "addScaleToControl: Object does not exist: " + str(ctl)
            assert cmds.objExists(ctl),msg
            if not cmds.objExists(ctl + '.globalScale'):
                cmds.addAttr(ctl, longName = 'globalScale', shortName = 'gs',
                             attributeType = 'float', min = 0, defaultValue = 1,
                             keyable = True)
        self.__setup_scale_attribute()
    #END __add_scale_to_control()

    def __setup_scale_attribute(self):
        if not self._addSpaceSwitch:
            return
        for ctl in self._addScaleToControl:
            attribute.lock_n_hide(ctl, ['s'], True)
            for axis in 'xyz':
                if not cmds.listConnections(ctl + '.s' + axis):
                    if not cmds.isConnected(ctl + '.globalScale', ctl + '.s' + axis):
                        cmds.connectAttr(ctl + '.globalScale', ctl + '.s' + axis)
            attribute.lock_n_hide(ctl, ['s'], False)
    #END __setup_scale_attribute()

    def __setup_space_switch(self):
        for space in self._addSpaceSwitch:
            driven = None
            drivers = None
            attrName  = None
            attrHolder  = None
            withTranslation  = None
            for i in space.items():
                if i[0] == 'driven':
                    driven = i[1]
                elif i[0] == 'drivers':
                    drivers = i[1]
                elif i[0] == 'attrName':
                    attrName = i[1]
                elif i[0] == 'attrHolder':
                    attrHolder = i[1]
                elif i[0] == 'withTranslation':
                    withTranslation = i[1]
                else:
                    raise Exception("addSpaceSwitch: Please define 'driven', "
                                   "'drivers', 'attrName', 'attrHolder', "
                                   "'withTranslation' as keys!")

            if driven:
                print driven, drivers, attrName, attrHolder, withTranslation
    #END __setup_space_switch()

    def __limit_transforms(self):
        for d in self._limitTransforms:
            node = None
            attr = None
            mini  = None
            maxi  = None
            for i in d.items():
                if i[0] == 'node':
                    node = i[1]
                elif i[0] == 'attr':
                    attr = i[1]
                elif i[0] == 'min':
                    mini = i[1]
                elif i[0] == 'max':
                    maxi = i[1]
                else:
                    raise Exception("limitTransforms: Please define 'node', "
                                   "'attr', 'min', 'max' as keys!")

            if node:
                #--- enable the transforms
                enableMin = False
                enableMax = False

                if not mini == None:
                    enableMin = True
                if not maxi == None:
                    enableMax = True

                #--- specify default limitation values 
                if attr.startswith('t'):
                    if mini == None:
                        mini = -1
                    if maxi == None:
                        maxi = 1
                elif attr.startswith('r'):
                    if mini == None:
                        mini = -45
                    if maxi == None:
                        maxi = 45
                if attr.startswith('s'):
                    if mini == None:
                        mini = -1
                    if maxi == None:
                        maxi = 1

                #--- set translation
                if attr == 'tx':
                    cmds.transformLimits(node, etx = (enableMin, enableMax),
                                         tx = (mini, maxi))
                elif attr == 'ty':
                    cmds.transformLimits(node, ety = (enableMin, enableMax),
                                         ty = (mini, maxi))
                elif attr == 'tz':
                    cmds.transformLimits(node, etz = (enableMin, enableMax),
                                         tz = (mini, maxi))

                #--- set rotation
                if attr == 'rx':
                    cmds.transformLimits(node, erx = (enableMin, enableMax),
                                         rx = (mini, maxi))
                elif attr == 'ry':
                    cmds.transformLimits(node, ery = (enableMin, enableMax),
                                         ry = (mini, maxi))
                elif attr == 'rz':
                    cmds.transformLimits(node, erz = (enableMin, enableMax),
                                         rz = (mini, maxi))

                #--- set scale
                if attr == 'sx':
                    cmds.transformLimits(node, esx = (enableMin, enableMax),
                                         sx = (mini, maxi))
                elif attr == 'sy':
                    cmds.transformLimits(node, esy = (enableMin, enableMax),
                                         sy = (mini, maxi))
                elif attr == 'sz':
                    cmds.transformLimits(node, esz = (enableMin, enableMax),
                                         sz = (mini, maxi))
    #END __limit_transforms()

    def __hide_controls(self):
        if self._hideControls:
            for i in self.controls:
                cmds.setAttr(i.shape + '.v', 0)

        if self._hide:
            if isinstance(self._hide, list):
                for i in self._hide:
                    attribute.lock_n_hide(i, ['v'], True)
                    cmds.setAttr(i + '.v', 0)
            else:
                attribute.lock_n_hide(self._hide, ['v'], True)
                cmds.setAttr(self._hide + '.v', 0)
    #END __hide_controls()

    def __reparent_controls(self):
        if self._hookLastControl:
            attribute.lock_all(self.controls[-1].group, True)
            cmds.parent(self.controls[-1].group, self._hookLastControl)
            attribute.lock_all(self.controls[-1].group)
    #END __reparent_controls()

    def __lock_attributes(self):
        if not self._lockAttrs:
            return
        for attr in self._lockAttrs.items():
            key = attr[0]
            value = attr[1]
            assert cmds.objExists(key),("lockAttrs: Key object does not exist: " + key)
            for v in value:
                assert (cmds.objExists(key + '.' + v)),("lockAttrs: Given key "
                                                        "object and value do not "
                                                        "exist: " + key + "." + v)
            attribute.lock_n_hide(key, value, False)
    #END __lock_attributes()

    def __out_hooks(self):
        #--- outHooks
        for i, ctl in enumerate(self.controls):
            if not self._moduleName:
                name = self.guides[0][0] + str(i)
            else:
                name = self._moduleName + str(i)
            if self._withGimbal:
                self.outHooks[name] = ctl.gimbal
            else:
                self.outHooks[name] = ctl.transform
    #END __out_hooks()

    def __cleanup(self):
        if self._moduleName:
            guideGrp = self._moduleName.upper() + 'GUIDE'
            if cmds.objExists(guideGrp):
                cmds.delete(guideGrp)
            else:
                if self._guides:
                    for i in self._guides:
                        if cmds.objExists(i):
                            cmds.delete(i)
            guideTrn = self._side + '_' + self._moduleName + 'Guide_TRN'
            if cmds.objExists(guideTrn):
                cmds.delete(guideTrn)

        guideRoot = 'GUIDE_ROOT'
        if cmds.objExists(guideRoot):
            if not cmds.listRelatives(guideRoot, children=True):
                cmds.delete(guideRoot)
            elif not cmds.listRelatives(guideRoot, allDescendents=True, 
                                        type='goe_locator'):
                cmds.delete(guideRoot)

        #--- cleanup the constraints
        pac = cmds.ls(type='parentConstraint')
        pcn = cmds.ls(type='pointConstraint')
        ocn = cmds.ls(type='orientConstraint')
        scn = cmds.ls(type='scaleConstraint')
        constraints = [pac, pcn, ocn, scn]
        for const in constraints:
            for i in const:
                if not i:
                    continue
                attribute.lock_all(i)
                cmds.setAttr(i + '.ihi', 0)

        #--- lock and hide all to_lock nodes
        for i in self.lock:
            attribute.lock_all(i)
            cmds.setAttr(i + '.ihi', 0)

        #--- ihi unnecessary nodes
        for i in cmds.ls('*ikRPsolver*', '*ikSCsolver*'):
            if not i:
                continue
            cmds.setAttr(i + '.ihi', 0)

        #--- cleanup joints
        for jnt in self.joints:
            cmds.setAttr(jnt + '.ihi', 0)

        #--- hide joints
        for i, obj in enumerate(self.joints):
            for axis in 'xyz':
                if self._addIk:
                    cmds.setAttr(obj + '.t' + axis, keyable=False)
                    cmds.setAttr(obj + '.r' + axis, keyable=False)
                    cmds.setAttr(obj + '.s' + axis, keyable=False)
                else:
                    cmds.setAttr(obj + '.t' + axis, keyable=False, lock=True)
                    cmds.setAttr(obj + '.r' + axis, keyable=False, lock=True)
                    cmds.setAttr(obj + '.s' + axis, keyable=False, lock=True)
            cmds.setAttr(obj + '.v', keyable=False, lock=True)
            cmds.setAttr(obj + '.radi', keyable=False, channelBox=False)
            cmds.setAttr(obj + '.drawStyle', 0)
    #END __cleanup()

    def __create(self):
        #--- check parameters
        self.__check_parameters()

        #--- prepare guides
        self.__prepare_guides()

        #--- create mod group
        self.__create_mod_group()

        #--- setup mod group
        self.__setup_mod_group()

        #--- create controls
        self.__create_controls()

        #--- setup
        self.__setup()

        #--- setup mesh connections
        if not self._useJoints:
            #--- create constraints
            self.__prepare_constraints()
        else:
            if self._meshes:
                #--- create constraints
                self.__prepare_constraints()
            #--- create joints
            self.__prepare_joint_setup()
            if self._jointChain:
                #--- create jointChain
                self.__create_joint_chain()

                #--- create ikHandle
                self.__create_ik_setup()

        #--- add scale to meshes
        self.__add_scale_to_meshes()

        #--- add scale to control
        self.__add_scale_to_control()

        #--- setup space switch
        self.__setup_space_switch()

        #--- limit transforms
        self.__limit_transforms()

        #--- hide controls
        self.__hide_controls()

        #--- parent last control
        self.__reparent_controls()

        #--- lock attributes
        self.__lock_attributes()

        #--- outHooks
        self.__out_hooks()

        #--- cleanup
        self.__cleanup()
    #END __create()
#END PropCmds()
