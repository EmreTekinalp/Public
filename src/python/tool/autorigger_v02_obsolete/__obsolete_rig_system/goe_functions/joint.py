'''
Created on 31.08.2013
@author: Emre Tekinalp
@email: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Create different JointChains
'''

from maya import cmds

from goe_functions import ikhandle

reload(ikhandle)


class Joint(object):
    """ This is the base joint class to create a custom joint """
    def __init__(self,
                 side=None,
                 name=None,
                 suffix=None,
                 position=[0, 0, 0],
                 orientation=[0, 0, 0],
                 parent=True,
                 radius=1,
                 skinTag=True):
        #--- args
        self._side = side
        self._name = name
        self._suffix = suffix
        self._position = position
        self._orientation = orientation
        self._parent = parent
        self._radius = radius
        self._skinTag = skinTag

        #--- vars
        self.joint = None

        #--- methods
        self.__create()
    #END __init__()

    def __check_joint_name(self):
        """ Check the name of the joint """
        if not self._side:
            if not self._name:
                if not self._suffix:
                    self.joint = 'joint'
                else:
                    self.joint = 'joint_' + self._suffix
            else:
                if not self._suffix:
                    self.joint = self._name
                else:
                    self.joint = self._name + '_' + self._suffix
        else:
            if not self._name:
                if not self._suffix:
                    self.joint = self._side + '_joint'
                else:
                    self.joint = self._side + '_joint_' + self._suffix
            else:
                if not self._suffix:
                    self.joint = self._side + '_' + self._name + '_JNT'
                else:
                    self.joint = self._side + '_' + self._name + '_' + self._suffix

        if not self._name:
            if not self._side:
                if not self._suffix:
                    self.joint = 'joint'
                else:
                    self.joint = 'joint_' + self._suffix
            else:
                if not self._suffix:
                    self.joint = self._side + '_joint'
                else:
                    self.joint = self._side + '_joint_' + self._suffix
        else:
            if not self._side:
                if not self._suffix:
                    self.joint = self._name
                else:
                    self.joint = self._name + '_' + self._suffix
            else:
                if not self._suffix:
                    self.joint = self._side + '_' + self._name + '_JNT'
                else:
                    self.joint = self._side + '_' + self._name + '_' + self._suffix
    #END __check_joint_name()

    def __create_joint(self):
        """ Create a joint """
        jnt = None
        if self._parent:
            sel = cmds.ls(selection=True)
            if not sel:
                jnt = cmds.joint(name=self.joint, position=self._position,
                                 orientation=self._orientation,
                                 radius=self._radius)
            else:
                if not cmds.nodeType(sel[0]) == 'joint':
                    jnt = cmds.joint(name=self.joint, position=self._position,
                                     orientation=self._orientation,
                                     radius=self._radius)
                    cmds.setAttr(jnt + '.t', 0, 0, 0)
                    cmds.setAttr(jnt + '.r', 0, 0, 0)
                    cmds.setAttr(jnt + '.s', 1, 1, 1)
                else:
                    jnt = cmds.joint(name=self.joint, position=self._position,
                                     orientation=self._orientation,
                                     radius=self._radius)
                    if "|" in jnt:
                        self.joint = jnt.split("|")[-1]
                    else:
                        self.joint = jnt
        else:
            jnt = cmds.joint(name=self.joint, position=self._position,
                             orientation=self._orientation, radius=self._radius)
            self.joint = jnt
            cmds.select(clear=True)
        return
    #END __create_joint()

    def __add_skin_tag(self):
        """ Add a skin tag to the joint """
        cmds.addAttr(self.joint, longName='SKIN', attributeType='bool')
        if self._skinTag:
            cmds.setAttr(self.joint + '.SKIN', 1)
        else:
            cmds.setAttr(self.joint + '.SKIN', 0)
    #END __add_skin_tag()

    def __create(self):
        """ Call the methods in the proper order """
        #--- check the joint name
        self.__check_joint_name()
        #--- create a joint
        self.__create_joint()
        #--- add skin tag
        self.__add_skin_tag()
    #END __create()
#END Joint()


class Chain(object):
    """this is the base jointChain class, which will be used to create jointChains"""

    def __init__(self,
                 side=None,
                 name=None,
                 suffix=None,
                 position=[0, 0, 0],
                 orientation=[0.0, 0.0, 0.0],
                 offset=[0, 0, 0],
                 amount=0,
                 mirror=False,
                 radius=1):
        #--- args
        self._side = side
        self._name = name
        self._suffix = suffix
        self._position = position
        self._orientation = orientation
        self._offset = offset
        self._amount = amount
        self._mirror = mirror
        self._radius = radius

        #--- vars
        self.joint_names = list()
        self.mirrored_joint_names = list()

        #--- methods
        self.__create()
    #END __init__()

    def __create_chain(self):
        """ Create a joint chain by the specified flags and values """
        if isinstance(self._name, list):
            for i in range(len(self._name)):
                jnt = self._create_joint(i)
                self.joint_names.append(jnt.name)
        else:
            for i in range(self._amount):
                jnt = self._create_joint(i)
                self.joint_names.append(jnt.name)

        cmds.select(clear=True)

        #--- reorient the jointChain
        for i in self.joint_names:
            cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint='xyz',
                       secondaryAxisOrient='yup')
        #--- zero out the jointOrient values of the last joint
        cmds.setAttr(self.joint_names[-1] + '.jointOrient', 0, 0, 0)
    #END __create_chain()

    def __create_joint(self, i=0):
        """ Create the joint """
        jnt = None
        if not self._position:
            off = [0, 0, 0]
            if self._offset == [0, 0, 0]:
                off = [0, 0 + i, 0]
            elif self._offset[0] > 0:
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [self._offset[0] + i, self._offset[1] + i,
                               self._offset[2] + i]
                    else:
                        off = [self._offset[0] + i, self._offset[1] + i, 0]
                else:
                    off = [self._offset[0] + i, 0, 0]
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [0, self._offset[1] + i, self._offset[2] + i]
                    else:
                        off = [0, self._offset[1] + i, 0]
                else:
                    off = [0, 0 + i, 0]
            jnt = Joint(side=self._side, name=self._name[i],
                        suffix=self._suffix, position=off,
                        parent=True, radius=self._radius)
        else:
            jnt = Joint(side=self._side, name=self._name[i],
                        suffix=self._suffix, position=self._position[i],
                        orientation=self._orientation[i], parent=True,
                        radius=self._radius)
        return jnt
    #END __create_joint()

    def __mirror_chain(self):
        """ Mirror the created jointChain create one temporary joint at the origin """
        if not self._mirror:
            return
        tmp_jnt = cmds.joint(position=[0, 0, 0])

        #--- parent the chain to that joint
        cmds.parent(self.joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if self._side == 'L':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'R'))
        elif self._side == 'R':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'L'))
        else:
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True)

        #--- unparent the chain and delete the temporary joint
        cmds.parent(self.joint_names[0], self.mirrored_joint_names[0], world=True)
        cmds.delete(tmp_jnt)
        cmds.select(clear=True)
    #END __mirror_chain()

    def __create(self):
        """ Call the methods in the proper order """
        #--- create the chain
        self.__create_chain()
        #--- mirror the chain
        self.__mirror_chain()
    #END __create()
#END Chain()


class FkChain(object):
    """ This is the fk_chain class, which will be used to create fk based
    jointChains with fkControls """

    def __init__(self,
                 side=None,
                 name=None,
                 suffix=None,
                 position=[0, 0, 0],
                 orientation=[0, 0, 0],
                 offset=[0, 0, 0],
                 amount=3,
                 mirror=False,
                 radius=1):
        #--- args
        self._side = side
        self._name = name
        self._suffix = suffix
        self._position = position
        self._orientation = orientation
        self._offset = offset
        self._amount = amount
        self._mirror = mirror
        self._radius = radius

        #--- vars
        self.joint_names = list()
        self.mirrored_joint_names = list()

        #--- methods
        self.__create()
    #end def __init__()

    def __create_chain(self):
        """ Create a joint chain by the specified flags and values """
        if isinstance(self._name, list):
            for i in range(len(self._name)):
                jnt = self.__create_joint(i)
                self.joint_names.append(jnt.name)
        else:
            for i in range(self._amount):
                jnt = self.__create_joint(i)
                self.joint_names.append(jnt.name)

        cmds.select(clear=True)

        #--- reorient the jointChain
        for i in self.joint_names:
            cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint='xyz',
                       secondaryAxisOrient='yup')
        #--- zero out the jointOrient values of the last joint
        cmds.setAttr(self.joint_names[-1] + '.jointOrient', 0, 0, 0)
    #END __create_chain()

    def __create_joint(self, i=0):
        """ Create the joint """
        jnt = None
        if not self._position:
            off = [0, 0, 0]
            if self._offset == [0, 0, 0]:
                off = [0, 0 + i, 0]
            elif self._offset[0] > 0:
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [self._offset[0] + i, self._offset[1] + i,
                               self._offset[2] + i]
                    else:
                        off = [self._offset[0] + i, self._offset[1] + i, 0]
                else:
                    off = [self._offset[0] + i, 0, 0]
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [0, self._offset[1] + i, self._offset[2] + i]
                    else:
                        off = [0, self._offset[1] + i, 0]
                else:
                    off = [0, 0 + i, 0]
            jnt = Joint(side=self._side, name=self._name[i] + 'FK',
                        suffix=self._suffix, position=off,
                        parent=True, radius=self._radius)
        else:
            jnt = Joint(side=self._side, name=self._name[i] + 'FK',
                        suffix=self._suffix, position=self._position[i],
                        orientation=self._orientation[i], parent=True,
                        radius=self._radius)
        return jnt
    #END __create_joint()

    def __mirror_chain(self):
        """ Mirror the created jointChain create one temporary joint at the origin """
        if not self._mirror:
            return
        tmp_jnt = cmds.joint(position=[0, 0, 0])

        #--- parent the chain to that joint
        cmds.parent(self.joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if self._side == 'L':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'R'))
        elif self._side == 'R':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'L'))
        else:
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True)

        #--- unparent the chain and delete the temporary joint
        cmds.parent(self.joint_names[0], self.mirrored_joint_names[0], world=True)
        cmds.delete(tmp_jnt)
        cmds.select(clear=True)
    #END __mirror_chain()

    def __create(self):
        """ Call the methods in the proper order """
        #--- create the chain
        self.__create_chain()
        #--- mirror the chain
        self.__mirror_chain()
    #END __create()
#END FkChain()


class IkChain(object):
    """
    this is the ik_chain class, which will be used to create an ik based
    jointChain with an specified ik_solver
    """
    def __init__(self,
                 side=None,
                 name=None,
                 suffix=None,
                 position=[0, 0, 0],
                 orientation=[0, 0, 0],
                 ikSolver='ikRPSolver',
                 ikCurve=None,
                 ikName=None,
                 offset=[0, 0, 0],
                 amount=0,
                 mirror=False,
                 radius=1,
                 parentJoint=None,
                 parentIk=None):
        #--- args
        self._side = side
        self._name = name
        self._suffix = suffix
        self._position = position
        self._orientation = orientation
        self._ikSolver = ikSolver
        self._ikCurve = ikCurve
        self._ikName = ikName
        self._offset = offset
        self._amount = amount
        self._mirror = mirror
        self._radius = radius
        self._parentJoint = parentJoint
        self._parentIk = parentIk

        #--- vars
        self.joint_names = list()
        self.ik_handle_names = list()

        self.mirrored_joint_names = list()
        self.mirrored_ik_handle_names = list()

        #--- methods
        self.__create()
    #END __init__()

    def __create_chain(self):
        """ Create a joint chain by the specified flags and values """
        if isinstance(self._name, list):
            self.joint_names = [self.__create_joint(i) for i in range(len(self._name))]
        else:
            for i in range(self._amount):
                jnt = self.__create_joint(i)
                self.joint_names.append(jnt.joint)
        cmds.select(clear=True)

        #--- reorient the jointChain
        for i in self.joint_names:
            cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint='xyz',
                       secondaryAxisOrient='yup')
        #--- zero out the jointOrient values of the last joint
        cmds.setAttr(self.joint_names[-1] + '.jointOrient', 0, 0, 0)
    #END __create_chain()

    def __create_joint(self, i=0):
        """ Create the joint """
        jnt = None
        if not self._position:
            off = [0, 0, 0]
            if self._offset == [0, 0, 0]:
                off = [0, 0 + i, 0]
            elif self._offset[0] > 0:
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [self._offset[0] + i, self._offset[1] + i,
                               self._offset[2] + i]
                    else:
                        off = [self._offset[0] + i, self._offset[1] + i, 0]
                else:
                    off = [self._offset[0] + i, 0, 0]
                if self._offset[1] > 0:
                    if self._offset[2] > 0:
                        off = [0, self._offset[1] + i, self._offset[2] + i]
                    else:
                        off = [0, self._offset[1] + i, 0]
                else:
                    off = [0, 0 + i, 0]
            jnt = Joint(side=self._side, name=self._name[i] + 'IK',
                        suffix=self._suffix, position=off,
                        parent=True, radius=self._radius)
        else:
            jnt = Joint(side=self._side, name=self._name[i] + 'IK',
                        suffix=self._suffix, position=self._position[i],
                        orientation=self._orientation[i], parent=True,
                        radius=self._radius)
        return jnt.joint
    #END __create_joint()

    def __setup_ik_handle(self):
        """ Setup the ik handle properly """
        #--- parent the joints and ikHandles
        if self._parentJoint:
            if self._mirror:
                if isinstance(self._parentJoint, list):
                    if len(self._parentJoint) == 2:
                        cmds.parent(self.joint_names[0], self._parentJoint[0])
                        cmds.parent(self.mirrored_joint_names[0], self._parentJoint[1])
                    else:
                        raise Exception('First element is left and second is right!'
                                        'You have to specify proper parent nodes!')
                else:
                    cmds.parent(self.joint_names[0],
                                self.mirrored_joint_names[0], self._parentIk)
            else:
                cmds.parent(self.joint_names[0], self._parentJoint)
        #-- ikHandles
        if self._parentIk:
            if self._mirror:
                if isinstance(self._parentIk, list):
                    if len(self._parentIk) == 2:
                        cmds.parent(self.ik_handle_names[0], self._parentIk[0])
                        cmds.parent(self.mirrored_ik_handle_names[0], self._parentIk[1])
                    else:
                        raise Exception('First element is left and second is right!'
                                        'You have to specify proper parent nodes!')
                else:
                    cmds.parent(self.ik_handle_names[0],
                                self.mirrored_ik_handle_names[0], self._parentIk)
            else:
                cmds.parent(self.ik_handle_names[0], self._parentIk)
    #END __setup_ik_handle()

    def __create_ik_handle(self):
        """ Create the specified ikHandle """
        ikH = ikhandle.IkHandle()
        if not self._ikName:
            #--- ikSCSolver
            if self._ikSolver == 'ikSCSolver':
                self.ik_handle_names = ikH.ikSCsolver(startJoint=self.joint_names[0],
                                                      endEffector=self.joint_names[-1],
                                                      side=self._side, name=self._name[0],
                                                      suffix=self._suffix)
            #--- ikSplineSolver
            elif self._ikSolver == 'ikSplineSolver':
                self.ik_handle_names = ikH.ikSplineSolver(startJoint=self.joint_names[0],
                                                          endEffector=self.joint_names[-1],
                                                          curve=self._ikCurve,
                                                          side=self._side,
                                                          name=self._name[0],
                                                          suffix=self._suffix)
            #--- ikRPsolver
            else:
                self.ik_handle_names = ikH.ikRPsolver(startJoint=self.joint_names[0],
                                                      endEffector=self.joint_names[-1],
                                                      side=self._side, name=self._name[0],
                                                      suffix=self._suffix)
        else:
            #--- ikSCSolver
            if self._ikSolver == 'ikSCSolver':
                self.ik_handle_names = ikH.ikSCsolver(startJoint=self.joint_names[0],
                                                      endEffector=self.joint_names[-1],
                                                      side=self._side, name=self._ikName,
                                                      suffix=self._suffix)
            #--- ikSplineSolver
            elif self._ikSolver == 'ikSplineSolver':
                self.ik_handle_names = ikH.ikSplineSolver(startJoint=self.joint_names[0],
                                                          endEffector=self.joint_names[-1],
                                                          curve=self._ikCurve,
                                                          side=self._side,
                                                          name=self._ikName,
                                                          suffix=self._suffix)
            #--- ikRPsolver
            else:
                self.ik_handle_names = ikH.ikRPsolver(startJoint=self.joint_names[0],
                                                      endEffector=self.joint_names[-1],
                                                      side=self._side,
                                                      name=self._ikName,
                                                      suffix=self._suffix)
        return self.ik_handle_names
    #END __create_ik_handle()

    def __mirror_chain(self):
        """ Mirror the created jointChain create one temporary joint at the origin """
        if not self._mirror:
            return
        tmp_jnt = cmds.joint(position=[0, 0, 0])

        #--- parent the chain to that joint
        cmds.parent(self.joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if self._side == 'L':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'R'))
        elif self._side == 'R':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True,
                                                         searchReplace=(self._side, 'L'))
        else:
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0],
                                                         mirrorYZ=True,
                                                         mirrorBehavior=True)

        #--- unparent the chain and delete the temporary joint
        cmds.parent(self.joint_names[0], self.mirrored_joint_names[0], world=True)
        cmds.delete(tmp_jnt)
        cmds.select(clear=True)

        #--- rename the side of the effector correctly and store the ik, eff in a list
        mirrored_ik = self.mirrored_joint_names[0][0] + self.ik_handle_names[0][1:]
        mirrored_eff = cmds.rename(self.mirrored_joint_names[-1],
                                   self.mirrored_joint_names[0][0] +
                                   self.ik_handle_names[-1][1:])
        self.mirrored_ik_handle_names = [mirrored_ik, mirrored_eff]
        self.mirrored_joint_names.pop(-1)
    #END __mirror_chain()

    def __create(self):
        """ Call the methods in the proper order """
        #--- create the ik chain
        self.__create_chain()
        #--- create ik handle
        self.__create_ik_handle()
        #--- setup ik handle
        self.__setup_ik_handle()
    #END __create()
#END IkChain()
