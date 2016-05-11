'''
Created on 28.08.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the ikHandle class
'''

from maya import cmds


class IkHandle(object):
    """ This is the base ik class, which will be used to create iks """
    def __init__(self):
        #--- vars
        self.ik_name = list()
    #END __init__()

    def __check_ik_joints(self, startJoint=None, endEffector=None):
        #--- check if startJoint and endEffector exists
        assert cmds.objExists(startJoint), 'StartJoint is missing, cannot create ik_handle!'
        assert cmds.objExists(endEffector), 'EndEffector to ' + startJoint + ' is missing!'
    #END __check_ik_joints()

    def __check_ik_name(self, startJoint=None, endEffector=None, side=None,
                        name=None, suffix=None):
        #--- check if joints exist
        self.__check_ik_joints(startJoint=startJoint, endEffector=endEffector)

        #--- get the side info of the startJoint and store it
        side_list = ['C_', 'L_', 'R_', 'c_', 'l_', 'r_']
        for i in side_list:
            if i in startJoint:
                side = startJoint[0]
                break
            elif i in endEffector:
                side = endEffector[0]

        #--- check names
        if not side:
            if not name:
                if not suffix:
                    self.ik_name = 'ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = 'ik_handle_IK'
                else:
                    self.ik_name = 'ik_handle_' + suffix
            else:
                if not suffix:
                    self.ik_name = name
                elif suffix == 'JNT':
                    self.ik_name = name + '_IK'
                else:
                    self.ik_name = name + '_' + suffix
        else:
            if not name:
                if not suffix:
                    self.ik_name = side + '_ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = side + '_ik_handle_IK'
                else:
                    self.ik_name = side + '_ik_handle_' + suffix
            else:
                if not suffix:
                    self.ik_name = side + '_' + name + '_IK'
                elif suffix == 'JNT':
                    self.ik_name = side + '_' + name + '_IK'
                else:
                    self.ik_name = side + '_' + name + '_' + suffix

        if not name:
            if not side:
                if not suffix:
                    self.ik_name = 'ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = 'ik_handle_IK'
                else:
                    self.ik_name = 'ik_handle_' + suffix
            else:
                if not suffix:
                    self.ik_name = side + '_ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = side + 'ik_handle_IK'
                else:
                    self.ik_name = side + '_ik_handle_' + suffix
        else:
            if not side:
                if not suffix:
                    self.ik_name = name
                elif suffix == 'JNT':
                    self.ik_name = name + '_IK'
                else:
                    self.ik_name = name + '_' + suffix
            else:
                if not suffix:
                    self.ik_name = side + '_' + name + '_IK'
                elif suffix == 'JNT':
                    self.ik_name = side + '_' + name + '_IK'
                else:
                    self.ik_name = side + '_' + name + '_' + suffix
    #END __check_ik_name()

    def ikSCsolver(self,
                   startJoint=None,
                   endEffector=None,
                   side=None,
                   name=None,
                   suffix=None,
                   parent=None,
                   hide=False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint=startJoint, endEffector=endEffector,
                             side=side, name=name, suffix=suffix)

        #--- create the ik_handle
        ik = cmds.ikHandle(startJoint=startJoint, endEffector=endEffector,
                           name=self.ik_name, solver='ikSCsolver')

        #--- rename the effector
        eff = cmds.rename(ik[-1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = [ik[0], eff]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ikHandle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear=True)
        return ik_handle
    #END ikSCsolver()

    def ikRPsolver(self,
                   startJoint=None,
                   endEffector=None,
                   side=None,
                   name=None,
                   suffix=None,
                   parent=None,
                   hide=False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint=startJoint, endEffector=endEffector,
                             side=side, name=name, suffix=suffix)

        #--- create the ik_handle
        ik = cmds.ikHandle(startJoint=startJoint, endEffector=endEffector,
                           name=self.ik_name, solver='ikRPsolver')

        #--- rename the effector
        eff = cmds.rename(ik[-1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = [ik[0], eff]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ik handle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear=True)
        return ik_handle
    #END ikRPsolver()

    def ikSplineSolver(self,
                       startJoint=None,
                       endEffector=None,
                       curve=None,
                       side=None,
                       name=None,
                       suffix=None,
                       parent=None,
                       hide=False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint=startJoint, endEffector=endEffector,
                             side=side, name=name, suffix=suffix)

        #--- create the ik_handle
        if not curve:
            ik = cmds.ikHandle(startJoint=startJoint, endEffector=endEffector,
                               createCurve=True, name=self.ik_name,
                               solver='ikSplineSolver')
        else:
            assert cmds.objExists(curve), 'There is no specified curve: ' + curve
            ik = cmds.ikHandle(startJoint=startJoint, endEffector=endEffector,
                               curve=curve, createCurve=False,
                               name=self.ik_name, solver='ikSplineSolver')

        #--- rename the effector
        eff = cmds.rename(ik[1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = list()
        if not curve:
            #--- rename the automated curve
            crv = cmds.rename(ik[-1], ik[0] + 'CRV')
            ik_handle = [ik[0], eff, crv]
        else:
            ik_handle = [ik[0], eff, curve]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ikHandle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear=True)
        return ik_handle
    #END ikSplineSolver()
#END IkHandle()
